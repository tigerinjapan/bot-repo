# 説明：今日の生活情報

import utils.constants as const
import utils.function as func
import utils.function_beautiful_soup as func_bs
import utils.function_gemini as func_gemini

# アプリケーション名
app_name = func.get_app_name(__file__)

# タイトル
app_title = "今日の生活情報"

# カラムリスト
COL_LIST = [const.STR_DIV_JA, const.STR_CONTENTS_JA]

# URL
URL_TENKI = "https://tenki.jp"
URL_NAVER_FINANCE = "https://finance.naver.com"

# 改行
NEW_LINE = const.SYM_NEW_LINE

# 定数（日本語）
DIV_WEATHER = "天気"
DIV_RATE = "為替"
DIV_OUTFIT = "コーデ"
DIV_DINNER = "夕食"
DIV_LIST = [DIV_WEATHER, DIV_RATE, DIV_OUTFIT, DIV_DINNER]

STR_YEN_JA = "円"
STR_WON_JA = "ウォン"


# データリスト取得
def get_data_list() -> list[tuple[list[str], list[str]]]:
    data_list = []

    today_info = get_today_info()[0]
    today_info_list = [[div, info] for div, info in today_info]
    today_info_list = [COL_LIST, today_info_list]
    data_list.append(today_info_list)
    return data_list


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

    today_outfit = recommend_outfit_dinner[0]
    today_dinner = recommend_outfit_dinner[1].replace(NEW_LINE, const.SYM_BLANK)

    info_list = [today_weather, today_won_rate, today_outfit, today_dinner]
    today_info = zip(DIV_LIST, info_list)
    return today_info, forecast


# 今日の天気情報取得
def get_today_weather() -> tuple[list[str], str]:
    # 東京の情報取得
    soup_result = func_bs.get_elem_from_url(
        URL_TENKI, attr_div=const.ATTR_ID, attr_val="forecast-map-entry-13101"
    )

    forecast = get_elem_val_by_class(soup_result, "forecast-image")
    max_temp = get_elem_val_by_class(soup_result, "max-temp")
    min_temp = get_elem_val_by_class(soup_result, "min-temp")
    rain_prob = get_elem_val_by_class(soup_result, "prob-precip")

    today_weather = f"{forecast}・{max_temp}/{min_temp}・{rain_prob}"
    return today_weather, forecast


# 今日のウォン取得
def get_today_won() -> list[str]:
    url = (
        f"{URL_NAVER_FINANCE}/marketindex/exchangeDetail.naver?marketindexCd=FX_JPYKRW"
    )
    class_ = "tbl_calculator"

    elem = func_bs.get_elem_from_url(url, attr_div=const.ATTR_CLASS, attr_val=class_)
    elem_list = func_bs.find_elem_by_attr(elem, tag=const.TAG_TD, list_flg=const.FLG_ON)

    won = elem_list[0].text
    today_won_rate = f"100{STR_YEN_JA}={won}{STR_WON_JA}"
    return today_won_rate


# 要素値取得
def get_elem_val_by_class(soup, class_: str) -> str:
    elem = func_bs.find_elem_by_attr(soup, attr_div=const.ATTR_CLASS, attr_val=class_)

    if class_ == "forecast-image":
        elem_val = elem.get(const.ATTR_ALT)
    else:
        elem_val = elem.text
    return elem_val


if __name__ == const.MAIN_FUNCTION:
    data_list = get_data_list()
    print(data_list)
