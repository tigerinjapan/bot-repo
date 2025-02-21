# 説明：LINEメッセージAPI

import apps.news as news
import apps.today as today
import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_api as func_api
from apps.utils.message_constants import MSG_ERR_API_RESPONSE_NONE

# アプリケーション
app_name = func.get_app_name(__file__)

# URL
URL_LINE_API = "https://api.line.me"
URL_KOYEB = func.get_env_val("URL_KOYEB")

# LINE API情報
LINE_CHANNEL_ID = func.get_env_val("LINE_CHANNEL_ID")
LINE_CHANNEL_SECRET = func.get_env_val("LINE_CHANNEL_SECRET")
MAX_MESSAGE_CNT = 200

# 改行
NEW_LINE = const.SYM_NEW_LINE

# メッセージタイプ
MSG_TYPE_TXT = "text"
MSG_TYPE_IMG = "image"
LIST_MSG_TYPE = [MSG_TYPE_IMG]
LIST_MSG_TYPE_ALL = LIST_MSG_TYPE + [MSG_TYPE_TXT, MSG_TYPE_TXT]

# ファイル区分
FILE_DIV_TODAY = "today"
FILE_DIV_NEWS = "news"
FILE_DIV_AI_NEWS = "ai_news"
LIST_FILE_DIV = [FILE_DIV_TODAY]
LIST_FILE_DIV_ALL = LIST_FILE_DIV + [FILE_DIV_NEWS, FILE_DIV_AI_NEWS]

# タイトル
WEEKDAY_JA = const.LIST_WEEKDAY[const.DATE_WEEKDAY]
DIV_MARK = "*-----*-----*-----*-----*"
DIV_MARK_TXT = "*--- {} ---*"
DIV_MARK_IMG = "==== {} ===="

# プロパティ
NUM_FONT_SIZE = 11
NUM_IMG_MAX_SEQ = 4
WEEKLY_MSG = "金"


def main():

    func.print_start(app_name)

    if LINE_CHANNEL_ID:
        # チャネル・アクセストークン取得
        token = get_channel_access_token()

        # メッセージ数チェック
        use_cnt = check_message_count(token)

        if use_cnt <= (MAX_MESSAGE_CNT - 20):
            # メッセージ取得
            data = get_json_data()

            # メッセージ送信
            send_message(token, data)

    func.print_end(app_name)


# チャネル・アクセストークン取得
def get_channel_access_token() -> str:

    url = f"{URL_LINE_API}/oauth2/v3/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": LINE_CHANNEL_ID,
        "client_secret": LINE_CHANNEL_SECRET,
    }

    response = func_api.get_response_result(
        url, request_type=const.REQUEST_TYPE_POST, headers=headers, data=data
    ).text
    if not response:
        func.print_error_msg(const.STR_TOKEN_JA, MSG_ERR_API_RESPONSE_NONE)

    result = func_api.get_loads_json(response)

    # トークン・タイプ
    token_type = result["token_type"]

    # アクセストークン
    access_token = result["access_token"]

    # 有効期限（秒）
    expires_in = result["expires_in"]

    token = f"{token_type} {access_token}"

    expires_min = int(expires_in / 60)
    func.print_info_msg(const.STR_TOKEN_JA, f"{const.STR_EXPIRE_JA}：{expires_min}分")
    return token


# メッセージ件数取得
def check_message_count(access_token: str) -> int:
    url = f"{URL_LINE_API}/v2/bot/message/quota/consumption"
    headers = {"Content-Type": "application/json", "Authorization": access_token}
    response = func_api.get_response_result(url, headers=headers)
    result = func_api.get_loads_json(response.text)
    total_usage = result["totalUsage"]

    message_count = f"{total_usage} / {MAX_MESSAGE_CNT}"
    func.print_info_msg(const.STR_MESSAGE_JA, message_count)
    return total_usage


# メッセージ送信
def send_message(access_token: str, json_data):
    url = f"{URL_LINE_API}/v2/bot/message/broadcast"
    headers = {"Content-Type": "application/json", "Authorization": access_token}

    response = func_api.get_response_result(
        url, request_type=const.REQUEST_TYPE_POST, headers=headers, data=json_data
    )

    result = func_api.get_loads_json(response.text)
    if result:
        err_msg = [response.status_code, response.reason, result["message"]]
        func.print_error_msg(const.STR_LINE_API, err_msg)


# LINE送信用のJSONデータ取得
def get_json_data():
    messages = []

    msg_list, forecast = get_msg_list()
    for msg_type, msg_div, msg_data in msg_list:
        json_object = {"type": msg_type}

        text_title = get_title(msg_div, msg_type)
        text_msg = text_title + const.SYM_NEW_LINE + NEW_LINE.join(msg_data)

        if msg_type == MSG_TYPE_IMG:
            img_url = create_msg_img(msg_div, text_msg, forecast)
            update_data = {"originalContentUrl": img_url, "previewImageUrl": img_url}

        else:
            update_data = {"text": text_msg}

        info_msg = [msg_type, msg_div]
        func.print_info_msg(const.STR_MESSAGE_JA, info_msg)

        json_object.update(update_data)
        messages.append(json_object)

    data = {"messages": messages}
    json_data = func_api.get_dumps_json(data)
    json_data = json_data.encode(const.CHARSET_ASCII)
    return json_data


# メッセージ取得
def get_msg_list() -> list[str]:

    msg_type_list = LIST_MSG_TYPE
    file_div_list = LIST_FILE_DIV

    today_info, forecast = today.get_today_info()
    today_info_list = [f"[{div}] {info}" for div, info in today_info]
    msg_list = [today_info_list]

    if WEEKDAY_JA == WEEKLY_MSG:
        msg_type_list = LIST_MSG_TYPE_ALL
        file_div_list = LIST_FILE_DIV_ALL

        news_msg = news.get_news_msg_list(news.DIV_NEWS_LIST)
        korea_news_msg = news.get_news_msg_list(news.DIV_KOREA_NEWS_LIST)
        msg_list += [korea_news_msg, news_msg]

    data_list = zip(msg_type_list, file_div_list, msg_list)
    return data_list, forecast


# タイトル取得
def get_title(div: str, msg_type: str = const.SYM_BLANK) -> list[str]:
    title_div = f"{const.DATE_TODAY_SLASH}({WEEKDAY_JA})"
    if div == FILE_DIV_NEWS:
        title_div = news.DIV_NEWS.format(const.SYM_BLANK)
    elif div == FILE_DIV_AI_NEWS:
        title_div = news.DIV_AI_NEWS

    title_txt = DIV_MARK_TXT.format(title_div)
    title_img = DIV_MARK_IMG.format(title_div)

    if msg_type == MSG_TYPE_TXT:
        title_list = [DIV_MARK, title_txt, DIV_MARK]
        title = NEW_LINE.join(title_list)
    elif msg_type == MSG_TYPE_IMG:
        title = title_img
    else:
        title = title_div

    return title


# 画像に文字列挿入
def create_msg_img(div: str, msg: str, forecast: str) -> str:

    if div == FILE_DIV_TODAY:
        if "晴" in forecast:
            img_div = "sunny"
        elif "曇" in forecast:
            img_div = "cloudy"
        elif "雨" in forecast:
            img_div = "rainy"
        elif "雪" in forecast:
            img_div = "snowy"
        else:
            img_div = "sunny"
    else:
        img_div = FILE_DIV_NEWS

    # 任意の数値取得
    img_no = str(func.get_random_int(NUM_IMG_MAX_SEQ))
    img_no = img_no.zfill(3)

    img_file_org = f"{img_div}_{img_no}"

    font_type = "meiryo.ttc"
    font_size = NUM_FONT_SIZE
    xy_size = (75, 185) if div == FILE_DIV_TODAY else (45, 90)

    file_path = func_api.insert_msg_to_img(
        div, img_file_org, font_type, font_size, xy_size, msg
    )

    img_file_name = func.get_app_name(file_path)
    if not func.check_local_ip:
        func.print_info_msg(MSG_TYPE_IMG, img_url)

    img_url = f"https://{URL_KOYEB}/{const.STR_IMG}/{img_file_name}"
    return img_url


if __name__ == const.MAIN_FUNCTION:
    get_json_data()
