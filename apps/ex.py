# 説明: 為替情報

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_beautiful_soup as func_bs

# アプリケーション名
app_name = func.get_app_name(__file__)

# URLパラメータ
URL_PARAM = "finance/quote/JPY-{}"

# JPY単位
JPY_LIST = [100, 1000, 10000]

# カラムリスト
EX_LIST = [
    const.STR_KRW,
    const.STR_USD,
    const.STR_TWD,
    const.STR_THB,
    const.STR_PHP,
    const.STR_VND,
]
EX_LIST_JA = [
    const.STR_KRW_JA,
    const.STR_USD_JA,
    const.STR_TWD_JA,
    const.STR_THB_JA,
    const.STR_PHP_JA,
    const.STR_VND_JA,
]
DICT_EX = dict(zip(EX_LIST, EX_LIST_JA))


# 今日のウォン取得
def get_today_won() -> str:
    url = f"{const.URL_NAVER_FINANCE}/marketindex/exchangeDetail.naver?marketindexCd=FX_JPYKRW"
    class_ = "tbl_calculator"

    elem = func_bs.get_elem_from_url(url, attr_val=class_)
    elem_list = func_bs.find_elem_by_attr(elem, tag=const.TAG_TD, list_flg=const.FLG_ON)

    won = elem_list[0].text if elem_list else "1000"
    today_won_rate = f"100{const.STR_JPY_JA} = {won}{const.STR_KRW_JA}"
    return today_won_rate


# 今日の為替情報取得
def get_ex_yen_list():
    col_list = [const.STR_DIV_JA]
    for jpy in JPY_LIST:
        col_list.append(f"{jpy}{const.STR_JPY_JA}")

    ex_yen_list = []

    for ex_div in EX_LIST:
        ex_info = get_ex_info(ex_div)
        ex_yen_list.append(ex_info)
    return ex_yen_list


def get_ex_info(ex_div: str = const.STR_KRW):
    url = f"{const.URL_GOOGLE}/{URL_PARAM}".format(ex_div)
    ex_str = func_bs.get_elem_from_url(url, attr_val="YMlKec fxKbKc")

    if ex_str:
        ex_text = ex_str.text
        ex_num = float(ex_text) * 100
        ex_val = round(ex_num, 2)
        col_ex = DICT_EX[ex_div]
        ex_info = f"100{const.STR_JPY_JA} = {ex_val}{col_ex}"
    return ex_info


if __name__ == const.MAIN_FUNCTION:
    ex_div = const.STR_USD
    ex_info = get_ex_info(ex_div)
    func.print_test_data(ex_info)
