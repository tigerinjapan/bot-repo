"""
ランキング
"""

import apps.news as news
import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_beautiful_soup as func_bs

# タイトル
app_title = news.DIV_WEEKLY_RANKING.format(const.SYM_BLANK)

# ランキング区分リスト
LIST_RANKING_WEEKLY = [const.STR_KPOP]
LIST_RANKING_DAILY = [const.STR_X_TREND_JA]
DIV_DAILY_RANKING = "{}日間" + const.STR_RANKING_JA

# カラムリスト
col_list_weekly = [news.DIV_WEEKLY_RANKING.format(div) for div in LIST_RANKING_WEEKLY]
col_list_daily = [DIV_DAILY_RANKING.format(div) for div in LIST_RANKING_DAILY]
col_list = col_list_weekly + col_list_daily

# URL
URL_X_PARAM = "/twitter_trend_daily_ranking_all/"


def get_item_list():
    """
    アイテムリスト取得
    """
    item_list = []

    for div_weekly in LIST_RANKING_WEEKLY:
        ranking_info = get_weekly_ranking(div_weekly)
        item_list.append(ranking_info)

    for div_daily in LIST_RANKING_DAILY:
        ranking_info = get_daily_ranking(div_daily)
        item_list.append(ranking_info)

    item_list = [list(item) for item in zip(*item_list)]
    return item_list


def get_weekly_ranking(div: str = const.STR_KPOP):
    """
    週間KPOPランキング取得
    """
    weekly_ranking = []

    url = f"{const.URL_WOWKOREA}/ranking/weekly/{div}/"

    elem_list = news.get_elem_list(news.DIV_KPOP_RANKING, url)

    if not elem_list:
        return weekly_ranking

    for elem in elem_list[: const.MAX_DISPLAY_CNT]:
        if not elem:
            break

        if div == const.STR_KPOP:
            text_data = elem.text
            if not text_data:
                continue

            ranking_info = text_data
            text_list = []

            split_str_list = ["」 ", "」", "] ", "\u3000"]
            for split_str in split_str_list:
                if split_str in text_data:
                    text_list = text_data.split(split_str)
                    break

            if text_list:
                singer = text_list[1]

                target_list = ["「 ", "「", "["]
                song = func.get_replace_data(text_list[0], target_list)
                ranking_info = f"{singer} - {song}"

            weekly_ranking.append(ranking_info)

    return weekly_ranking


def get_daily_ranking(div: str = const.STR_X_TREND_JA):
    """
    Xトレンド日間ランキング
    """
    daily_ranking = []

    if div == const.STR_X_TREND_JA:
        url = f"{const.URL_ACHIKOCHI}{URL_X_PARAM}"
        soup = func_bs.get_elem_from_url(url, attr_val="panel")
        elem_list = func_bs.find_elem_by_attr(
            soup, tag=const.TAG_H4, list_flg=const.FLG_ON
        )
        if elem_list:
            for elem in elem_list[: const.MAX_DISPLAY_CNT]:
                elem_text = elem.text
                if elem_text:
                    ranking_info = elem_text if elem_text[0] == "#" else f"#{elem_text}"
                    daily_ranking.append(ranking_info)

    return daily_ranking


if __name__ == const.MAIN_FUNCTION:
    item_list = get_item_list()
    func.print_test_data(item_list)
