# 説明：TV番組検索

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_beautiful_soup as func_bs

# アプリケーション名
app_name = func.get_app_name(__file__)

# タイトル
app_title = "TV番組"

# ソートリスト
sort_list = ["放送時間", "チャンネル"]
ascending_div = [True, True]

# カラムリスト
col_list = sort_list + ["番組名"]

# 重複チェックリスト
duplicates_list = sort_list

# キーワードリスト
LIST_KEYWORD = func.get_input_data(const.STR_KEYWORD, app_name)

# URL
URL_PARAM = (
    "schedulesBySearch.action?stationPlatformId=1"
    + "&condition.keyword={}&submit=%E6%A4%9C%E7%B4%A2"
)


# アイテムリスト取得
def get_item_list():
    item_list = []
    for keyword in LIST_KEYWORD:
        tv_info_list = get_tv_info_list(keyword)
        item_list += tv_info_list

    return item_list


# TV番組情報取得
def get_tv_info_list(keyword) -> list[str]:
    tv_info_list = []

    url = f"{const.URL_TV}/{URL_PARAM}".format(keyword)
    soup = func_bs.get_elem_from_url(
        url, const.TAG_FORM, const.STR_NAME, "form_multi_iepg"
    )
    title_list = func_bs.find_elem_by_attr(
        soup, tag=const.TAG_H2, list_flg=const.FLG_ON
    )
    program_list = func_bs.find_elem_by_attr(
        soup,
        attr_div=const.ATTR_CLASS,
        attr_val="utileListProperty",
        list_flg=const.FLG_ON,
    )

    if not title_list or not program_list:
        return tv_info_list

    for title_elem, program_elem in zip(title_list, program_list):
        title_text = func.get_replace_data(title_elem.text)
        if not title_text or keyword not in title_text:
            continue

        title_text = title_text.replace(keyword, f"<b>{keyword}</b>")

        link = const.URL_TV + func_bs.get_link_from_soup(title_elem)

        tv_info_txt = (
            func.get_replace_data(program_elem.text)
            .replace(const.SYM_SPACE, const.SYM_BLANK)
            .split("\r")
        )
        time = tv_info_txt[1]
        running_min = time.split("分")[0].split("(")[-1]
        hour = time.split(")")[1].split(":")[0]
        if 30 <= int(running_min) and 10 <= int(hour):
            channel = tv_info_txt[2]
            title = func.get_a_tag(link, title_text)
            tv_info = [time, channel, title]
            tv_info_list.append(tv_info)

    return tv_info_list


if __name__ == const.MAIN_FUNCTION:
    item_list = get_item_list()
    func.print_test_data(item_list)
