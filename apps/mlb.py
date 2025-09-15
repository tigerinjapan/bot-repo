# 説明: MLB STAT

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_beautiful_soup as func_bs

# アプリケーション名
app_name = func.get_app_name(__file__)

# タイトル
app_title = const.APP_MLB


# アイテムリスト取得
def get_item_list():
    item_list = get_last_game_info()
    # item_list = get_ranking_info()
    return item_list


# ランキング情報取得
def get_ranking_info():
    player_list = []

    url = f"{const.URL_MLB}/stats/ops"
    url = f"{const.URL_MLB}/stats/pitching/whip?sortState=asc"

    soup = func_bs.get_elem_from_url(url, attr_val="table-scroller-GsCM0EhI scroller")
    player_info_list = func_bs.find_elem_by_attr(
        soup,
        attr_div=const.ATTR_CLASS,
        attr_val="top-wrapper-TqtRaIeD",
        list_flg=const.FLG_ON,
    )[0:5]
    for player_info in player_info_list:
        player_name = func_bs.find_elem_by_attr(
            player_info, tag=const.TAG_A, attr_div="aria-label"
        )
        player_list.append(player_name)
    return player_list


# 直近の試合情報取得
def get_last_game_info(player_div: int = const.NUM_ONE) -> tuple[str, str]:
    player_name = "大谷"
    url_param = "shohei-ohtani-660271#"

    if player_div == const.NUM_TWO:
        player_name = "Kim"
        url_param = "hyeseong-kim-808975"
    elif player_div == const.NUM_THREE:
        player_name = "Lee"
        url_param = "jung-hoo-lee-808982"

    list_no = 1 if player_div == const.NUM_ONE else 2

    url = f"{const.URL_MLB}/player/{url_param}"
    attr_val = "player-splits--last player-splits--last-3 has-xgames"
    soup = func_bs.get_elem_from_url(url, attr_val=attr_val, list_flg=const.FLG_ON)[
        list_no
    ] # TODO: [ERROR] KOYEB 'NoneType' Object
    game = get_text_from_info(soup).replace(const.SYM_SPACE, const.SYM_BLANK)

    game_info = []
    hit = get_text_from_info(soup, const.NUM_THREE)
    if hit == str(const.NUM_ZERO):
        game_info = "no hit"
    else:
        game_info = f"{hit}H"
        home_run = get_text_from_info(soup, const.NUM_FOUR)
        if home_run != str(const.NUM_ZERO):
            game_info = f"{home_run}HR"

    last_game_info = f"<{player_name}> {game} {game_info}"
    return last_game_info, url


# テキスト取得
def get_text_from_info(soup, div=const.NUM_ZERO):
    attr_val = "col-0 row-0 td--text" if div == const.NUM_ZERO else f"col-{div} row-0"
    soup = func_bs.find_elem_by_attr(soup, attr_div=const.ATTR_CLASS, attr_val=attr_val)
    text = func_bs.get_text_from_soup(soup)
    return text


if __name__ == const.MAIN_FUNCTION:
    item_list = get_item_list()
    func.print_test_data(item_list)
