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


# 今日のウォン取得
def get_today_won() -> str:
    url = f"{const.URL_NAVER_FINANCE}/marketindex/exchangeDetail.naver?marketindexCd=FX_JPYKRW"
    class_ = "tbl_calculator"

    elem = func_bs.get_elem_from_url(url, attr_val=class_)
    elem_list = func_bs.find_elem_by_attr(elem, tag=const.TAG_TD, list_flg=const.FLG_ON)

    won = elem_list[0].text if elem_list else "1000"
    today_won_rate = f"100{const.STR_YEN_JA} = {won}{const.STR_WON_JA}"
    return today_won_rate


# 今日の為替情報取得
def get_ex_yen_list():
    col_list = [const.STR_DIV_JA]
    for jpy in JPY_LIST:
        col_list.append(f"{jpy}{const.STR_YEN_JA}")

    ex_yen_list = []

    for i, ex in enumerate(EX_LIST):
        col_ex = EX_LIST_JA[i]
        url = f"{const.URL_GOOGLE}/{URL_PARAM}".format(ex)
        ex_str = func_bs.get_elem_from_url(url, attr_val="YMlKec fxKbKc")

        if ex_str:
            ex_text = ex_str.text
            ex_num = float(ex_text)
            ex_info_list = [col_ex]
            for jpy in JPY_LIST:
                ex_info_list.append(round(ex_num * jpy, 2))
            ex_yen_list.append(ex_info_list)
    return ex_yen_list


if __name__ == const.MAIN_FUNCTION:
    ex_yen_list = get_ex_yen_list()
    func.print_test_data(ex_yen_list)
