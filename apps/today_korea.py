# 説明: 今日の生活情報

import apps.ex as ex
import apps.today as today
import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_beautiful_soup as func_bs

# 定数（韓国語）
DIV_TITLE = "📢 {} 오늘의 뉴스 📢"
DIV_WEATHER = "날씨"
DIV_RATE = "환율"
DIV_JAPANESE = "일본어"
DIV_FLIGHT = "항공권"
DIV_LIST = [DIV_WEATHER, DIV_RATE, DIV_JAPANESE, DIV_FLIGHT]

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


# 今日の生活情報取得
def get_today_info(img_flg: bool = const.FLG_ON):
    # タイトル
    today_date = func.convert_date_to_str(func.get_now(), const.DATE_FORMAT_YYYYMMDD_KO)
    title = DIV_TITLE.format(today_date)
    if img_flg:
        title = title.replace("📢", "■")

    today_info_list = get_today_info_list()
    item_list = [
        f"[{div}] {info}" for div, info in zip(DIV_LIST, today_info_list) if info
    ]
    item_list.insert(0, title)
    today_info = const.SYM_NEW_LINE.join(item_list)

    link_title = TITLE_LINK
    link = URL_LINK
    link_mo = URL_LINK_MO
    forecast = get_forecast()
    outfit = today.get_today_outfit()
    return today_info, link_title, link, link_mo, forecast, outfit


# 今日の生活情報取得
def get_today_info_list():
    # 天気
    weather_news, news_link = get_today_weather_news()

    # 為替
    yen_to_won = ex.get_today_won(const.FLG_ON)

    # 日本語
    japanese = get_japanese_study()

    # 航空券セール
    flight_sale, link = get_flight_sale()

    today_info = [weather_news, yen_to_won, japanese, flight_sale]
    return today_info


# 天気ニュース取得
def get_today_weather_news():
    title = const.SYM_BLANK

    today = func.get_now(const.DATE_TODAY)
    url = f"https://media.naver.com/press/214/ranking?type=section&date={today}"

    soup = func_bs.get_elem_from_url(
        url, attr_val="press_ranking_box is_section", list_flg=const.FLG_ON
    )[3]
    link = func_bs.get_link_from_soup(soup)

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

    return title, link


# 天気予報取得
def get_forecast() -> str:
    url = f"{const.URL_TENKI}/world/5/89/47108/"
    soup = func_bs.get_elem_from_url(
        url, attr_val="weather-image", list_flg=const.FLG_ON
    )[1]
    forecast = func_bs.get_text_from_soup(soup)
    return forecast


# 航空券セール情報取得
def get_flight_sale():
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
        dd_id = link_info.get("ddid")
        p_num = link_info.get("pnum")
        link = f"{URL_FLIGHT}/common/free/getGoodsInfo.do?ddId={dd_id}&pnum={p_num}"

        if from_ in LIST_CITY_KOR and to in LIST_CITY_JPN and int(price) < 300000:
            sale_info = f"{from_}↔️{to} {price_info}"
            return sale_info, link


# 日本語
def get_japanese_study() -> str:
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

            study = f"{japanese} : {korean}"
            return study


# 今日の一言取得
def get_phrase():
    phrase = today.get_today_phrase(const.STR_PHRASE_KO)
    return phrase


if __name__ == const.MAIN_FUNCTION:
    # today_info, link, link_mo, link_title, forecast, outfit = get_today_info_list()
    # func.print_test_data(today_info)
    get_forecast()
