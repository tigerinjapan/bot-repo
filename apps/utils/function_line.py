"""
LINEメッセージAPI
"""

import sys

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_api as func_api
import apps.utils.function_beautiful_soup as func_bs
import apps.utils.function_gemini as func_gemini

# スクリプト名
SCRIPT_NAME = func.get_app_name(__file__)

# LINE API情報
LINE_CHANNEL_ID = func.get_env_val("LINE_CHANNEL_ID")
LINE_CHANNEL_SECRET = func.get_env_val("LINE_CHANNEL_SECRET")
LINE_CHANNEL_ID_2 = func.get_env_val("LINE_CHANNEL_ID_2")
LINE_CHANNEL_SECRET_2 = func.get_env_val("LINE_CHANNEL_SECRET_2")

# 改行
NEW_LINE = const.SYM_NEW_LINE


def get_channel_access_token(admin_flg: bool = const.FLG_OFF) -> str:
    """
    チャネル・アクセストークン取得

    引数:
        admin_flg (bool): 管理者フラグ
    """
    url = f"{const.URL_LINE_API}/oauth2/v3/token"

    client_id = LINE_CHANNEL_ID
    client_secret = LINE_CHANNEL_SECRET
    if func.is_local_env() or admin_flg:
        client_id = LINE_CHANNEL_ID_2
        client_secret = LINE_CHANNEL_SECRET_2

    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }

    result = func_api.get_response_result(
        url,
        request_type=const.REQUEST_TYPE_POST,
        data=data,
        header_json_flg=const.FLG_OFF,
    )

    if not result:
        return const.SYM_BLANK

    # トークン・タイプ
    token_type = result["token_type"]

    # アクセストークン
    access_token = result["access_token"]

    # 有効期限 (秒)
    expires_in = result["expires_in"]

    token = f"{token_type} {access_token}"

    expires_min = int(expires_in // 60)
    func.print_debug_msg(const.STR_TOKEN, f"{const.STR_EXPIRATION}: {expires_min} min")

    # メッセージ数チェック
    total_usage = check_message_count(token)

    if (const.MAX_MSG_API_CNT - 20) < total_usage:
        token = const.NONE_CONSTANT
    return token


def check_message_count(access_token: str) -> int:
    """
    メッセージ件数チェック
    """
    url = f"{const.URL_LINE_API}/v2/bot/message/quota/consumption"
    headers = {"Authorization": access_token}
    result = func_api.get_response_result(url, headers=headers)
    if result:
        total_usage = result["totalUsage"]
    else:
        total_usage = const.MAX_MSG_API_CNT

    message_count = f"{total_usage} / {const.MAX_MSG_API_CNT}"
    func.print_debug_msg(const.STR_MESSAGE, message_count)
    return total_usage


def send_line_msg(access_token: str, messages: list):
    """
    メッセージ送信
    """
    url = f"{const.URL_LINE_API}/v2/bot/message/broadcast"
    headers = {"Authorization": access_token}
    data = {"messages": messages}
    json_data = func.get_dumps_json(data, ensure_ascii=const.FLG_ON)
    result = func_api.get_response_result(
        url, request_type=const.REQUEST_TYPE_POST, headers=headers, data=json_data
    )

    if result:
        curr_func_nm = sys._getframe().f_code.co_name
        func.print_error_msg(
            SCRIPT_NAME, curr_func_nm, const.STR_LINE_API, result["details"]
        )


def get_line_messages(msg_list: list[list[str]]):
    """
    LINE送信用のJSONデータ取得
    """
    messages = []

    for msg_data in msg_list:
        msg_type = msg_data[0]
        text_msg = msg_data[1]
        json_object = {const.STR_TYPE: msg_type}

        if msg_type == const.MSG_TYPE_IMG:
            img_url = text_msg
            update_data = {"originalContentUrl": img_url, "previewImageUrl": img_url}
        else:
            update_data = {const.MSG_TYPE_TXT: text_msg}

        json_object.update(update_data)
        messages.append(json_object)

    return messages


def send_msg_for_admin(msg_json: list, admin_flg: bool = const.FLG_ON):
    """
    メッセージ送信
    """
    token = get_channel_access_token(admin_flg)
    if token:
        send_line_msg(token, msg_json)


def get_template_msg_json(alt_text: str, actions):
    """
    テンプレート・メッセージ取得
    """
    # base_url = func_api.URL_KOYEB_APP
    img_url, template_title, template_text = get_temp_img()

    json_object = {
        "type": const.MSG_TYPE_TMP,
        "altText": alt_text,
        "template": {
            "type": "buttons",
            "thumbnailImageUrl": img_url,
            "imageAspectRatio": "rectangle",
            "imageSize": "cover",
            "imageBackgroundColor": const.COLOR_CD_WHITE,
            "title": template_title,
            "text": template_text,
            # "defaultAction": {
            #     "type": "uri",
            #     "label": "View detail",
            #     "uri": img_url,
            # },
            "actions": actions,
        },
    }
    return json_object


def get_flex_msg_json(
    alt_text: str, data_list, flex_type: str = const.MSG_TYPE_CAROUSEL
):
    """
    フレックス・メッセージ取得
    """
    contents = get_bubble_contents(data_list)
    json_object = {
        "type": const.MSG_TYPE_FLEX,
        "altText": alt_text,
        "contents": {"type": flex_type, "contents": contents},
    }
    return json_object


def get_bubble_contents(data_list):
    """
    バーブル・コンテンツ取得
    """
    header_text_list = data_list[0]
    percent_list = data_list[1]
    bg_color_list = [
        ["#0D8186", "#9FD8E36E", "#27ACB2"],
        ["#DE5658", "#FAD2A76E", "#FF6B6E"],
        ["#7D51E4", "#9FD8E36E", "#A17DF5"],
    ]
    body_text_list = data_list[2]

    bubble_contents = []

    for header_text, percent, bg_color, body_text in zip(
        header_text_list, percent_list, bg_color_list, body_text_list
    ):
        contents = {
            "type": "bubble",
            "size": "nano",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": header_text,
                        "color": const.COLOR_CD_WHITE,
                        "align": "start",
                        "size": "md",
                        "gravity": const.ALIGN_CENTER,
                    },
                    {
                        "type": "text",
                        "text": percent,
                        "color": const.COLOR_CD_WHITE,
                        "align": "start",
                        "size": "xs",
                        "gravity": const.ALIGN_CENTER,
                        "margin": "lg",
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [{"type": "filler"}],
                                "width": percent,
                                "backgroundColor": bg_color[0],
                                "height": "6px",
                            }
                        ],
                        "backgroundColor": bg_color[1],
                        "height": "6px",
                        "margin": "sm",
                    },
                ],
                "backgroundColor": bg_color[2],
                "paddingTop": "19px",
                "paddingAll": "12px",
                "paddingBottom": "16px",
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": body_text,
                                "color": "#8C8C8C",
                                "size": "sm",
                                "wrap": const.FLG_ON,
                            }
                        ],
                        "flex": 1,
                    }
                ],
                "spacing": "md",
                "paddingAll": "12px",
            },
            "styles": {"footer": {"separator": const.FLG_OFF}},
        }
        bubble_contents.append(contents)
    return bubble_contents


def get_temp_img(section: str = const.STR_WORLD):
    """
    イメージ取得
    """
    img_url = headline = const.SYM_BLANK

    title = f"CNN {func.upper_str(section)}"
    url = f"https://edition.cnn.com/{section}"
    class_ = "container__item--type-media-image"
    soup = func_bs.get_elem_from_url(url, attr_val=class_)
    if soup:
        img_elem = func_bs.find_elem_by_class(soup, "image__hide-placeholder")
        img_url = img_elem.get("data-url").replace("?c=original", const.SYM_BLANK)
        headline_elem = func_bs.find_elem_by_class(soup, "container__headline-text")
        headline_text = headline_elem.text
        response = func_gemini.get_gemini_response(
            title, headline_text, msg_flg=const.FLG_ON
        )
        if response:
            headline = response[0]
        else:
            headline = f"{headline_text[57:]}..."
    return img_url, title, headline


if __name__ == const.MAIN_FUNCTION:
    # get_channel_access_token()
    get_temp_img()
