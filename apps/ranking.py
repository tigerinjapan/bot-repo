# 説明: ランキング

import apps.news as news
import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_beautiful_soup as func_bs

# アプリケーション名
app_name = func.get_app_name(__file__)

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


# アイテムリスト取得
def get_item_list():
    item_list = []

    for div_weekly in LIST_RANKING_WEEKLY:
        ranking_info = get_weekly_ranking(div_weekly)
        item_list.append(ranking_info)

    for div_daily in LIST_RANKING_DAILY:
        ranking_info = get_daily_ranking(div_daily)
        item_list.append(ranking_info)

    item_list = [list(item) for item in zip(*item_list)]
    return item_list


# 週間ランキング取得
def get_weekly_ranking(div: str = const.STR_KPOP):
    weekly_ranking = []

    url = f"{const.URL_WOWKOREA}/ranking/weekly/{div}/"

    elem_list = news.get_elem_list(news.DIV_KPOP_RANKING, url)

    if not elem_list:
        return weekly_ranking

    for elem in elem_list[: const.MAX_DISPLAY_CNT]:
        if not elem:
            break

        ranking_info = const.SYM_BLANK

        if div == const.STR_KPOP:
            text_data = elem.text
            if "] " in text_data:
                text_list = text_data.split("] ")
            else:
                text_list = text_data.split("」")

            singer = text_list[1]
            song = (
                text_list[0]
                .replace("「 ", const.SYM_BLANK)
                .replace("「", const.SYM_BLANK)
            )
            ranking_info = f"{singer} - {song}"

        if ranking_info:
            weekly_ranking.append(ranking_info)

    return weekly_ranking


# 日間ランキング
def get_daily_ranking(div: str = const.STR_X_TREND_JA):
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
