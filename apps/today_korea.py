# 説明: 今日の生活情報

import apps.ex as ex
import apps.today as today
import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_api as func_api
import apps.utils.function_beautiful_soup as func_bs
import apps.utils.function_gemini as func_gemini
import apps.utils.function_kakao as func_kakao

# 定数（韓国語）
DIV_TITLE = "📢 {} 오늘의 뉴스 📢"
DIV_UPDATE_TIME = "업데이트일시"
DIV_WEATHER = "날씨"
DIV_RATE = "환율"
DIV_JAPANESE = "일본어"
DIV_ENGLISH = "영어"
DIV_FLIGHT = "항공권"
DIV_LIST = [
    DIV_UPDATE_TIME,
    DIV_WEATHER,
    DIV_RATE,
    DIV_JAPANESE,
    DIV_ENGLISH,
    DIV_FLIGHT,
]

LIST_CITY_KOR = ["서울", "인천", "대구"]
LIST_CITY_JPN = ["도쿄", "후쿠오카", "오사카", "나고야", "오키나와"]

# URL
URL_FLIGHT = "https://www.ttang.com"
URL_FLIGHT_MO = "https://mm.ttang.com"
URL_FLIGHT_PARAM = "/product/free/index.do"
URL_LINK = f"{URL_FLIGHT}{URL_FLIGHT_PARAM}"
URL_LINK_MO = f"{URL_FLIGHT_MO}{URL_FLIGHT_PARAM}"
URL_NAVER_RANKING_NEWS = "https://news.naver.com/main/ranking/popularDay.naver"
URL_NAVER_RANKING_NEWS_MO = "https://m.news.naver.com/rankingList"

TITLE_LINK = "✈ 최저가 항공권 정보 ✈"

# タイトル
app_title = "Today's News"

# カラムリスト
col_list = ["구분", "오늘의 생활정보", "링크"]


# アイテムリスト取得
def get_item_list():
    today_info_list = get_today_info_list()
    info_list = today_info_list[0]
    link_list = today_info_list[1]
    today_info = zip(DIV_LIST, info_list, link_list)
    item_list = [[div, info, link] for div, info, link in today_info if info]
    return item_list


# 今日の生活情報取得
def get_today_info(object_type: str = func_kakao.OBJECT_TYPE_FEED):
    # タイトル
    today_date = func.convert_date_to_str(func.get_now(), const.DATE_FORMAT_YYYYMMDD_KO)
    title = DIV_TITLE.format(today_date)
    if object_type == func_kakao.OBJECT_TYPE_FEED:
        title = title.replace("📢", "■")

    json_data = func_api.get_result_on_app(const.APP_TODAY_KOREA)[1:]
    data_list = [list(info.values()) for info in json_data]
    today_info_list = [
        f"[{data[0]}]{const.SYM_NEW_LINE}{data[1]}" for data in data_list if data[1]
    ]
    today_info_list.insert(0, title)
    today_info = const.SYM_NEW_LINE.join(today_info_list)

    file_path = const.SYM_BLANK
    if object_type == func_kakao.OBJECT_TYPE_FEED:
        file_path = get_news_image(today_info)
    return today_info, file_path


# ニュースイメージ取得
def get_news_image(today_info: str) -> str:
    forecast = get_forecast()
    outfit = get_outfit()

    file_path = func_gemini.get_today_news_image(
        today_info, forecast, outfit, const.APP_TODAY_KOREA
    )
    return file_path


# 今日の生活情報取得
def get_today_info_list():
    # 更新日時
    update_time = func.convert_date_to_str(
        func.get_now(), const.DATE_FORMAT_YYYYMMDD_HHMM
    )

    # 天気
    weather_news = get_today_weather_news()
    weather_news_link = "https://www.weather.go.kr/w/weather/forecast/short-term.do"

    # 為替
    yen_to_won = ex.get_today_won(const.FLG_ON)
    finance_link = f"{const.URL_NAVER_FINANCE}/marketindex/"

    # 日本語
    japanese = get_japanese_study()
    japanese_link = "https://ja.dict.naver.com/#/main"

    # 英語
    english_conversation = get_english_conversation()
    english_link = "https://learn.dict.naver.com/conversation#/"

    # 航空券セール
    flight_sale = get_flight_sale()
    flight_sale_link = URL_LINK_MO

    today_info_list = [
        update_time,
        weather_news,
        yen_to_won,
        japanese,
        english_conversation,
        flight_sale,
    ]
    link_list = [
        const.SYM_DASH,
        weather_news_link,
        finance_link,
        japanese_link,
        english_link,
        flight_sale_link,
    ]
    return today_info_list, link_list


# 天気ニュース取得
def get_today_weather_news() -> str:
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


# 天気予報取得
def get_forecast() -> str:
    url = f"{const.URL_TENKI}/world/5/89/47108/"
    soup = func_bs.get_elem_from_url(
        url, attr_val="weather-image", list_flg=const.FLG_ON
    )[1]
    forecast = func_bs.get_text_from_soup(soup)
    return forecast


# コーデ取得
def get_outfit() -> str:
    today_outfit = today.get_today_outfit()
    outfit = today_outfit.split(const.SYM_NEW_LINE)[0].split(const.SYM_PERIOD)[:2]
    return outfit[:20]


# 航空券セール情報取得
def get_flight_sale() -> str:
    flight_sale = const.SYM_BLANK

    url = f"{URL_FLIGHT}/product/free/subIndex.do?majorCategoryCd=C003"
    soup = func_bs.get_elem_from_url(url, attr_val="tblListB noBd line2")

    item_list = func_bs.find_elem_by_attr(
        soup, tag=const.TAG_TR, list_flg=const.FLG_ON
    )[1:5]
    for item in item_list:
        info_list = func_bs.find_elem_by_class(item, "shortCut", list_flg=const.FLG_ON)
        price_info = func_bs.find_elem_by_class(item, "js_tooltip_btn").text
        price = price_info.replace("원", const.SYM_BLANK).replace(",", const.SYM_BLANK)
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


# 日本語
def get_japanese_study() -> str:
    japanese_study = const.SYM_BLANK

    url = "https://wquiz.dict.naver.com/jakodict/today/quiz.dict#tab=1"
    soup = func_bs.get_elem_from_url(url, attr_val="todayword_quiz _primary_quiz")

    japanese = func_bs.find_elem_by_class(soup, "_primary_btn_listen btn_pron").get(
        "data-sentence"
    )

    korean_elem_list = func_bs.find_elem_by_class(
        soup, "multiple_answer_item _primary_answer_item", list_flg=const.FLG_ON
    )

    for korean_elem in korean_elem_list:
        if korean_elem.get("data-correct") == "1":
            korean = func_bs.get_text_from_soup(korean_elem)
            split_str = const.SYM_SEMI_COLON
            if split_str in korean:
                korean = korean.split(split_str)[0].replace(
                    const.SYM_DOT, const.SYM_BLANK
                )

            if split_str in japanese:
                japanese = japanese.split(split_str)[0].replace(
                    const.SYM_DOT, const.SYM_BLANK
                )

            japanese_study = f"{japanese} : {korean}"
            if korean_elem.get("lang") == const.LANG_JA:
                japanese_study = f"{korean} : {japanese}"
                break

    return japanese_study


# 英会話
def get_english_conversation() -> str:
    data = today.get_today_phrase(
        const.STR_ENGLISH
    )  # TODO: 英語も韓国語も半角スペース込みで16文字以内で再作成
    english_conversation = f"{data[1]}{const.SYM_NEW_LINE}{data[2]}"
    return english_conversation


# 今日の一言取得
def get_phrase() -> str:
    phrase = today.get_today_phrase(const.STR_PHRASE_KO)
    return phrase


if __name__ == const.MAIN_FUNCTION:
    # get_today_info_list()
    get_today_info()
