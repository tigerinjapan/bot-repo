"""
イベントの一覧取得
"""

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_beautiful_soup as func_bs


def get_item_list(list_flg: bool = const.FLG_OFF):
    """
    イベントタイトルのリスト取得
    """
    item_list = []

    check_day_list = get_check_day_list()

    json_data = func.get_input_data("event")
    for event in json_data:
        target_date = event[const.STR_DATE]
        if target_date in check_day_list:
            title = event[const.STR_TITLE]
            item_list.append(title)

    if not item_list:
        url = "https://kids.yahoo.co.jp/today"
        class_ = "DateInfoEvent_eventTitle__u2nYP"
        elem = func_bs.get_elem_from_url(url, attr_val=class_)
        item_list = [elem.text]

    if not list_flg:
        return item_list[0]

    return item_list


def get_check_day_list():
    """
    今日を基準にして照合に使う複数形式の日付リスト
    """
    now = func.get_now()
    today = func.get_now(const.DATE_TODAY)

    # 曜日名略称 (例:Mon)
    day_abbr = func.convert_date_to_str(now, "%a")

    month_week_day = convert_day(now, day_abbr)
    month_day = f"mm{today[6:]}"
    month_day_no_zero = f"mm{const.SYM_ASTA}{today[-1]}"
    every_day = f"every{day_abbr}"

    check_list = [today, month_week_day, month_day, month_day_no_zero, every_day]
    return check_list


def convert_day(now, day_abbr: str):
    """
    月＋週＋曜日の文字列を作成
    """
    # 月名略称 (例:Dec)
    month_abbr = func.convert_date_to_str(now, "%b")

    # 同じ月の1日を取得
    first_day_of_month = now.replace(day=1)

    # 1日から指定の日付までの日数差
    day_difference = (now - first_day_of_month).days

    # 週番号 (0から始まる)。7日ごとに、週番号が増える計算
    week_number_zero_indexed = day_difference // 7

    # 1始まりの週番号に変換
    week_number = week_number_zero_indexed + 1

    # 何週目か計算
    week_suffix = {1: "st", 2: "nd", 3: "rd"}.get(week_number, "th")
    week_text = f"{week_number}{week_suffix}"

    # 月 + 週 + 曜日 を結合
    result = f"{month_abbr}{week_text}{day_abbr}"
    return result


if __name__ == const.MAIN_FUNCTION:
    get_item_list()
