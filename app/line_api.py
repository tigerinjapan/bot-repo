# 説明：LINEメッセージAPI

import constants as const
import function as func
import function_api as func_api
import function_beautiful_soup as func_bs
import function_gemini as func_gemini
from message_constants import MSG_ERR_API_RESPONSE_NONE

# アプリケーション
app_nm = func.get_app_nm(__file__)

# URL
URL_LINE_API = "https://api.line.me"
URL_TENKI = "https://tenki.jp"
URL_NAVER_FINANCE = "https://finance.naver.com"
URL_KONEST = "https://www.konest.com"

# LINE API情報
LINE_CHANNEL_ID = func.get_env_val("LINE_CHANNEL_ID")
LINE_CHANNEL_SECRET = func.get_env_val("LINE_CHANNEL_SECRET")

# 改行
NEW_LINE = const.SYM_NEW_LINE

# メッセージタイプ
MSG_TYPE_TXT = "text"
MSG_TYPE_IMG = "image"

# ファイル区分
FILE_DIV_TODAY = "today"
FILE_DIV_NEWS = "news"
FILE_DIV_AI_NEWS = "ai_news"
LIST_FILE_DIV = [FILE_DIV_TODAY, FILE_DIV_NEWS, FILE_DIV_AI_NEWS]

# 定数（日本語）
STR_TODAY_JA = "■今日の"
DIV_WEATHER = "[天気] "
DIV_RATE = "[為替] "
STR_YEN_JA = "円"
STR_WON_JA = "ウォン"
DIV_OUTFIT = "[コーデ] "
DIV_DINNER = "[夕食] "
STR_NEWS_JA = "ニュース"
DIV_NEWS = f"{STR_TODAY_JA}ニュース"
STR_AI = "AI"
DIV_AI_NEWS = f"{STR_TODAY_JA}{STR_AI}{STR_NEWS_JA}"

# プロパティ
NUM_FONT_SIZE = 11
NUM_IMG_MAX_SEQ = 4
NUM_WRAP_WIDTH = 40


def main(msg_type: str = MSG_TYPE_IMG):

    func.print_start(app_nm)

    if LINE_CHANNEL_ID:
        # メッセージ取得
        if func.check_local_ip():
            msg_type = MSG_TYPE_TXT
        data = get_json_data_for_line(msg_type)

        # チャネル・アクセストークン取得
        token = get_channel_access_token()

        # メッセージ数チェック
        check_message_count(token)

        # メッセージ送信
        send_message(token, data)

    func.print_end(app_nm)


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
def check_message_count(access_token: str):
    url = f"{URL_LINE_API}/v2/bot/message/quota/consumption"
    headers = {"Content-Type": "application/json", "Authorization": access_token}
    response = func_api.get_response_result(url, headers=headers)
    result = func_api.get_loads_json(response.text)
    total_usage = result["totalUsage"]

    message_limit = 200
    message_count = f"{total_usage} / {message_limit}"
    func.print_info_msg(const.STR_MESSAGE_JA, message_count)


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
def get_json_data_for_line(msg_type: str):

    msg_list = get_msg_list(msg_type)

    messages = []

    if msg_type == MSG_TYPE_IMG:
        file_path_list = msg_list

        for img_url in file_path_list:
            json_object = {
                "type": msg_type,
                "originalContentUrl": img_url,
                "previewImageUrl": img_url,
            }

            messages.append(json_object)
    else:
        for msg in msg_list:
            json_object = {"type": msg_type, "text": msg}
            messages.append(json_object)

    data = {"messages": messages}
    json_data = func_api.get_dumps_json(data)

    if msg_type == MSG_TYPE_TXT:
        json_data = json_data.encode(const.CHARSET_ASCII)

    return json_data


# LINEメッセージ取得
def get_msg_list(msg_type: str) -> list[str]:

    today_info, forecast = get_today_info(msg_type)

    today_news = get_today_news()

    today_ai_news = get_today_ai_news()

    msg_list = [today_info, today_news, today_ai_news]

    if msg_type == MSG_TYPE_IMG:
        img_url_list = []
        for div, msg in zip(LIST_FILE_DIV, msg_list):
            img_url = create_msg_img(div, msg, forecast)
            img_url_list.append(img_url)

        msg_list = img_url_list

    return msg_list


# 今日の生活情報取得
def get_today_info(msg_type: str) -> tuple[str, str]:
    # タイトル
    today_title = get_today_title(msg_type)

    # 今日の天気
    today_weather, forecast = get_today_weather()

    # 今日のウォン
    today_won_rate = get_today_won()

    # 今日のコーデ・夕食
    recommend_outfit_dinner = func_gemini.get_recommend_outfit_dinner(
        NEW_LINE.join(today_weather)
    )

    today_outfit = [f"{DIV_OUTFIT} {recommend_outfit_dinner[0]}"]
    recommend_dinner = recommend_outfit_dinner[1].replace(NEW_LINE, const.SYM_BLANK)
    today_dinner = [f"{DIV_DINNER} {recommend_dinner}"]

    msg_list = today_title
    msg_list += today_weather
    msg_list += today_won_rate
    msg_list += today_outfit
    msg_list += today_dinner
    today_info = NEW_LINE.join(msg_list)
    return today_info, forecast


# タイトル取得
def get_today_title(msg_type: str = const.SYM_BLANK) -> list[str]:
    weekday = const.LIST_WEEKDAY[const.DATE_WEEKDAY]
    div_mark = "*-----*-----*-----*-----*"
    title = f"{const.DATE_TODAY_SLASH}({weekday})"
    title_text = f"*--- {title} ---*"
    title_img = f"==== {title} ===="

    if msg_type == MSG_TYPE_TXT:
        today_title = [div_mark, title_text, div_mark]
    elif msg_type == MSG_TYPE_IMG:
        today_title = [title_img]
    else:
        today_title = [title]

    return today_title


# 今日の天気情報取得
def get_today_weather() -> tuple[str, str]:
    # 東京の情報取得
    soup_result = func_bs.get_elem_from_url(
        URL_TENKI, "forecast-map-entry-13101", attr_div=const.ATTR_ID
    )

    forecast = get_elem_val_by_class(soup_result, "forecast-image")
    max_temp = get_elem_val_by_class(soup_result, "max-temp")
    min_temp = get_elem_val_by_class(soup_result, "min-temp")
    rain_prob = get_elem_val_by_class(soup_result, "prob-precip")

    weather_info = f"{DIV_WEATHER} {forecast}・{max_temp}/{min_temp}・{rain_prob}"
    today_weather = [weather_info]
    return today_weather, forecast


# 今日のウォン取得
def get_today_won() -> list[str]:
    url = (
        f"{URL_NAVER_FINANCE}/marketindex/exchangeDetail.naver?marketindexCd=FX_JPYKRW"
    )
    class_ = "tbl_calculator"
    today_won_rate = get_today_info_common(DIV_RATE, url, class_, const.TAG_TD)
    return today_won_rate


# 今日のニュース取得
def get_today_news() -> str:
    url = f"{URL_KONEST}/contents/news_top.html"
    class_ = "mArticleKonest"
    today_news = get_today_info_common(DIV_NEWS, url, class_, const.TAG_A)
    return today_news


# 今日のAIニュース取得
def get_today_ai_news() -> str:
    url = "https://www.itmedia.co.jp/ranking/"
    id = "rank-all"
    today_ai_news = get_today_info_common(
        DIV_AI_NEWS, url, id, const.TAG_A, attr_div=const.ATTR_ID
    )
    return today_ai_news


# 今日の情報取得
def get_today_info_common(
    div: str, url: str, attr_val: str, tag_div: str, attr_div: str = const.ATTR_CLASS
):
    elem_list = get_elem_list(url, attr_val, tag_div, attr_div)

    if div == DIV_RATE:
        won = elem_list[0].text
        info = f"{div} 100{STR_YEN_JA}={won}{STR_WON_JA}"
        today_info = [info]
    else:
        news_list = []
        news_no = 0

        if div == DIV_NEWS:
            for idx, a in enumerate(elem_list):
                if idx % 2 == 0:
                    continue

                a_href = a.get(const.ATTR_HREF)
                url_news = f"{URL_KONEST}/contents/{a_href}"
                a_title = a.get(const.ATTR_TITLE)

                if a_title and func.check_in_list(a_title, ["芸能", "旅行"]):
                    news_no += 1
                    news_contents = func_bs.get_elem_from_url(url_news, "size14")
                    news_result = f"[{news_no}] {news_contents}"
                    news_list.append(news_result)

        elif div == DIV_AI_NEWS:
            for a in elem_list:
                a_href = a.get(const.ATTR_HREF)
                a_text = a.text

                if STR_AI.upper() in a_text.upper():
                    news_no += 1
                    p_list = get_elem_list(
                        a_href, "cmsBody", const.TAG_P, const.ATTR_ID
                    )
                    news_contents_list = [p.text for p in p_list[0:-2]]
                    news_contents = NEW_LINE.join(news_contents_list)
                    news_result = f"[{news_no}] {news_contents}"
                    news_list.append(news_result)

        info = func_gemini.get_news_summary(news_list)
        news_info = [div, info]
        today_info = NEW_LINE.join(news_info)

    return today_info


# 要素リスト取得
def get_elem_list(
    url: str, attr_val: str, tag_div: str, attr_div: str = const.ATTR_CLASS
):
    elem = func_bs.get_elem_from_url(url, attr_val, attr_div)
    tag_list = func_bs.find_elem_list_by_attr(elem, tag_div)
    return tag_list


# 要素値取得
def get_elem_val_by_class(soup, class_: str) -> str:
    elem = func_bs.find_elem_by_attr(soup, class_, const.ATTR_CLASS)

    if class_ == "forecast-image":
        elem_val = elem.get(const.ATTR_ALT)
    else:
        elem_val = elem.text
    return elem_val


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

    img_file_nm = f"{img_div}_{img_no}"

    font_type = "meiryo.ttc"
    font_size = NUM_FONT_SIZE
    xy_size = (75, 185) if div == FILE_DIV_TODAY else (45, 90)

    file_path = func_api.insert_msg_to_img(
        div, img_file_nm, font_type, font_size, xy_size, msg
    )

    file_nm = func.get_app_nm(file_path)

    if func.check_local_ip():
        protocol = "http"
        host = const.IP_LOCAL_HOST
        port = const.PORT_NUM

    else:
        protocol = "https"
        host = const.IP_DEFAULT
        port = const.PORT_DEFAULT

    img_url = f"{protocol}://{host}:{port}/{const.STR_IMG}/{file_nm}"
    return img_url


if __name__ == const.MAIN_FUNCTION:
    msg_type = MSG_TYPE_IMG
    main(msg_type)
