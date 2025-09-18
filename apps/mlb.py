# 説明: MLB STAT

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_api as func_api
import apps.utils.function_beautiful_soup as func_bs

# アプリケーション名
app_name = func.get_app_name(__file__)

# タイトル
app_title = const.APP_MLB

# ID
TEAM_ID_LAD = "119"
TEAM_LAD = "LAD"
PLAYER_ID_OHTANI = "660271"
PLAYER_NAME_OHTANI = "大谷"


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
    ]  # [ERROR] KOYEB 'NoneType' Object
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


# MLB Stat取得
def get_mlb_stat_of_api(team_id: str = TEAM_ID_LAD, player_id: str = PLAYER_ID_OHTANI):
    stat_data_list = []

    game_data = game_link = const.NONE_CONSTANT

    target_date, japan_date = get_target_date()
    stat_data_list.append(japan_date)

    url = f"{const.URL_MLB_STAT_API}/api/v1/schedule?date={target_date}&sportId=1"
    response_data = func_api.get_response_result(url)
    if response_data:
        game_list = response_data["dates"][0]["games"]
        for game in game_list:
            if game["teams"]["home"]["team"]["link"] == f"/api/v1/teams/{team_id}":
                game_link = game["link"]
                break

    if game_link:
        url = f"{const.URL_MLB_STAT_API}{game_link}"
        response_data = func_api.get_response_result(url)
        if response_data:
            teams_data = response_data["liveData"]["boxscore"]["teams"]
            home_team = response_data["gameData"]["teams"]["home"]["abbreviation"]
            away_team = response_data["gameData"]["teams"]["away"]["abbreviation"]

            away_flg = const.FLG_ON if away_team == TEAM_LAD else const.FLG_OFF
            team_data_div = "home"
            opposing_team = away_team
            if away_flg:
                team_data_div = "away"
                opposing_team = home_team

            stat_data_list.append(f"@{opposing_team}")

            player_data = teams_data[team_data_div]["players"][f"ID{player_id}"]
            if player_data:
                game_data = player_data["stats"]["batting"]["summary"]

    player_name = PLAYER_NAME_OHTANI
    stat_data_list.append(player_name)

    if game_data:
        game_data_2 = game_data.split(" | ")[1].split(const.SYM_COMMA)[0]
        if game_data_2 and "HR" in game_data_2:
            if game_data_2 == "HR":
                home_run = "1"
            else:
                home_run = game_data_2.replace("HR", const.SYM_BLANK)

            game_stat = f"{home_run}本塁打"
        else:
            hit = game_data.split(" | ")[0].split(const.SYM_DASH)[0]
            game_stat = f"{hit}安打"
    else:
        game_stat = "No game"

    stat_data_list.append(game_stat)

    stat_data = const.SYM_SPACE.join(stat_data_list)
    return stat_data


# ゲーム日付取得
def get_target_date():
    japan_date = func.get_now()
    days_num = -1

    if func.get_now(const.DATE_HOUR) < 13:
        japan_date = func.get_calc_date(-1)
        days_num = -2

    # 現地時間
    target_date = func.get_calc_date(days_num)

    # mm/dd/yyyyに変換して出力
    formatted_date = func.convert_date_to_str(target_date, "%m/%d/%Y")

    # mm/ddに変換して出力
    formatted_date_2 = func.convert_date_to_str(japan_date, "%#m/%#d")
    return formatted_date, formatted_date_2


if __name__ == const.MAIN_FUNCTION:
    # item_list = get_item_list()
    # func.print_test_data(item_list)
    stat_data = get_mlb_stat_of_api()
    func.print_test_data(stat_data)
