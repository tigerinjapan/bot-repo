"""
TV番組検索
"""

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_api as func_api
import apps.utils.function_beautiful_soup as func_bs

# ソートリスト
sort_list = [const.STR_DATE, const.STR_CHANNEL]
ascending_div = [const.FLG_ON, const.FLG_ON]

# カラムリスト
col_list = sort_list + [const.STR_PROGRAM]

# 重複チェックリスト
duplicates_list = sort_list

# キーワードリスト
LIST_KEYWORD = func.get_input_data(const.STR_KEYWORD, const.APP_TV)

# 分割リスト
LIST_SPLIT = ["\u3000", "▽", "★", "☆", "◆", "◇", "■", "□", "#", "？", "！"]

# URL
URL_PARAM = (
    "schedulesBySearch.action?stationPlatformId=1"
    + "&condition.keyword={}&submit=%E6%A4%9C%E7%B4%A2"
)


def get_item_list():
    """
    アイテムリスト取得
    """
    item_list = get_tv_info_list()
    return item_list


def get_tv_info_list() -> list[str]:
    """
    TV番組情報取得
    """
    tv_info_list = []

    url = f"{const.URL_TV}/ranking/?genre_id=5"
    program_list = func_bs.get_elem_from_url(url, attr_val="program_list_convertible")

    link_info_list = func_bs.find_elem_by_class(
        program_list, "js-logging", list_flg=const.FLG_ON
    )

    for link_info in link_info_list:
        tv_info_text = func_bs.find_elem_by_class(
            link_info, "program_supplement"
        ).text.split("　")

        date_txt = tv_info_text[0].split(" ")
        date = func.convert_date_format(
            f"{func.get_now(const.DATE_YEAR)}年" + date_txt[0],
            new_format=const.DATE_FORMAT_YYYYMMDD_SLASH,
            old_format=const.DATE_FORMAT_YYYYMMDD_JA,
        )
        time_text = date_txt[2]
        hour = time_text.split(":")[0]

        if 20 <= int(hour):
            date += f" {time_text}"
            channel = tv_info_text[1]

            program_title = func_bs.find_elem_by_class(link_info, "program_title").text
            link = const.URL_TV + link_info[const.ATTR_HREF]
            program = func.get_a_tag(link, program_title)

            if func.check_in_list(program_title, LIST_KEYWORD):
                tv_info = [date, channel, program]
                tv_info_list.append(tv_info)

            if len(tv_info_list) == 5:
                break

    return tv_info_list


def get_temp_msg(div: str = const.APP_TV):
    """
    テンプレートメッセージ取得
    """
    program = url = const.SYM_BLANK

    json_data = func_api.get_json_data_on_app(div)
    if json_data:
        tv_info = json_data[0]
        contents = tv_info[const.STR_PROGRAM]
        a_elem = func_bs.get_soup_from_contents(contents)
        program = get_tv_title(a_elem.text)
        url = func_bs.get_link_from_soup(a_elem)

    return div, program, url


def get_tv_title(tv_title: str):
    """
    TVタイトル取得
    """
    for split_str in LIST_SPLIT:
        if split_str in tv_title:
            tv_title = tv_title.split(split_str)[0]
            break
    return tv_title


if __name__ == const.MAIN_FUNCTION:
    # item_list = get_item_list()
    # func.print_test_data(item_list)
    get_temp_msg()
