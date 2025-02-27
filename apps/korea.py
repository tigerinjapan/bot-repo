# 説明：韓国ニュース

import apps.news as news
import apps.utils.constants as const
import apps.utils.function as func

# アプリケーション名
app_name = func.get_app_name(__file__)

# タイトル
app_title = const.STR_KOREA_JA + const.STR_NEWS_JA

# カラムリスト
col_list = news.col_list


# データリスト取得
def get_data_list() -> list[tuple[list[str], list[str]]]:
    data_list = []

    item_list = get_item_list(news.DIV_KOREA_NEWS_LIST)  # TODO ランキングに変更
    data_info = [col_list, item_list]
    data_list.append(data_info)

    data_list += get_korea_weekly_ranking()
    return data_list


# アイテムリスト取得
def get_item_list():
    item_list = news.get_item_list(news.DIV_KOREA_NEWS_LIST)
    return item_list


# 韓国週間ランキング取得
def get_korea_weekly_ranking(div: str = const.STR_KPOP):
    korea_news = []
    kpop_weekly_ranking = []

    url = f"{news.URL_WOWKOREA}/ranking/weekly/{div.lower()}/"
    elem_list = news.get_elem_list(news.DIV_KPOP_RANKING, url)

    if not elem_list:
        return korea_news

    for elem in elem_list[: const.MAX_DISPLAY_CNT]:
        if not elem:
            break
        text_data = elem.text
        text_list = text_data.split("」")
        singer = text_list[1]
        song = (
            text_list[0].replace("「 ", const.SYM_BLANK).replace("「", const.SYM_BLANK)
        )
        ranking_info = [f"{singer} - {song}"]
        kpop_weekly_ranking.append(ranking_info)

    column_list = [news.DIV_KPOP_RANKING]
    korea_news.append([column_list, kpop_weekly_ranking])
    return korea_news


if __name__ == const.MAIN_FUNCTION:
    data_list = get_data_list()
    print(data_list)
