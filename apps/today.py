# 説明：今日の生活情報

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
DIV_WEATHER_PLUS = "天気+"
DIV_RATE = "為替"
DIV_OUTFIT = "コーデ"
DIV_DINNER = "夕食"
DIV_LIST = [DIV_WEATHER, DIV_WEATHER_PLUS, DIV_RATE, DIV_OUTFIT, DIV_DINNER]


# アイテムリスト取得
def get_item_list():
    today_info = get_today_info(const.FLG_OFF)[0]
    item_list = [[div, info] for div, info in today_info]
    return item_list


# 今日の生活情報取得
def get_today_info(msg_flg: bool = const.FLG_ON):
    # 天気
    today_weather, forecast, date_time = get_today_weather()

    # 天気
    today_weather_plus = get_today_weather_plus()

    # 為替
    today_won_rate = get_today_won()

    # コーデ・夕食
    recommend_outfit_dinner = func_gemini.get_recommend_outfit_dinner(
        NEW_LINE.join(today_weather)
    )

    today_outfit = recommend_outfit_dinner[0]
    # today_dinner = recommend_outfit_dinner[1].replace(NEW_LINE, const.SYM_BLANK)
    today_dinner = get_today_menu()

    col_list = DIV_LIST
    info_list = [
        today_weather,
        today_weather_plus,
        today_won_rate,
        today_outfit,
        today_dinner,
    ]
    if not msg_flg:
        info_list = [date_time] + info_list
        col_list = [DIV_DATE] + col_list

    today_info = zip(col_list, info_list)
    return today_info, forecast, date_time


# 今日の天気情報取得
def get_today_weather() -> tuple[str, str, str]:
    # 天気マップ取得
    elem_forecast_map = func_bs.get_elem_from_url(
        const.URL_TENKI, attr_div=const.ATTR_ID, attr_val="forecast-map-wrap"
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

    # 東京の情報取得
    elem_forecast = func_bs.find_elem_by_attr(
        elem_forecast_map, attr_div=const.ATTR_ID, attr_val="forecast-map-entry-13101"
    )

    forecast = get_elem_val_by_class(elem_forecast, "forecast-image")
    max_temp = get_elem_val_by_class(elem_forecast, "max-temp")
    min_temp = get_elem_val_by_class(elem_forecast, "min-temp")
    rain_prob = get_elem_val_by_class(elem_forecast, "prob-precip")

    today_weather = f"{forecast}・{max_temp}/{min_temp}・{rain_prob}"
    return today_weather, forecast, date_time


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

    today_weather_plus = f"花：{pollen}・黄：{dust}"
    return today_weather_plus


# 今日のウォン取得
def get_today_won() -> str:
    url = f"{const.URL_NAVER_FINANCE}/marketindex/exchangeDetail.naver?marketindexCd=FX_JPYKRW"
    class_ = "tbl_calculator"

    elem = func_bs.get_elem_from_url(url, attr_div=const.ATTR_CLASS, attr_val=class_)
    elem_list = func_bs.find_elem_by_attr(elem, tag=const.TAG_TD, list_flg=const.FLG_ON)

    won = elem_list[0].text if elem_list else "1000"
    today_won_rate = f"100{const.STR_YEN_JA}={won}{const.STR_WON_JA}"
    return today_won_rate


# 今日のレシピメニュー取得
def get_today_menu():
    url = const.URL_RAKUTEN_RECIPE
    _class = "weekly_menu__menu weekly_list"
    weekly_menu_list = func_bs.get_elem_from_url(
        url, attr_val=_class, list_flg=const.FLG_ON
    )
    weekly_menu = weekly_menu_list[const.DATE_WEEKDAY]
    menu = get_elem_val_by_class(weekly_menu, "text weekly_list__text omit_2line")
    return menu


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
