# 説明: ドラマランキング

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_beautiful_soup as func_bs

# アプリケーション名
app_name = func.get_app_name(__file__)

# タイトル
app_title = const.STR_DRAMA_JA + const.STR_RANKING_JA

# カラムリスト
col_list = [const.STR_IMG_JA, const.STR_CONTENTS_JA]

# ランキング区分
LIST_RANKING_WEEKLY = [const.APP_DRAMA]


# アイテムリスト取得
def get_item_list():
    item_list = []

    for div_weekly in LIST_RANKING_WEEKLY:
        ranking_info = get_weekly_ranking(div_weekly)
        item_list += ranking_info

    return item_list


# 週間ランキング取得
def get_weekly_ranking(div: str):
    weekly_ranking = []

    if div == const.APP_DRAMA:
        elem_val_list = get_elem_val_list(div)
        elem_list = zip(*elem_val_list)

    if not elem_list:
        return weekly_ranking

    for img, elem in elem_list:
        ranking_info = const.SYM_BLANK

        if div == const.APP_DRAMA:
            img_path = const.URL_WOWKOREA + img.get("data-src")
            img_tag = func.get_img_tag(img_path)
            h2_elem = func_bs.find_elem_by_attr(elem, tag=const.TAG_H2)
            title = f"<b>{h2_elem.text}</b>"
            ul_elem = func_bs.find_elem_by_attr(elem, tag=const.TAG_UL)
            li_elem_list = func_bs.find_elem_by_attr(
                ul_elem, tag=const.TAG_LI, list_flg=const.FLG_ON
            )
            if li_elem_list:
                genre_text = li_elem_list[0].get_text(strip=const.FLG_ON)
                genre = genre_text.split(const.SYM_COMMA_JAP)[0]
                cast_text = li_elem_list[4].get_text(strip=const.FLG_ON)
                cast = cast_text.split(const.SYM_COMMA_JAP)[0]
                contents_tag = ["<p>", title, genre, cast, "</p>"]
                contents = const.SYM_NEW_LINE.join(contents_tag)
                ranking_info = [img_tag, contents]

        if ranking_info:
            weekly_ranking.append(ranking_info)

    return weekly_ranking


# 要素リスト取得
def get_elem_val_list(div: str):
    elem_val_list = []

    url = f"{const.URL_WOWKOREA}/ranking/weekly/{div}/"
    soup = func_bs.get_soup(url)

    attr_val_list = ["img-fluid lazy", "card-body pt-3 pt-lg-0"]
    for attr_val in attr_val_list:
        elem_list = func_bs.find_elem_by_attr(
            soup, attr_div=const.ATTR_CLASS, attr_val=attr_val, list_flg=const.FLG_ON
        )[: const.MAX_DISPLAY_CNT]
        elem_val_list.append(elem_list)

    return elem_val_list


if __name__ == const.MAIN_FUNCTION:
    item_list = get_item_list()
    func.print_test_data(item_list)
