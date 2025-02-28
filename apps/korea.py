# 説明：韓国ニュース

import apps.news as news
import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_beautiful_soup as func_bs

# アプリケーション名
app_name = func.get_app_name(__file__)

# タイトル
app_title = const.STR_KOREA_JA + const.STR_NEWS_JA

# カラムリスト
col_list = news.col_list

# ランキング区分リスト
LIST_RANKING_DIV = [const.STR_KPOP, const.STR_DRAMA]


# アイテムリスト取得
def get_item_list():
    item_list = news.get_item_list(news.DIV_KOREA_NEWS_LIST)
    return item_list


# データリスト取得
def get_data_list() -> list:
    data_list = []

    data_val_list = []
    for div in LIST_RANKING_DIV:
        weekly_ranking = get_weekly_ranking(div)
        data_val = [raking_info[0] for raking_info in weekly_ranking]
        data_val_list.append(data_val)

    column_list = [news.DIV_WEEKLY_RANKING.format(div) for div in LIST_RANKING_DIV]
    data_val_list = [list(data_val) for data_val in zip(*data_val_list)]
    data_info_list = [column_list, data_val_list]
    data_list.append(data_info_list)
    return data_list


# 週間ランキング取得
def get_weekly_ranking(div: str = const.STR_KPOP):
    weekly_ranking = []

    url = f"{news.URL_WOWKOREA}/ranking/weekly/{div.lower()}/"

    elem_list = news.get_elem_list(news.DIV_KPOP_RANKING, url)

    if div == const.STR_DRAMA:
        attr_val = "card-body pt-3 pt-lg-0"
        elem_list = func_bs.get_elem_from_url(
            url, attr_val=attr_val, list_flg=const.FLG_ON
        )

    if not elem_list:
        return weekly_ranking

    for elem in elem_list[: const.MAX_DISPLAY_CNT]:
        if div == const.STR_KPOP:
            if not elem:
                break
            text_data = elem.text
            text_list = text_data.split("」")
            singer = text_list[1]
            song = (
                text_list[0]
                .replace("「 ", const.SYM_BLANK)
                .replace("「", const.SYM_BLANK)
            )
            ranking_info = [f"{singer} - {song}"]

        elif div == const.STR_DRAMA:
            h2_elem = func_bs.find_elem_by_attr(elem, tag=const.TAG_H2)
            title = h2_elem.text
            a_href = func_bs.get_link_from_soup(h2_elem)
            link = f"{news.URL_WOWKOREA}{a_href}"
            ul_elem = func_bs.find_elem_by_attr(elem, tag=const.TAG_UL)
            li_elem_list = func_bs.find_elem_by_attr(
                ul_elem, tag=const.TAG_LI, list_flg=const.FLG_ON
            )
            li_elem = li_elem_list[4]
            a_elem_list = func_bs.find_elem_by_attr(
                li_elem, tag=const.TAG_A, list_flg=const.FLG_ON
            )[:2]
            a_elem_text = [a_elem.text for a_elem in a_elem_list]
            cast = const.SYM_SLASH.join(a_elem_text)
            # ranking_info = [title, cast, link]
            ranking_info = [f"{title} - {cast}"]

        weekly_ranking.append(ranking_info)

    return weekly_ranking


if __name__ == const.MAIN_FUNCTION:
    data_list = get_data_list()
    print(data_list)
