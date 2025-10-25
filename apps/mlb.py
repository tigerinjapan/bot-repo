# 説明: MLB STAT

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_api as func_api
import apps.utils.function_beautiful_soup as func_bs

from apps.utils.message_constants import MSG_ERR_DATA_NOT_EXIST

# タイトル
app_title = const.APP_MLB


# アイテムリスト取得
def get_item_list():
    item_list = get_last_game_info()
    # item_list = get_ranking_info()
    return item_list


# MLB Stat取得
def get_mlb_game_data(
    team_id: int = const.TEAM_ID_LAD,
    all_flg: bool = const.FLG_OFF,
) -> list[str]:
    stat_data_list = []

    game_data, game_date, game_score, home_away_div = get_mlb_stat_of_api(team_id)
    if game_data:
        if not all_flg:
            stat_data_list.append(game_date)

        box_score_data = game_data["liveData"]["boxscore"]
        teams_data = box_score_data["teams"]

        home_away = get_home_away(game_data)
        stat_data_list.append(home_away)

        stat_data_list.append(game_score)

        my_team_data = teams_data[home_away_div]
        batters = my_team_data["batters"]
        pitchers = my_team_data["pitchers"]

        idx = const.LIST_TEAM_ID.index(team_id)
        player_id_list = const.LIST_PLAYER_ID[idx]

        if not all_flg:
            player_id_list = player_id_list[:1]

        for player_id in player_id_list:
            if player_id in batters or player_id in pitchers:
                players_data = game_data["gameData"]["players"]
                for key, value in players_data.items():
                    if value.get("id") == player_id:
                        stat_data_list.append(const.SYM_NEW_LINE)
                        player_name = value.get("boxscoreName")
                        stat_data_list.append(player_name)
                        break

                player_data = my_team_data["players"][f"ID{player_id}"]["stats"]
                if player_data:
                    game_stat = get_game_stats(player_data, all_flg)
                    stat_data_list.extend(game_stat)

        if all_flg:
            player_of_game_data = get_player_of_game_data(team_id, game_data)
            stat_data_list.append(player_of_game_data)

    stat_data = const.SYM_SPACE.join(stat_data_list)
    return stat_data


# 今日のヒーロー
def get_player_of_game_data(
    team_id: int = const.TEAM_ID_LAD, game_data=const.NONE_CONSTANT
) -> str:
    stat_data_list = ["[POG]"]

    if game_data:
        stat_data_list.insert(0, const.SYM_NEW_LINE)
    else:
        game_data, game_date, game_score, home_away_div = get_mlb_stat_of_api(team_id)

        if not game_data:
            return const.SYM_BLANK

        stat_data_list.append(game_date)

        home_away = get_home_away(game_data)
        stat_data_list.append(home_away)

        stat_data_list.append(game_score)

    if game_data:
        box_score_data = game_data["liveData"]["boxscore"]
        top_performer_data = box_score_data["topPerformers"][0]["player"]
        person_data = top_performer_data["person"]

        player_id = person_data["id"]

        idx = const.LIST_TEAM_ID.index(team_id)
        player_id_list = const.LIST_PLAYER_ID[idx]
        if player_id in player_id_list:
            return const.SYM_BLANK

        player_name = person_data["boxscoreName"]
        stat_data_list.append(player_name)

        player_of_game_data = get_game_stats(top_performer_data["stats"], const.FLG_ON)
        stat_data_list.extend(player_of_game_data)

    stat_data = const.SYM_SPACE.join(stat_data_list)
    return stat_data


# MLB Stat取得
def get_mlb_stat_of_api(team_id: int):
    game_data = const.NONE_CONSTANT
    game_date = game_score = home_away_div = const.SYM_BLANK

    team_schedule_url = (
        f"{const.URL_MLB_STAT_API}/api/v1/schedule?sportId=1&teamId={team_id}"
    )
    team_schedule_data = func_api.get_response_result(team_schedule_url)
    if team_schedule_data:
        team_schedule_dates = team_schedule_data["dates"]
        if team_schedule_dates:
            games = team_schedule_dates[0]["games"][0]

            status = games["status"]["detailedState"]
            if status in ["In Progress", "Final"]:
                game_date = get_game_date(games["gameDate"])
                game_link = games["link"]

                home_team_data = games["teams"]["home"]
                away_team_data = games["teams"]["away"]

                if home_team_data["team"]["id"] == team_id:
                    home_away_div = "home"
                else:
                    home_away_div = "away"

                home_score = home_team_data["score"]
                away_score = away_team_data["score"]
                game_score = f"[{status[:2]}] {away_score}:{home_score}"

                game_url = f"{const.URL_MLB_STAT_API}{game_link}"
                response_data = func_api.get_response_result(game_url)
                if response_data:
                    game_data = response_data

            else:
                info_msg = f"{team_id} {status}"
                func.print_info_msg(const.APP_MLB, info_msg)

    if not game_data:
        func.print_info_msg(const.APP_MLB, MSG_ERR_DATA_NOT_EXIST)

    return game_data, game_date, game_score, home_away_div


# ホーム&アウエー
def get_home_away(game_data) -> str:
    team_data = game_data["gameData"]["teams"]
    home_team = team_data["home"]["abbreviation"]
    away_team = team_data["away"]["abbreviation"]
    home_away = f"{away_team}@{home_team}"
    return home_away


# ゲームスタッツ取得
def get_game_stats(player_data, all_flg: bool = const.FLG_OFF) -> list[str]:
    game_stats = []
    batting_data = pitching_data = {}

    stats_batting = player_data["batting"]
    stats_pitching = player_data["pitching"]
    if stats_batting:
        batting_data = stats_batting["summary"]
    if stats_pitching:
        pitching_data = stats_pitching["summary"]

    if batting_data:
        if all_flg:
            batting_stat = batting_data

        else:
            batting_data = batting_data.split(" | ")
            hit = batting_data[0].split(const.SYM_DASH)[0]
            batting_stat = f"{hit} H"

            if const.NUM_ZERO < int(hit):
                home_run = batting_data[1].split(const.SYM_COMMA)[0]
                if home_run and "HR" in home_run:
                    home_run_stat = home_run[0]
                    if home_run == "HR":
                        home_run_stat = str(const.NUM_ONE)
                    batting_stat += f" ({home_run_stat} HR)"

        game_stats.append(batting_stat)

    if pitching_data:
        if all_flg:
            if batting_data:
                game_stats.append(const.SYM_NEW_LINE + const.SYM_TAB)
            pitching_stat = pitching_data

        else:
            pitching_stat = pitching_data.split(const.SYM_COMMA)[:2]
            pitching_stat = const.SYM_BLANK.join(pitching_stat)

        game_stats.append(pitching_stat)

    return game_stats


# ゲーム日付取得
def get_game_date(game_date: str) -> str:
    jst_date = const.SYM_BLANK

    # 日付型へ変換
    game_date = func.convert_str_to_date(game_date)

    # タイムゾーンを削除
    game_date_naive = game_date.replace(tzinfo=const.NONE_CONSTANT)

    # 日本時間に計算
    calc_date = func.get_calc_date(9, const.DATE_HOUR, game_date_naive)

    jst_date = func.convert_date_to_str(calc_date, const.DATE_FORMAT_MMDD_SLASH_NO_ZERO)
    return jst_date


# ランキング情報取得
def get_ranking_info():
    player_list = []

    url = f"{const.URL_MLB}/stats/ops"
    url = f"{const.URL_MLB}/stats/pitching/whip?sortState=asc"

    soup = func_bs.get_elem_from_url(url, attr_val="table-scroller-GsCM0EhI scroller")
    player_info_list = func_bs.find_elem_by_class(
        soup, "top-wrapper-TqtRaIeD", list_flg=const.FLG_ON
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
    elem = func_bs.find_elem_by_class(soup, attr_val)
    text = func_bs.get_text_from_soup(elem)
    return text


if __name__ == const.MAIN_FUNCTION:
    # item_list = get_item_list()
    # func.print_test_data(item_list)
    stat_data = get_mlb_game_data()
    func.print_test_data(stat_data)
