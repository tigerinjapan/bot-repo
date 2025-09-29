# 説明: TV番組検索

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_beautiful_soup as func_bs

# タイトル
app_title = "TV番組"

# ソートリスト
sort_list = ["放送時間", "チャンネル"]
ascending_div = [const.FLG_ON, const.FLG_ON]

# カラムリスト
col_list = sort_list + ["番組名"]

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


# アイテムリスト取得
def get_item_list():
    item_list = get_tv_info_list()
    return item_list


# TV番組情報取得
def get_tv_info_list(list_flg: bool = const.FLG_ON) -> list[str]:
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
            old_format=f"%Y年%m月%d日",
        )
        time_text = date_txt[2]
        hour = time_text.split(":")[0]

        if 20 <= int(hour):
            date += f" {time_text}"
            channel = tv_info_text[1]

            title = func_bs.find_elem_by_class(link_info, "program_title").text
            link = const.URL_TV + link_info[const.ATTR_HREF]
            title_link = func.get_a_tag(link, title)

            if func.check_in_list(title, LIST_KEYWORD):
                tv_info = [date, channel, title_link]

                if not list_flg:
                    tv_info = [time_text, channel, title, link]
                    return tv_info

                tv_info_list.append(tv_info)

            if len(tv_info_list) == 5:
                break

    return tv_info_list


# テンプレートメッセージ取得
def get_temp_msg():
    lbl, url = get_tv_info_today()
    return lbl, url


# TV番組情報取得
def get_tv_info_today():
    today_tv_info = link = const.SYM_BLANK

    tv_info_today = get_tv_info_list(list_flg=const.FLG_OFF)
    if tv_info_today:
        time = tv_info_today[0]
        channel = tv_info_today[1]
        title = get_tv_title(tv_info_today[2])
        today_tv_info = f"[{channel} {time}] {title}"
        link = tv_info_today[3]
    return today_tv_info, link


# TVタイトル取得
def get_tv_title(tv_title: str):
    for split_str in LIST_SPLIT:
        if split_str in tv_title:
            tv_title = tv_title.split(split_str)[0]
            break
    return tv_title


if __name__ == const.MAIN_FUNCTION:
    tv_info_today = get_tv_info_today()
    func.print_test_data(tv_info_today)
