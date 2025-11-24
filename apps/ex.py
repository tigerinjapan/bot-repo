"""
為替情報
"""

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_beautiful_soup as func_bs

# URLパラメータ
URL_PARAM = "finance/quote/JPY-{}"

DICT_EX = dict(zip(const.EX_LIST, const.EX_LIST_JA))


def get_today_won(ko_flg: bool = const.FLG_OFF) -> str:
    """
    今日のウォン取得
    """
    url = f"{const.URL_NAVER_FINANCE}/marketindex/exchangeDetail.naver?marketindexCd=FX_JPYKRW"
    class_ = "tbl_calculator"

    elem = func_bs.get_elem_from_url(url, attr_val=class_)
    elem_list = func_bs.find_elem_by_attr(elem, tag=const.TAG_TD, list_flg=const.FLG_ON)

    won = "950"
    if elem_list:
        won = get_ex_val(elem_list[0].text)

    yen_unit = const.STR_JPY_JA
    won_unit = const.STR_KRW_JA
    if ko_flg:
        yen_unit = const.STR_JPY_KO
        won_unit = const.STR_KRW_KO
    today_won_rate = f"100{yen_unit} = {won}{won_unit}"
    return today_won_rate


def get_ex_yen_list():
    """
    今日の為替情報取得
    """
    col_list = [const.STR_DIV]
    for jpy in const.JPY_LIST:
        col_list.append(f"{jpy}{const.STR_JPY_JA}")

    ex_yen_list = []

    for ex_div in const.EX_LIST:
        ex_info = get_ex_info(ex_div)
        ex_yen_list.append(ex_info)
    return ex_yen_list


def get_ex_info(ex_div: str = const.STR_KRW):
    """
    為替情報取得
    """
    url = f"{const.URL_GOOGLE}/{URL_PARAM}".format(ex_div)
    ex_str = func_bs.get_elem_from_url(url, attr_val="YMlKec fxKbKc")

    if ex_str:
        ex_val = get_ex_val(ex_str.text, unit_flg=const.FLG_ON)
        col_ex = DICT_EX[ex_div]
        ex_info = f"100{const.STR_JPY_JA} = {ex_val}{col_ex}"
    return ex_info


def get_ex_val(
    ex_text: str,
    unit_flg: bool = const.FLG_OFF,
    round_flg: bool = const.FLG_OFF,
    str_flg: bool = const.FLG_ON,
):
    """
    為替の数値取得
    """
    ex_num = float(ex_text)
    if unit_flg:
        ex_num *= 100

    if round_flg:
        ex_num = round(ex_num, 2)

    # 3桁区切りの表示
    ex_val = int(ex_num)
    if str_flg:
        ex_val = "{:,}".format(ex_val)
    return ex_val


if __name__ == const.MAIN_FUNCTION:
    ex_div = const.STR_USD
    ex_info = get_ex_info(ex_div)
    func.print_test_data(ex_info)
