# 説明：LCCニュース

import utils.constants as const
import utils.function as func
import utils.function_beautiful_soup as func_bs

# アプリケーション名
app_name = func.get_app_name(__file__)

# タイトル
app_title = "LCC" + const.STR_NEWS_JA

# URL
URL_LCC = "https://dsk.ne.jp/"

# カラムリスト
COL_LIST = [
    const.STR_DIV_JA,
    const.STR_COMPANY_JA,
    const.STR_TITLE_JA,
    const.STR_LINK_JA,
]

# キーワードリスト
KEYWORD_LIST = [
    "韓国",
    "ソウル",
    "沖縄",
    "那覇",
    "台北",
    "ハノイ",
    "バンコク",
    "セール",
    "SALE",
]


# データリスト取得
def get_data_list() -> list[tuple[list[str], list[str]]]:
    data_list = []

    lcc_data_list = []
    lcc_list = func_bs.get_elem_from_url(
        URL_LCC, tag=const.TAG_DIV, attr_val="dgt3", list_flg=const.FLG_ON
    )
    for lcc_info in lcc_list:
        lcc_data = []
        href = func_bs.get_link_from_soup(lcc_info)
        if not href:
            continue

        url_news = URL_LCC + href

        # lcc_info_details = func_bs.get_elem_from_url(
        #     url_news, tag=const.TAG_DIV, attr_val="body"
        # )
        # url_news = func_bs.get_link_from_soup(lcc_info_details)

        lcc_line = func_bs.find_elem_by_attr(
            lcc_info, tag=const.TAG_DIV, attr_val="headline"
        )
        div = get_lcc_text(const.STR_DIV, lcc_line)
        date = get_lcc_text(const.TYPE_DATE, lcc_line)
        title_org = get_lcc_text(const.STR_TITLE, lcc_line)
        if not div or not date or not title_org:
            continue

        title_text = title_org.split(date)[1].split("、")
        company = title_text[0]
        title = title_text[1]

        if func.check_in_list(title, KEYWORD_LIST):
            lcc_data = [company, div, title, url_news]
            lcc_data_list.append(lcc_data)

            if len(lcc_data_list) == const.NUM_PRINT_CNT:
                break

    data_info = [COL_LIST, lcc_data_list]
    data_list.append(data_info)
    return data_list


# テキスト値取得
def get_lcc_text(lcc_div, soup):
    lcc_item = soup
    if lcc_div == const.STR_DIV:
        lcc_item = func_bs.find_elem_by_attr(soup, tag=const.TAG_SPAN)
    elif lcc_div == const.TYPE_DATE:
        lcc_item = func_bs.find_elem_by_attr(soup, tag=const.TAG_DIV, attr_val="date")

    try:
        lcc_text = lcc_item.text
    except:
        lcc_text = const.SYM_BLANK

    return lcc_text


if __name__ == const.MAIN_FUNCTION:
    data_list = get_data_list()
    print(data_list[0][1])
