"""
LCCニュース
"""

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_api as func_api
import apps.utils.function_beautiful_soup as func_bs

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


def get_lcc_info_list() -> list[str]:
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
        date_time = func.convert_str_to_date(date, const.DATE_FORMAT_YYYYMMDD_JA)

        # 7日前
        target_date = func.get_calc_date(-const.NUM_TARGET_DAYS)
        if date_time < target_date:
            continue

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
            company = func.get_a_tag(url_official, company)
            lcc_data = [date, company, title]
            lcc_info_list.append(lcc_data)

            if len(lcc_info_list) == const.MAX_DISPLAY_CNT:
                break
    return lcc_info_list


def get_temp_msg(div: str = const.APP_LCC):
    """
    テンプレートメッセージ取得
    """
    company = url = const.SYM_BLANK
    json_data = func_api.get_json_data_on_app(div)
    if json_data:
        lcc_info = json_data[0]
        contents = lcc_info[const.STR_COMPANY]
        a_elem = func_bs.get_soup_from_contents(contents)
        company = a_elem.text
        url = func_bs.get_link_from_soup(a_elem)

    return div, company, url


def get_lcc_news_list():
    """
    LCCニュースリスト取得
    """
    news_list = []
    lcc_info_list = func_api.get_json_data_on_app(const.APP_LCC)
    if lcc_info_list:
        for lcc_info in lcc_info_list:
            date = lcc_info[const.STR_DATE]
            today = func.get_now(
                const.DATE_TODAY, const.DATE_FORMAT_YYYYMMDD_JA_NO_ZERO
            )
            if date != today:
                continue

            contents = lcc_info[const.STR_COMPANY]
            a_elem = func_bs.get_soup_from_contents(contents)
            company = a_elem.text
            news = lcc_info[const.APP_NEWS]

            title = f"[{company}] {news}"
            link_url = func_bs.get_link_from_soup(a_elem)
            news_info = [title, link_url]
            news_list.append(news_info)
            if len(news_list) == 3:
                break

    return news_list


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
    # get_temp_msg(const.FLG_ON)
