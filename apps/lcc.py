# 説明: LCCニュース

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_beautiful_soup as func_bs

# タイトル
app_title = func.convert_upper_lower(const.APP_LCC) + const.STR_NEWS_JA

# カラムリスト
col_list = [const.STR_DATE_JA, const.STR_COMPANY_JA, app_title]

# キーワードリスト
LIST_KEYWORD = func.get_input_data(const.STR_KEYWORD, const.APP_LCC)


# アイテムリスト取得
def get_item_list():
    item_list = get_lcc_info_list()
    return item_list


# LCC情報取得
def get_lcc_info_list(list_flg: bool = const.FLG_ON) -> list[str]:
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

            if list_flg:
                company = func.get_a_tag(url_official, company)
                lcc_data = [date, company, title]
                lcc_info_list.append(lcc_data)
            else:
                lcc_title = f"[LCC] {company}"
                return lcc_title, url_official

            if len(lcc_info_list) == const.MAX_DISPLAY_CNT:
                break
    return lcc_info_list


# テンプレートメッセージ取得
def get_temp_msg():
    lbl, url = get_lcc_info_list(list_flg=const.FLG_OFF)
    return lbl, url


# テキスト値取得
def get_lcc_text(lcc_div, soup):
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
