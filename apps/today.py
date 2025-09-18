# 説明: 今日の生活情報

import apps.ex as ex
import apps.mlb as mlb
import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_beautiful_soup as func_bs
import apps.utils.function_gemini as func_gemini

# アプリケーション名
app_name = func.get_app_name(__file__)

# タイトル
app_title = "今日の生活情報"

# カラムリスト
col_list = [const.STR_DIV_JA, app_title]

# 改行
NEW_LINE = const.SYM_NEW_LINE

# 定数（日本語）
DIV_DATE = "日時"
DIV_WEATHER = "天気"
DIV_WEATHER_PLUS = "天気"
DIV_NISA = "＄NISA＄"
DIV_RATE = "￥為替￥"
DIV_RATE_PLUS = "￥為替￥"
DIV_MLB = "MLB"
DIV_OUTFIT = "コーデ"
DIV_DINNER = "夕食"

DIV_LIST = [
    DIV_DATE,
    DIV_WEATHER,
    # DIV_WEATHER_PLUS,
    DIV_NISA,
    DIV_RATE,
    DIV_RATE_PLUS,
    DIV_MLB,
    DIV_OUTFIT,
    DIV_DINNER,
]


# アイテムリスト取得
def get_item_list():
    today_info_list = get_today_info()
    today_info = zip(DIV_LIST, today_info_list)
    item_list = [[div, info] for div, info in today_info]
    return item_list


# 今日の生活情報取得
def get_today_info():
    # 天気
    weather, date_time = get_today_weather()

    # 天気+
    # weather_plus = get_today_weather_plus()

    # NISA
    nisa = get_today_nisa()

    # 為替
    won = ex.get_today_won()

    # 為替+
    today_rate = ex.get_ex_info(const.STR_VND)

    # コーデ・夕食
    # recommend_outfit_dinner = func_gemini.get_recommend_outfit_dinner(
    #     NEW_LINE.join(today_weather)
    # )

    # outfit = recommend_outfit_dinner[0]
    # dinner = recommend_outfit_dinner[1].replace(NEW_LINE, const.SYM_BLANK)

    # コーデ
    outfit = get_today_outfit()

    # 夕食
    menu = get_today_menu()

    # MLB
    mlb_game = mlb.get_mlb_stat_of_api()

    today_info_list = [
        date_time,
        weather,
        nisa,
        won,
        today_rate,
        mlb_game,
        outfit,
        menu,
    ]
    return today_info_list


# 今日の天気情報取得
def get_today_weather() -> tuple[str, str]:

    url = f"{const.URL_TENKI}/forecast/3/"
    # location_id = 13101 # 東京
    location_id = 12100  # 千葉

    # 天気マップ取得
    elem_forecast_map = func_bs.get_elem_from_url(
        url, attr_div=const.ATTR_ID, attr_val="forecast-map-wrap"
    )

    # 現在日付
    elem_date_time = func_bs.find_elem_by_attr(
        elem_forecast_map,
        attr_div=const.ATTR_ID,
        attr_val="forecast-map-announce-datetime",
    )
    date_time_text = elem_date_time.get("datetime")

    date_time = func.convert_date_format(
        date_time_text, const.DATE_FORMAT_ISO, const.DATE_FORMAT_YYYYMMDD_HHMM
    )

    elem_forecast = func_bs.find_elem_by_attr(
        elem_forecast_map,
        attr_div=const.ATTR_ID,
        attr_val=f"forecast-map-entry-{location_id}",
    )

    forecast = get_elem_val_by_class(elem_forecast, "forecast-image")
    max_temp = get_elem_val_by_class(elem_forecast, "max-temp")
    min_temp = get_elem_val_by_class(elem_forecast, "min-temp")
    rain_prob = get_elem_val_by_class(elem_forecast, "prob-precip")

    today_weather = f"{forecast}・{max_temp}/{min_temp}・{rain_prob}"
    return today_weather, date_time


# 今日の天気情報取得
def get_today_weather_plus() -> str:
    url = f"{const.URL_TENKI}/pollen/"
    class_ = "top-map-pollen-pref-4"
    elem_pollen = func_bs.get_elem_from_url(url, attr_val=class_)
    pollen_alt = func_bs.find_elem_by_attr(elem_pollen, tag=const.TAG_IMG).get(
        const.ATTR_ALT
    )
    pollen = pollen_alt.split(const.SYM_COLON)[1]

    url = f"{const.URL_TENKI}/yellow-sand/3/16/"
    class_ = "common-info-table yellow-sand-info-table"

    elem_dust = func_bs.get_elem_from_url(url, attr_val=class_)
    dust = func_bs.find_elem_by_attr(elem_dust, tag=const.TAG_TD).get_text(
        strip=const.FLG_ON
    )

    today_weather_plus = f"花: {pollen}・黄: {dust}"
    return today_weather_plus


# 今日のNISA取得
def get_today_nisa(
    fund_no: str = const.FUND_NO_SP_500, msg_flg: bool = const.FLG_ON
) -> str:
    url = f"{const.URL_SMBC_FUND}/{fund_no}/"
    class_ = "sw-FundComparisonTable sw-FundComparisonTable_center"
    soup = func_bs.get_elem_from_url(url, attr_val=class_)
    elem = func_bs.find_elem_by_attr(soup, tag=const.TAG_TD, list_flg=const.FLG_ON)[0:2]
    point = elem[0].text
    rate = elem[1].text.replace(const.SYM_NEW_LINE, const.SYM_BLANK)

    fund_name = const.FUND_NAME_SP_500
    if fund_no == const.FUND_NO_AI:
        fund_name = const.FUND_NAME_AI
    elif fund_no == const.FUND_NO_US_TECH:
        fund_name = const.FUND_NAME_US_TECH

    today_nisa = f"{fund_name} = {point}"

    if msg_flg:
        # today_nisa += f" ({rate})"
        return today_nisa
    else:
        return fund_name, point


# 今日のコーデ取得
def get_today_outfit():
    url = f"{const.URL_CANCAM}/archives/tag/今日のコーデ"
    soup_main = func_bs.get_elem_from_url(url, attr_val="site-main yellow-main")
    link_today = func_bs.get_link_from_soup(soup_main)
    soup = func_bs.get_elem_from_url(link_today, attr_val="entry-content")
    outfit_elem_1 = get_elem_val_by_class(soup, "wp-block-heading")
    outfit_elem_p = func_bs.find_elem_by_attr(
        soup, tag=const.TAG_P, list_flg=const.FLG_ON
    )
    outfit_elem_2 = outfit_elem_p[1].text
    outfit_text = outfit_elem_1 + const.SYM_NEW_LINE + outfit_elem_2
    today_outfit = func_gemini.get_recommend_outfit(outfit_text)
    return today_outfit


# 今日のレシピメニュー取得
def get_today_menu():
    url = "https://park.ajinomoto.co.jp/menu/"
    weekly_menu_list = func_bs.get_elem_from_url(
        url, attr_val="recipeTitle", list_flg=const.FLG_ON
    )
    weekly_menu = [menu.text for i, menu in enumerate(weekly_menu_list) if i % 3 == 0]
    today_menu = weekly_menu[func.get_now(const.DATE_WEEKDAY)]
    return today_menu


# 今日のフレーズ取得
def get_today_phrase():
    file_path = func.get_file_path(const.STR_PHRASE, const.FILE_TYPE_CSV)
    dict_data = func.get_dict_from_csv(file_path)
    random_int = str(func.get_random_int(const.MAX_PHRASE_CSV))
    key = random_int.zfill(3)
    phrase = dict_data.get(key)[1]
    return phrase


# 要素値取得
def get_elem_val_by_class(soup, class_: str) -> str:
    elem_val = const.SYM_BLANK

    elem = func_bs.find_elem_by_attr(soup, attr_div=const.ATTR_CLASS, attr_val=class_)
    if elem:
        if class_ == "forecast-image":
            elem_val = elem.get(const.ATTR_ALT)
        else:
            elem_val = elem.text
    return elem_val


if __name__ == const.MAIN_FUNCTION:
    item_list = get_item_list()
    func.print_test_data(item_list)
