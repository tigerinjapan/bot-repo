# 説明: LINEメッセージAPI

import sys

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_api as func_api

# スクリプト名
SCRIPT_NAME = func.get_app_name(__file__)

# URL
URL_LINE_API = "https://api.line.me"
URL_KOYEB_APP = "https://" + func.get_env_val("URL_KOYEB")
URL_TODAY_IMG = f"{URL_KOYEB_APP}/{const.STR_IMG}/{const.APP_TODAY}"

# LINE API情報
STR_LINE_API = "LINE API"
LINE_CHANNEL_ID = func.get_env_val("LINE_CHANNEL_ID")
LINE_CHANNEL_SECRET = func.get_env_val("LINE_CHANNEL_SECRET")
LINE_CHANNEL_ID_2 = func.get_env_val("LINE_CHANNEL_ID_2")
LINE_CHANNEL_SECRET_2 = func.get_env_val("LINE_CHANNEL_SECRET_2")
MAX_MSG_API_CNT = 200

# 改行
NEW_LINE = const.SYM_NEW_LINE

# メッセージタイプ
MSG_TYPE_TXT = "text"
MSG_TYPE_IMG = "image"
MSG_TYPE_TMP = "template"
MSG_TYPE_BTN = "button"
MSG_TYPE_FLEX = "flex"
MSG_TYPE_CAROUSEL = "carousel"
MSG_TYPE_BUBBLE = "bubble"


# チャネル・アクセストークン取得
def get_channel_access_token(admin_flg: bool = const.FLG_OFF) -> str:
    url = f"{URL_LINE_API}/oauth2/v3/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    client_id = LINE_CHANNEL_ID
    client_secret = LINE_CHANNEL_SECRET
    if admin_flg:
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
        headers=headers,
        data=data,
        header_json_flg=const.FLG_OFF,
    )

    if not result:
        return const.SYM_BLANK

    # トークン・タイプ
    token_type = result["token_type"]

    # アクセストークン
    access_token = result["access_token"]

    # 有効期限（秒）
    expires_in = result["expires_in"]

    token = f"{token_type} {access_token}"

    expires_min = int(expires_in / 60)
    func.print_info_msg(const.STR_TOKEN_JA, f"{const.STR_EXPIRE_JA}: {expires_min}分")

    # メッセージ数チェック
    total_usage = check_message_count(token)

    if (MAX_MSG_API_CNT - 20) < total_usage:
        token = const.NONE_CONSTANT
    return token


# メッセージ件数取得
def check_message_count(access_token: str) -> int:
    url = f"{URL_LINE_API}/v2/bot/message/quota/consumption"
    headers = {"Authorization": access_token}
    result = func_api.get_response_result(url, headers=headers)
    if result:
        total_usage = result["totalUsage"]
    else:
        total_usage = MAX_MSG_API_CNT

    message_count = f"{total_usage} / {MAX_MSG_API_CNT}"
    func.print_info_msg(const.STR_MESSAGE_JA, message_count)
    return total_usage


# メッセージ送信
def send_message(access_token: str, messages):
    url = f"{URL_LINE_API}/v2/bot/message/broadcast"
    headers = {"Authorization": access_token}
    data = {"messages": messages}
    json_data = func.get_dumps_json(data)
    result = func_api.get_response_result(
        url, request_type=const.REQUEST_TYPE_POST, headers=headers, data=json_data
    )

    if result:
        curr_func_nm = sys._getframe().f_code.co_name
        func.print_error_msg(SCRIPT_NAME, curr_func_nm, STR_LINE_API, result["details"])


# LINE送信用のJSONデータ取得
def get_line_messages(msg_list: list[list[str]]):
    messages = []

    for msg_data in msg_list:
        msg_type = msg_data[0]
        text_msg = msg_data[1]
        json_object = {const.STR_TYPE: msg_type}

        if msg_type == MSG_TYPE_IMG:
            img_url = text_msg
            update_data = {"originalContentUrl": img_url, "previewImageUrl": img_url}
        else:
            update_data = {"text": text_msg}

        json_object.update(update_data)
        messages.append(json_object)

    return messages


# メッセージ送信
def send_text_msg(msg_json, admin_flg: bool = const.FLG_ON):
    token = get_channel_access_token(admin_flg)
    send_message(token, msg_json)


# テンプレート・メッセージ取得
def get_template_msg_json(
    alt_text: str, template_title: str, template_text: str, actions
):
    # base_url = URL_KOYEB_APP
    img_url = URL_TODAY_IMG

    json_object = {
        "type": MSG_TYPE_TMP,
        "altText": alt_text,
        "template": {
            "type": "buttons",
            # "thumbnailImageUrl": img_url,
            "imageAspectRatio": "rectangle",
            "imageSize": "cover",
            "imageBackgroundColor": "#FFFFFF",
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


# フレックスメッセージ取得
def get_flex_msg_json(alt_text: str, data_list, flex_type: str = MSG_TYPE_CAROUSEL):
    contents = get_bubble_contents(data_list)
    json_object = {
        "type": MSG_TYPE_FLEX,
        "altText": alt_text,
        "contents": {"type": flex_type, "contents": contents},
    }
    return json_object


# バーブルコンテンツ取得
def get_bubble_contents(data_list):
    list_header_text = data_list[0]
    list_percent = data_list[1]
    list_bg_color = [
        ["#0D8186", "#9FD8E36E", "#27ACB2"],
        ["#DE5658", "#FAD2A76E", "#FF6B6E"],
        ["#7D51E4", "#9FD8E36E", "#A17DF5"],
    ]
    list_body_text = data_list[2]

    bubble_contents = []

    for header_text, percent, bg_color, body_text in zip(
        list_header_text, list_percent, list_bg_color, list_body_text
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
                        "color": "#ffffff",
                        "align": "start",
                        "size": "md",
                        "gravity": "center",
                    },
                    {
                        "type": "text",
                        "text": percent,
                        "color": "#ffffff",
                        "align": "start",
                        "size": "xs",
                        "gravity": "center",
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


if __name__ == const.MAIN_FUNCTION:
    get_channel_access_token()
