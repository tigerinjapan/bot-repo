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
URL_KSTYLE = "https://kstyle.com"

# LINE API情報
LINE_CHANNEL_ID = func.get_env_val("LINE_CHANNEL_ID")
LINE_CHANNEL_SECRET = func.get_env_val("LINE_CHANNEL_SECRET")
URL_KOYEB = func.get_env_val("URL_KOYEB")
MAX_MESSAGE_CNT = 200

# 改行
NEW_LINE = const.SYM_NEW_LINE

# メッセージタイプ
MSG_TYPE_TXT = "text"
MSG_TYPE_IMG = "image"

# ファイル区分
FILE_DIV_TODAY = "today"
FILE_DIV_NEWS = "news"
FILE_DIV_AI_NEWS = "ai_news"
LIST_FILE_DIV = [FILE_DIV_TODAY, FILE_DIV_NEWS]
LIST_FILE_DIV_ALL = LIST_FILE_DIV + [FILE_DIV_AI_NEWS]
LIST_MSG_TYPE = [MSG_TYPE_IMG, MSG_TYPE_TXT]
LIST_MSG_TYPE_ALL = LIST_MSG_TYPE + [MSG_TYPE_IMG]
LIST_KEYWORD_AI = ["AI", "OpenAI", "ChatGPT", "Gemini"]

# タイトル
WEEKDAY_JA = const.LIST_WEEKDAY[const.DATE_WEEKDAY]
DIV_MARK = "*-----*-----*-----*-----*"
DIV_MARK_TXT = "*--- {} ---*"
DIV_MARK_IMG = "==== {} ===="

# 定数（日本語）
DIV_WEATHER = "[天気] "
DIV_RATE = "[為替] "
STR_YEN_JA = "円"
STR_WON_JA = "ウォン"
DIV_OUTFIT = "[コーデ] "
DIV_DINNER = "[夕食] "
STR_TODAY_JA = "今日の"
STR_NEWS_JA = "ニュース"
STR_ENT_JA = "エンタメ"
STR_AI = "AI"

DIV_NEWS = STR_TODAY_JA + STR_NEWS_JA
DIV_ENT_NEWS = STR_TODAY_JA + f"{STR_ENT_JA}{STR_NEWS_JA}"
DIV_AI_NEWS = STR_TODAY_JA + f"{STR_AI}{STR_NEWS_JA}"

# プロパティ
NUM_FONT_SIZE = 11
NUM_IMG_MAX_SEQ = 4
WEEKDAY_IT_NEWS = "金"


def main():

    func.print_start(app_nm)

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

        text_data = get_title(msg_div, msg_type) + msg_data
        text_msg = const.SYM_NEW_LINE.join(text_data)

        if msg_type == MSG_TYPE_IMG:
            img_url = create_msg_img(msg_div, text_msg, forecast)
            update_data = {"originalContentUrl": img_url, "previewImageUrl": img_url}

        else:
            update_data = {"text": text_msg}

        info_msg = [msg_type, msg_div, text_msg]
        func.print_info_msg(const.STR_MESSAGE_JA, info_msg)

        json_object.update(update_data)
        messages.append(json_object)

    data = {"messages": messages}
    json_data = func_api.get_dumps_json(data)
    json_data = json_data.encode(const.CHARSET_ASCII)
    return json_data


# LINEメッセージ取得
def get_msg_list() -> list[str]:

    msg_type_list = LIST_MSG_TYPE
    file_div_list = LIST_FILE_DIV

    today_info, forecast = get_today_info()
    # today_news = get_today_news()
    today_news = get_today_ent_news()
    msg_list = [today_info, today_news]

    if WEEKDAY_JA == WEEKDAY_IT_NEWS:
        msg_type_list = LIST_MSG_TYPE_ALL
        file_div_list = LIST_FILE_DIV_ALL

        today_ai_news = get_today_ai_news()
        msg_list += [today_ai_news]

    data_list = zip(msg_type_list, file_div_list, msg_list)
    return data_list, forecast


# 今日の生活情報取得
def get_today_info() -> tuple[list[str], str]:
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

    today_info = today_weather
    today_info += today_won_rate
    today_info += today_outfit + today_dinner
    return today_info, forecast


# タイトル取得
def get_title(div: str, msg_type: str = const.SYM_BLANK) -> list[str]:
    title_div = f"{const.DATE_TODAY_SLASH}({WEEKDAY_JA})"
    if div == FILE_DIV_NEWS:
        title_div = DIV_NEWS
    elif div == FILE_DIV_AI_NEWS:
        title_div = DIV_AI_NEWS

    title_txt = DIV_MARK_TXT.format(title_div)
    title_img = DIV_MARK_IMG.format(title_div)

    if msg_type == MSG_TYPE_TXT:
        title = [DIV_MARK, title_txt, DIV_MARK]
    elif msg_type == MSG_TYPE_IMG:
        title = [title_img]
    else:
        title = [title_div]

    return title


# 今日の天気情報取得
def get_today_weather() -> tuple[list[str], str]:
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
def get_today_news() -> list[str]:
    url = f"{URL_KONEST}/contents/news_top.html"
    class_ = "mArticleKonest"
    today_news = get_today_info_common(DIV_NEWS, url, class_, const.TAG_A)
    return today_news


# 今日のニュース取得
def get_today_ent_news() -> list[str]:
    url = f"{URL_KSTYLE}/ranking.ksn"
    class_ = "ArticleRankingCard_heading__Xxney"
    today_ent_news = get_today_info_common(DIV_ENT_NEWS, url, class_, const.TAG_A)
    return today_ent_news


# 今日のAIニュース取得
def get_today_ai_news() -> list[str]:
    url = "https://www.itmedia.co.jp/ranking/"
    id = "rank-all"
    today_ai_news = get_today_info_common(
        DIV_AI_NEWS, url, id, const.TAG_A, attr_div=const.ATTR_ID
    )
    return today_ai_news


# 今日の情報取得
def get_today_info_common(
    div: str,
    url: str,
    attr_val: str,
    tag_div: str,
    attr_div: str = const.ATTR_CLASS,
) -> list[str]:

    elem_list = get_elem_list(url, attr_val, tag_div, attr_div)

    if div == DIV_RATE:
        won = elem_list[0].text
        info = f"{div} 100{STR_YEN_JA}={won}{STR_WON_JA}"

    else:
        news_list = []
        news_no = 0

        if div == DIV_ENT_NEWS:
            for a in elem_list:
                news_no += 1

                a_href = a.get(const.ATTR_HREF)
                a_text = func.get_replace_data(a.text)
                news_text_list = a_text.split("…")
                news_text = NEW_LINE.join(news_text_list)
                news_result = f"[{news_no}] {news_text}"
                news_list.append(news_result)

                if news_no == 1:
                    url_content = f"{URL_KSTYLE}/{a_href}"
                    news_list.append(url_content)

            info = NEW_LINE.join(news_list)

        elif div == DIV_NEWS:
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

            info = func_gemini.get_news_summary(news_list)

        elif div == DIV_AI_NEWS:
            for a in elem_list:
                a_href = a.get(const.ATTR_HREF)
                a_text = a.text

                if func.check_in_list(a_text, LIST_KEYWORD_AI):
                    news_no += 1
                    p_list = get_elem_list(
                        a_href, "cmsBody", const.TAG_P, const.ATTR_ID
                    )
                    news_contents_list = [p.text for p in p_list[0:-2]]
                    news_contents = NEW_LINE.join(news_contents_list)
                    news_result = f"[{news_no}] {news_contents}"
                    news_list.append(news_result)

            info = func_gemini.get_news_summary(news_list)

    today_info = [info]
    return today_info


# 要素リスト取得
def get_elem_list(
    url: str,
    attr_val: str,
    tag_div,
    attr_div: str = const.ATTR_CLASS,
):
    if URL_KSTYLE in url:
        elem_list = func_bs.get_elem_list_from_url(url, attr_val)
        elem_list = [func_bs.find_elem_by_attr(elem, tag_div) for elem in elem_list]

    else:
        elem = func_bs.get_elem_from_url(url, attr_val, attr_div)
        elem_list = func_bs.find_elem_list_by_attr(elem, tag_div)

    return elem_list


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

    img_file_org = f"{img_div}_{img_no}"

    font_type = "meiryo.ttc"
    font_size = NUM_FONT_SIZE
    xy_size = (75, 185) if div == FILE_DIV_TODAY else (45, 90)

    file_path = func_api.insert_msg_to_img(
        div, img_file_org, font_type, font_size, xy_size, msg
    )

    img_file_nm = func.get_app_nm(file_path, extension_flg=const.FLG_OFF)
    if not func.check_local_ip:
        func.print_info_msg(MSG_TYPE_IMG, img_url)

    img_url = f"https://{URL_KOYEB}/{const.STR_IMG}/{img_file_nm}"
    return img_url


if __name__ == const.MAIN_FUNCTION:
    get_json_data()
