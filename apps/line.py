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
URL_KOYEB_APP = "https://" + func.get_env_val("URL_KOYEB")

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

# ファイル区分
FILE_DIV_TODAY = "today"
FILE_DIV_NEWS = "news"
FILE_DIV_AI_NEWS = "ai_news"

# タイトル
DIV_MARK = "*----*----*----*----*----*"
DIV_MARK_TXT = "*-- {} --*"
DIV_MARK_IMG = "=== {} ==="

# プロパティ
LINE_IMG_DIV = func.get_env_val("LINE_IMG_DIV")
IMG_DIV_0 = str(const.NUM_ZERO)
IMG_DIV_1 = str(const.NUM_ONE)
IMG_DIV_2 = str(const.NUM_TWO)
NUM_IMG_MAX_SEQ = 4
FONT_TYPE = "msgothic"  # meiryo
WEEKLY_DIV_FRI = "Fri"


def main(auto_flg: bool = const.FLG_ON, data_flg: bool = const.FLG_ON):

    func.print_start(app_name)

    if LINE_CHANNEL_ID:
        # チャネル・アクセストークン取得
        token = get_channel_access_token()

        # メッセージ数チェック
        use_cnt = check_message_count(token)

        if use_cnt <= (MAX_MSG_API_CNT - 20):
            if data_flg:
                msg_list = get_msg_list(auto_flg)

                # メッセージ取得
                data = get_json_for_line(msg_list)
            else:
                data = get_json_data_for_line()

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
    )
    if not response:
        func.print_error_msg(const.STR_TOKEN_JA, MSG_ERR_API_RESPONSE_NONE)
        return const.SYM_BLANK

    result = func.get_loads_json(response.text)

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
    if response:
        result = func.get_loads_json(response.text)
        total_usage = result["totalUsage"]
    else:
        total_usage = MAX_MSG_API_CNT

    message_count = f"{total_usage} / {MAX_MSG_API_CNT}"
    func.print_info_msg(const.STR_MESSAGE_JA, message_count)
    return total_usage


# メッセージ送信
def send_message(access_token: str, json_data):
    url = f"{URL_LINE_API}/v2/bot/message/broadcast"
    headers = {"Content-Type": "application/json", "Authorization": access_token}

    response = func_api.get_response_result(
        url, request_type=const.REQUEST_TYPE_POST, headers=headers, data=json_data
    )

    if response.text:
        result = func.get_loads_json(response.text)
        if result:
            err_msg = f"[{response.status_code}, {response.reason}], {result}"
            func.print_error_msg(STR_LINE_API, err_msg)


# LINE送信用のJSONデータ取得
def get_json_for_line(msg_list: list[list[str]]):
    messages = []

    for msg_data in msg_list:
        msg_type = msg_data[0]
        text_msg = msg_data[1]
        json_object = {"type": msg_type}

        if msg_type == MSG_TYPE_IMG:
            img_url = text_msg
            update_data = {"originalContentUrl": img_url, "previewImageUrl": img_url}
        else:
            update_data = {"text": text_msg}

        json_object.update(update_data)
        messages.append(json_object)

    data = {"messages": messages}
    json_data = func.get_dumps_json(data)
    return json_data


# メッセージリスト取得
def get_msg_list(auto_flg: bool = const.FLG_ON) -> list[list[str]]:

    if auto_flg:
        today_info, forecast, date_today = today.get_today_info()
        msg_data = [f"[{div}] {info}" for div, info in today_info]

        msg_data_list = get_msg_data_list(
            FILE_DIV_TODAY, MSG_TYPE_IMG, msg_data, date_today, forecast
        )
    else:
        msg_div = const.STR_NOTIFY
        msg_data = func.get_input_data(const.STR_MESSAGE, msg_div)
        msg_data_list = get_msg_data_list(msg_div, MSG_TYPE_TXT, msg_data)

    msg_list = [msg_data_list]

    if auto_flg and WEEKLY_DIV_FRI in date_today:
        ai_news_msg = news.get_news_msg_list(news.DIV_AI_NEWS_LIST)
        msg_data_list = get_msg_data_list(
            FILE_DIV_AI_NEWS, MSG_TYPE_TXT, ai_news_msg, date_today
        )
        msg_list.append(msg_data_list)

    return msg_list


# LINEメッセージJSONデータ取得
def get_json_data_for_line():
    messages = []
    json_object = get_json_object()
    messages.append(json_object)
    data = {"messages": messages}
    json_data = func.get_dumps_json(data)
    return json_data


# JSONオブジェクト取得
def get_json_object(msg_type: str = const.SYM_BLANK):
    json_object = get_template_msg()
    # if msg_type == MSG_TYPE_TMP:
    #     json_object = get_template_msg()
    return json_object


# テンプレート・メッセージ取得
def get_template_msg():
    base_url = "https://kobe-dev.koyeb.app"
    img_url = base_url + "/img/test"

    json_object = {
        "type": MSG_TYPE_TMP,
        "altText": "LINEテスト：テンプレート・メッセージ",
        "template": {
            "type": "buttons",
            "thumbnailImageUrl": img_url,
            "imageAspectRatio": "rectangle",
            "imageSize": "cover",
            "imageBackgroundColor": "#FFFFFF",
            "title": "メニュー",
            "text": "ボタン選択してください。",
            "defaultAction": {
                "type": "uri",
                "label": "View detail",
                "uri": base_url,
            },
            "actions": [
                {
                    "type": "uri",
                    "label": "今日の生活情報",
                    "uri": f"{base_url}/json/today",
                },
                {
                    "type": "uri",
                    "label": "LCCニュース",
                    "uri": f"{base_url}/json/lcc",
                },
            ],
        },
    }
    return json_object


# メッセージ取得
def get_msg_data_list(
    msg_div: str,
    msg_type: str,
    msg_data: list[str],
    date_today: str = const.SYM_BLANK,
    forecast: str = const.SYM_BLANK,
) -> list[str]:
    text_title = get_title(msg_div, date_today, msg_type)
    text_msg = text_title + const.SYM_NEW_LINE + NEW_LINE.join(msg_data)

    if msg_type == MSG_TYPE_IMG:
        text_msg = create_msg_img(msg_div, text_msg, forecast)
    msg_data_list = [msg_type, text_msg]
    return msg_data_list


# タイトル取得
def get_title(div: str, date_today: str, msg_type: str = const.SYM_BLANK) -> str:
    title_div = date_today

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
        if "雨" in forecast:
            img_div = "rainy"
        elif "雪" in forecast:
            img_div = "snowy"
        elif "曇" in forecast:
            img_div = "cloudy"
        else:
            img_div = "sunny"
    else:
        img_div = FILE_DIV_NEWS

    # 任意の数値取得
    img_seq = str(func.get_random_int(NUM_IMG_MAX_SEQ))
    img_no = LINE_IMG_DIV + img_seq.zfill(2)

    img_file_base = f"{img_div}_{img_no}"

    font_type = FONT_TYPE
    font_size = 11
    xy_size = (45, 90)
    if div == FILE_DIV_TODAY:
        xy_size = (75, 185)
        if LINE_IMG_DIV == IMG_DIV_1:
            font_size = 15
            xy_size = (60, 120)

    file_path = func_api.insert_msg_to_img(
        div, img_file_base, font_type, font_size, xy_size, msg
    )

    img_file_name = func.get_app_name(file_path)
    img_url = f"{URL_KOYEB_APP}/{const.STR_IMG}/{img_file_name}"
    if func.is_local_env():
        img_url = file_path
    func.print_info_msg(MSG_TYPE_IMG, img_url)
    return img_url


if __name__ == const.MAIN_FUNCTION:
    msg_list = get_msg_list()
    # func.print_test_data(msg_list)
    # main(auto_flg=const.FLG_OFF)
    # main(data_flg=const.FLG_OFF)
