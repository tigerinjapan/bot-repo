"""
今日の生活情報
"""

import sys

import apps.ex as ex
import apps.today as today
import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_api as func_api
import apps.utils.function_beautiful_soup as func_bs
import apps.utils.function_gemini as func_gemini
import apps.utils.function_kakao as func_kakao

# スクリプト名
SCRIPT_NAME = func.get_app_name(__file__)

TITLE_LINK = "✈ 최저가 항공권 정보 ✈"

# 定数（韓国語）
DIV_TITLE = "📢 {} 오늘의 뉴스 📢"
DIV_UPDATE_TIME = "업데이트일시"
DIV_WEATHER = "날씨"
DIV_STOCK = "해외증시"
DIV_RATE = "환율"
DIV_JAPANESE = "일본어"
DIV_ENGLISH = "영어"
DIV_FLIGHT = "항공권"
DIV_LIST = [
    DIV_UPDATE_TIME,
    DIV_WEATHER,
    DIV_STOCK,
    DIV_RATE,
    DIV_JAPANESE,
    DIV_ENGLISH,
    DIV_FLIGHT,
]

LIST_CITY_KOR = ["서울", "인천", "대구"]
LIST_CITY_JPN = ["도쿄", "후쿠오카", "오사카", "나고야", "오키나와"]

# キーワードリスト
LIST_KEYWORD_AI = func.get_input_data(const.STR_KEYWORD, const.STR_AI)

# URL
URL_FLIGHT = "https://www.ttang.com"
URL_FLIGHT_MO = "https://mm.ttang.com"
URL_FLIGHT_PARAM = "/product/free/index.do"
URL_LINK = f"{URL_FLIGHT}{URL_FLIGHT_PARAM}"
URL_LINK_MO = f"{URL_FLIGHT_MO}{URL_FLIGHT_PARAM}"
URL_NAVER_RANKING_NEWS = "https://news.naver.com/main/ranking/popularDay.naver"
URL_NAVER_RANKING_NEWS_MO = "https://m.news.naver.com/rankingList"

# 天気
weather_news_link = "https://www.weather.go.kr/w/weather/forecast/short-term.do"

# S&P500
stock_link = f"{const.URL_NAVER_STOCK_MO}/worldstock/"

# 為替
finance_link = f"{const.URL_NAVER_STOCK_MO}/marketindex/home/exchangeRate/exchange"

# 日本語
japanese_link = "https://ja.dict.naver.com/#/main"

# 英語
english_link = "https://learn.dict.naver.com/conversation#/"

# 航空券セール
flight_sale_link = URL_LINK_MO

# タイトル
app_title = "Today's News"

# カラムリスト
col_list = ["구분", "오늘의 생활정보", "링크"]


def get_item_list():
    """
    アイテムリスト取得
    """
    today_info_list = get_today_info_list()
    info_list = today_info_list[0]
    link_list = today_info_list[1]
    today_info = zip(DIV_LIST, info_list, link_list)
    item_list = [[div, info, link] for div, info, link in today_info if info]
    return item_list


def get_today_info(object_type: str = func_kakao.OBJECT_TYPE_FEED):
    """
    今日の生活情報取得
    """
    json_data = func_api.get_json_data_on_app(const.APP_TODAY_KOREA)

    date_time_text = json_data[0].get(col_list[1])
    today_date = func.convert_date_format(
        date_time_text, const.DATE_FORMAT_YYYYMMDD_KO, const.DATE_FORMAT_YYYYMMDD_HHMM
    )
    title = DIV_TITLE.format(today_date)
    if object_type == func_kakao.OBJECT_TYPE_FEED:
        title = title.replace("📢", "■")

    data_list = [list(info.values()) for info in json_data[1:]]
    today_info_list = [f"[{data[0]}] {data[1]}" for data in data_list if data[1]]
    today_info_list.insert(0, title)
    today_info = const.SYM_NEW_LINE.join(today_info_list)

    file_path = const.SYM_BLANK
    if object_type == func_kakao.OBJECT_TYPE_FEED:
        file_path = get_news_image(today_info)
    return today_info, file_path


def get_news_image(today_info: str) -> str:
    """
    ニュースイメージ取得
    """
    forecast = get_forecast()
    outfit = get_outfit()

    file_path = func_gemini.get_today_news_image(
        today_info, forecast, outfit, const.APP_TODAY_KOREA
    )
    return file_path


def get_today_info_list():
    """
    今日の生活情報取得
    """
    curr_func_nm = sys._getframe().f_code.co_name

    # 更新日時
    update_time = func.get_now(const.DATE_TODAY, const.DATE_FORMAT_YYYYMMDD_HHMM)

    today_info_list = [update_time]
    today_link_list = [const.SYM_DASH]

    tasks = [
        get_today_weather_news,
        get_stock,
        get_won,
        get_japanese_study,
        get_english_conversation,
        get_flight_sale,
    ]

    link_list = [
        weather_news_link,
        stock_link,
        finance_link,
        japanese_link,
        english_link,
        flight_sale_link,
    ]

    for idx, (task, link) in enumerate(zip(tasks, link_list)):
        div = DIV_LIST[idx + 1]

        try:
            info = task()
            if info:
                today_info_list.append(info)
                today_link_list.append(link)

        except Exception as e:
            func.print_error_msg(SCRIPT_NAME, curr_func_nm, div, e)

    return today_info_list, today_link_list


def get_today_weather_news() -> str:
    """
    天気ニュース取得
    """
    title = const.SYM_BLANK

    today = func.get_now(const.DATE_TODAY)
    url = f"https://media.naver.com/press/214/ranking?type=section&date={today}"

    soup = func_bs.get_elem_from_url(
        url, attr_val="press_ranking_box is_section", list_flg=const.FLG_ON
    )[3]
    # link = func_bs.get_link_from_soup(soup)

    title_elem_list = func_bs.find_elem_by_class(
        soup, "list_title", list_flg=const.FLG_ON
    )
    split_str = "‥"

    for title_elem in title_elem_list:
        title_text = title_elem.text
        if DIV_WEATHER in title_text:
            title = title_text.replace("[날씨] ", const.SYM_BLANK)
            if split_str in title:
                title = title.split(split_str)[0]
            break

    if not title:
        title = title_elem_list[0].text

    return title


def get_forecast() -> str:
    """
    天気予報取得
    """
    url = f"{const.URL_TENKI}/world/5/89/47108/"
    soup = func_bs.get_elem_from_url(
        url, attr_val="weather-image", list_flg=const.FLG_ON
    )[1]
    forecast = func_bs.get_text_from_soup(soup)
    return forecast


def get_stock() -> str:
    """
    S&P500
    """
    url = f"{const.URL_NAVER_FINANCE}/world/sise.naver?symbol=SPI@SPX"
    soup = func_bs.get_elem_from_url(url, attr_val="today")
    today_elem = func_bs.find_elem_by_class(soup, "no_today")
    exday_elem = func_bs.find_elem_by_class(soup, "no_exday")
    today_no = func_bs.get_text_from_soup(today_elem)
    exday_no = func_bs.get_text_from_soup(exday_elem)
    exday_no = func.re_search(r"\(.+?\)", exday_no)
    stock_info = f"{const.FUND_NAME_SP_500} {today_no} {exday_no}"
    return stock_info


def get_won() -> str:
    """
    ウォン取得
    """
    today_won = ex.get_today_won(const.FLG_ON)
    return today_won


def get_outfit() -> str:
    """
    コーデ取得
    """
    today_outfit = today.get_today_outfit()
    outfit = today_outfit.split(const.SYM_NEW_LINE)[0].split(const.SYM_PERIOD)[:2]
    return outfit[:20]


def get_flight_sale() -> str:
    """
    航空券セール情報取得
    """
    flight_sale = const.SYM_BLANK

    url = f"{URL_FLIGHT}/product/free/subIndex.do?majorCategoryCd=C003"
    soup = func_bs.get_elem_from_url(url, attr_val="tblListB noBd line2")

    item_list = func_bs.find_elem_by_attr(
        soup, tag=const.TAG_TR, list_flg=const.FLG_ON
    )[1:5]
    for item in item_list:
        info_list = func_bs.find_elem_by_class(item, "shortCut", list_flg=const.FLG_ON)
        price_info = func_bs.find_elem_by_class(item, "js_tooltip_btn").text
        target_list = [const.SYM_COMMA, "원"]
        price = func.get_replace_data(price_info, target_list)

        from_ = info_list[0].text
        to = info_list[2].text.split(const.SYM_SLASH)[0]
        airline = info_list[3].text.replace("항공", const.SYM_BLANK)
        link_info = info_list[4]
        # dd_id = link_info.get("ddid")
        # p_num = link_info.get("pnum")
        # link = f"{URL_FLIGHT}/common/free/getGoodsInfo.do?ddId={dd_id}&pnum={p_num}"

        if from_ in LIST_CITY_KOR and to in LIST_CITY_JPN and int(price) < 300000:
            flight_sale = f"{from_}↔️{to} {price_info}"
            break

    return flight_sale


def get_japanese_study() -> str:
    """
    日本語取得
    """
    japanese_study = const.SYM_BLANK

    url = "https://wquiz.dict.naver.com/jakodict/today/quiz.dict#tab=1"
    soup = func_bs.get_elem_from_url(url, attr_val="todayword_quiz _primary_quiz")

    quiz_word = func_bs.find_elem_by_class(soup, "quiz_word_text").text
    answer_elem_list = func_bs.find_elem_by_class(
        soup, "multiple_answer_item _primary_answer_item", list_flg=const.FLG_ON
    )

    for answer_elem in answer_elem_list:
        if answer_elem.get("data-correct") == "1":
            answer = func_bs.get_text_from_soup(answer_elem)

            japanese = quiz_word
            korean = answer
            if answer_elem.get("lang") == const.LANG_CD_JA:
                japanese = answer
                korean = quiz_word

            split_str = const.SYM_SEMI_COLON
            if 20 <= len(korean) and split_str in korean:
                korean = korean.split(split_str)[0].replace(
                    const.SYM_DOT, const.SYM_BLANK
                )

            japanese_study = f"{japanese}{const.SYM_NEW_LINE}{korean}"
            break

    return japanese_study


def get_english_conversation() -> str:
    """
    英会話取得
    """
    data = today.get_today_phrase(const.STR_ENGLISH)
    english_conversation = f"{data[1]}{const.SYM_NEW_LINE}{data[2]}"
    return english_conversation


def get_phrase() -> str:
    """
    今日の一言取得
    """
    phrase = today.get_today_phrase(const.STR_PHRASE_KO)
    return phrase


def get_it_news() -> str:
    """
    ITニュース取得
    """
    news_list = []

    URL_ET_NEWS = "https://m.etnews.com"
    url = f"{URL_ET_NEWS}/news/section.html?id1=03"
    contents_list = func_bs.get_elem_from_url(
        url, const.TAG_DIV, attr_val="text", list_flg=const.FLG_ON
    )
    if contents_list:
        for contents in contents_list:
            a_elem = func_bs.find_elem_by_attr(contents, tag=const.TAG_A)
            a_text = a_elem.text
            a_href = a_elem.get(const.ATTR_HREF)
            if func.check_in_list(a_text, LIST_KEYWORD_AI):
                news_list.append(a_text)
                news_list.append(f"{URL_ET_NEWS}{a_href}")
                if 6 <= len(news_list):
                    break

    it_news = const.SYM_NEW_LINE.join(news_list)
    return it_news


if __name__ == const.MAIN_FUNCTION:
    # get_today_info_list()
    # get_today_info()
    get_it_news()
