# 説明: TV番組検索

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

LIST_SPLIT = ["\u3000", "▽", "★", "☆", "#", "？", "！"]

# URL
URL_PARAM = (
    "schedulesBySearch.action?stationPlatformId=1"
    + "&condition.keyword={}&submit=%E6%A4%9C%E7%B4%A2"
)


# アイテムリスト取得
def get_item_list():
    item_list = []
    # for keyword in LIST_KEYWORD:
    #     tv_info_list = get_tv_info_list(keyword)
    #     item_list += tv_info_list

    item_list = get_tv_info_list2()
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


# TV番組情報取得
def get_tv_info_list2() -> list[str]:
    tv_info_list = []

    url = f"{const.URL_TV_RANKING}/?genre_id=5"
    program_list = func_bs.get_elem_from_url(url, attr_val="program_list_convertible")

    title_info_list = func_bs.find_elem_by_attr(
        program_list,
        attr_div=const.ATTR_CLASS,
        attr_val="program_title",
        list_flg=const.FLG_ON,
    )
    title_list = [title_info.text for title_info in title_info_list]

    tv_info_elem_list = func_bs.find_elem_by_attr(
        program_list,
        attr_div=const.ATTR_CLASS,
        attr_val="program_supplement",
        list_flg=const.FLG_ON,
    )
    tv_info_text_list = [
        tv_info_elem.text.split("　") for tv_info_elem in tv_info_elem_list
    ]

    for title, tv_info_text in zip(title_list, tv_info_text_list):
        date_txt = tv_info_text[0].split(" ")
        date = func.convert_date_format(
            f"{const.DATE_YEAR}年" + date_txt[0], f"%Y年%m月%d日", f"%Y/%m/%d(%a)"
        )
        time_text = date_txt[2]
        hour = time_text.split(":")[0]

        if 10 <= int(hour):
            channel = tv_info_text[1]

            date += f" {time_text}"
            tv_info = [date, channel, title]
            tv_info_list.append(tv_info)
            if len(tv_info_list) == 10:
                break

    return tv_info_list


def get_tv_info_today():
    tv_info_today = None

    tv_info_list = get_tv_info_list2()
    for tv_info in tv_info_list:
        title = tv_info[2]
        if func.check_in_list(title, LIST_KEYWORD):
            tv_info_today = tv_info
            break

    if not tv_info_today:
        tv_info_today = tv_info_list[0]

    time = tv_info_today[0].split(")")[1]
    tv_company = tv_info_today[1]
    tv_title = get_tv_title(tv_info_today[2])
    today_tv_info = f"[{tv_company + time}] {tv_title}"
    if 25 < len(today_tv_info):
        today_tv_info = today_tv_info[:25]
    return today_tv_info


def get_tv_title(tv_title: str):
    title = tv_title
    for split_str in LIST_SPLIT:
        if split_str in tv_title:
            title = tv_title.split(split_str)[0]
            break
    return title


if __name__ == const.MAIN_FUNCTION:
    tv_info_today = get_tv_info_today()
    func.print_test_data(tv_info_today)
