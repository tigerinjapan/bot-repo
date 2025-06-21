# 説明: LINEメッセージAPI

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_api as func_api

# アプリケーション
app_name = func.get_app_name(__file__)

# URL
URL_LINE_API = "https://api.line.me"

# LINE API情報
STR_LINE_API = "LINE API"
LINE_CHANNEL_ID = func.get_env_val("LINE_CHANNEL_ID")
LINE_CHANNEL_SECRET = func.get_env_val("LINE_CHANNEL_SECRET")
MAX_MSG_API_CNT = 200

# 改行
NEW_LINE = const.SYM_NEW_LINE

# メッセージタイプ
MSG_TYPE_TXT = "text"
MSG_TYPE_IMG = "image"
MSG_TYPE_TMP = "template"


# チャネル・アクセストークン取得
def get_channel_access_token() -> str:
    url = f"{URL_LINE_API}/oauth2/v3/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": LINE_CHANNEL_ID,
        "client_secret": LINE_CHANNEL_SECRET,
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
        func.print_error_msg(STR_LINE_API, result["details"])


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


# LINEメッセージデータ取得
def get_send_messages(msg):
    messages = []
    messages.append(msg)
    return messages


# テンプレート・メッセージ取得
def get_template_msg_json(alt_text: str, template_text: str, actions):
    # base_url = URL_KOYEB_APP
    # img_url = URL_TODAY_IMG

    json_object = {
        "type": MSG_TYPE_TMP,
        "altText": alt_text,
        "template": {
            "type": "buttons",
            # "thumbnailImageUrl": img_url,
            "imageAspectRatio": "rectangle",
            "imageSize": "cover",
            "imageBackgroundColor": "#FFFFFF",
            # "title": "メニュー",
            "text": template_text,
            # "defaultAction": {
            #     "type": "uri",
            #     "label": "View detail",
            #     "uri": base_url,
            # },
            "actions": actions,
        },
    }
    return json_object


if __name__ == const.MAIN_FUNCTION:
    get_channel_access_token()
