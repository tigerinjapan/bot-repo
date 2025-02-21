# 説明：韓国ニュース

import news
import utils.constants as const
import utils.function as func

# アプリケーション名
app_name = func.get_app_name(__file__)

# タイトル
app_title = "韓国" + const.STR_NEWS_JA


# データリスト取得
def get_data_list() -> list[tuple[list[str], list[str]]]:
    data_list = news.get_data_list(news.DIV_KOREA_NEWS_LIST)
    data_list += get_korea_weekly_ranking()
    return data_list


# 韓国週間ランキング取得
def get_korea_weekly_ranking(div: str = "kpop"):
    korea_news = []
    kpop_weekly_ranking = []

    url = f"{news.URL_WOWKOREA}/ranking/weekly/{div}/"
    elem_list = news.get_elem_list(news.DIV_KPOP_RANKING, url)[:const.NUM_PRINT_CNT]

    for elem in elem_list:
        text_data = elem.text
        text_list = text_data.split("」")
        singer = text_list[1]
        song = (
            text_list[0].replace("「 ", const.SYM_BLANK).replace("「", const.SYM_BLANK)
        )
        ranking_info = [f"{singer} - {song}"]
        kpop_weekly_ranking.append(ranking_info)

    col_list = [news.DIV_KPOP_RANKING]
    korea_news.append([col_list, kpop_weekly_ranking])
    return korea_news
    

if __name__ == const.MAIN_FUNCTION:
    data_list = get_data_list()
    print(data_list)
    # print(data_list[0][1])
