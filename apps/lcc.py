"""
LCCニュース
"""

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_beautiful_soup as func_bs
import apps.utils.message_constants as msg_const

# カラムリスト
col_list = [const.STR_DATE, const.STR_COMPANY, const.APP_NEWS]

# キーワードリスト
LIST_KEYWORD = func.get_input_data(const.STR_KEYWORD, const.APP_LCC)


def get_item_list():
    """
    アイテムリスト取得
    """
    item_list = get_lcc_info_list()
    return item_list


def get_lcc_info_list(url_flg: bool = const.FLG_OFF) -> list[str]:
    """
    LCC情報取得
    """
    lcc_info_list = []
    url = f"{const.URL_LCC}/news/"
    lcc_list = func_bs.get_elem_from_url(url, attr_val="bgtitle", list_flg=const.FLG_ON)

    if not lcc_list:
        return lcc_info_list

    for lcc_info in lcc_list:
        lcc_data = []

        date = func_bs.find_elem_by_class(lcc_info, "bgdate").text
        title_info = func_bs.find_elem_by_attr(lcc_info, tag=const.TAG_A)
        title_text = title_info.text.split(const.SYM_COMMA_JAP)
        company = title_text[0]
        title = title_text[1].replace("」", f"」{const.SYM_NEW_LINE}")
        title_info = func_bs.find_elem_by_attr(lcc_info, tag=const.TAG_A)

        check_keyword = const.SYM_SPACE.join(title_text)
        if func.check_in_list(check_keyword, LIST_KEYWORD):
            url_news = const.URL_LCC + title_info.get(const.ATTR_HREF)

            lcc_info_details = func_bs.get_elem_from_url(
                url_news, tag=const.TAG_DIV, attr_val="body"
            )

            if not lcc_info_details:
                continue

            url_official = func_bs.get_link_from_soup(lcc_info_details)

            if url_flg:
                lcc_data = [date, company, title, url_official]
            else:
                company = func.get_a_tag(url_official, company)
                lcc_data = [date, company, title]

            lcc_info_list.append(lcc_data)

            if len(lcc_info_list) == const.MAX_DISPLAY_CNT:
                break
    return lcc_info_list


def get_temp_msg(data_flg: bool = const.FLG_OFF):
    """
    テンプレートメッセージ取得
    """
    lbl = url = const.SYM_BLANK
    lcc_info = get_lcc_info_list(url_flg=const.FLG_ON)[0]
    if lcc_info:
        lbl = f"[{const.APP_LCC}] {lcc_info[1]}"
        url = lcc_info[3]
        if data_flg:
            lcc_data = const.SYM_BLANK
            today = func.get_now(const.DATE_TODAY, const.DATE_FORMAT_YYYYMMDD_JA)
            if lcc_info[0] == today:
                lcc_data_list = [lbl] + lcc_info[2:]
                lcc_data = const.SYM_NEW_LINE.join(lcc_data_list)
            url = lcc_data

    if not url:
        func.print_debug_msg(const.APP_LCC, msg_const.MSG_INFO_DATA_NOT_EXIST)

    return lbl, url


def get_lcc_text(lcc_div, soup) -> str:
    """
    テキスト値取得
    """
    lcc_item = soup
    if lcc_div == const.STR_DIV:
        lcc_item = func_bs.find_elem_by_attr(soup, tag=const.TAG_SPAN)
    elif lcc_div == const.TYPE_DATE:
        lcc_item = func_bs.find_elem_by_attr(soup, tag=const.TAG_DIV, attr_val="date")

    lcc_text = lcc_item.text if lcc_item else const.SYM_BLANK
    return lcc_text


if __name__ == const.MAIN_FUNCTION:
    item_list = get_item_list()
    func.print_test_data(item_list)
    # get_temp_msg()
