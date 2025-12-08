"""
ランク情報DAO
"""

import apps.utils.constants as const
import apps.utils.function_mongo as func_mongo
import apps.utils.mongo_constants as mongo_const
import apps.utils.rank_dto as rank_dto


def get_rank_info_list(number_list: list[int]):
    """
    ランク情報取得: number
    """
    rank_info_list = []

    client = func_mongo.db_connect()
    cond = {mongo_const.FI_NUMBER: {mongo_const.OPERATOR_IN: number_list}}
    result = func_mongo.db_find(
        client, mongo_const.COLL_RANK_INFO, cond, debug_flg=const.FLG_OFF
    )
    for rank_info in result:
        rank_info_data = rank_dto.get_rank_info_data(rank_info)
        rank_info_list.append(rank_info_data)

    func_mongo.db_close(client)
    return rank_info_list


def get_rank_info_top():
    """
    ランキング情報取得: number TODO: 現在使用箇所無し
    """
    # 5桁で「.」が含まれている
    cond = {
        mongo_const.FI_RANK_TIME: {
            mongo_const.OPERATOR_REGEX: "^.{5}$",
            mongo_const.OPERATOR_REGEX: "\\.",
        }
    }

    select_data = {
        mongo_const.FI_ID: 0,
        mongo_const.FI_NUMBER: 1,
        mongo_const.FI_RANK_TIME: 1,
        mongo_const.FI_USER_NAME: 1,
        mongo_const.FI_UPDATE_DATE: {
            "$dateToString": {"format": "%Y/%m/%d %H:%M", "date": "$dUpdateDate"}
        },
    }
    sort = {
        mongo_const.FI_RANK_TIME: mongo_const.SORT_ASCENDING,
        mongo_const.FI_UPDATE_DATE: mongo_const.SORT_DESCENDING,
    }

    rank_top = get_rank_top(
        cond, select_data, sort, coll_name=mongo_const.COLL_RANK_INFO
    )
    return rank_top


def get_ranking_top(app_name: str):
    """
    ランキング情報取得: sudoku, itQuiz
    """
    cond = {mongo_const.FI_DIV: app_name}

    select_data = {
        mongo_const.FI_ID: 0,
        mongo_const.FI_RANK: 1,
        mongo_const.FI_SCORE: 1,
        mongo_const.FI_USER_NAME: 1,
        mongo_const.FI_UPDATE_DATE: {
            "$dateToString": {
                "format": "%Y/%m/%d %H:%M",
                "date": "$dUpdateDate",
            }
        },
    }
    sort = {
        mongo_const.FI_RANK: mongo_const.SORT_ASCENDING,
        mongo_const.FI_UPDATE_DATE: mongo_const.SORT_DESCENDING,
    }

    ranking_top = get_rank_top(cond, select_data, sort)
    return ranking_top


def get_rank_top(
    cond,
    select_data,
    sort,
    limit_cnt: int = 5,
    coll_name: str = mongo_const.COLL_RANKING,
    json_flg: bool = const.FLG_ON,
):
    """
    [共通] ランキング情報取得: sudoku, itQuiz
    """
    client = func_mongo.db_connect()
    rank_info_list = func_mongo.db_find(
        client, coll_name, cond, select_data, sort
    ).limit(limit_cnt)

    rank_top = []
    for rank_info in rank_info_list:
        if json_flg:
            rank_info = rank_dto.get_ranking_data(rank_info)

        rank_top.append(rank_info)

    func_mongo.db_close(client)

    return rank_top


def update_rank_info_of_api(json_data):
    """
    ランク情報更新 (API): number
    """
    coll_rank = mongo_const.COLL_RANK_INFO
    update_data = rank_dto.get_rank_info_data(json_data, update_flg=const.FLG_ON)

    client = func_mongo.db_connect()
    cond = {mongo_const.FI_NUMBER: update_data[mongo_const.FI_NUMBER]}
    count = func_mongo.db_count(client, coll_rank, cond)
    if count == 0:
        func_mongo.db_insert(client, coll_rank, update_data)
    else:
        func_mongo.db_update(client, coll_rank, cond, update_data)
    func_mongo.db_close(client)


def update_ranking_of_api(app_name: str, json_data):
    """
    ランキング情報更新 (API): sudoku, itQuiz
    """
    coll_rank = mongo_const.COLL_RANKING
    insert_data, target_rank, target_score = rank_dto.get_update_data_for_ranking(
        app_name, json_data
    )

    client = func_mongo.db_connect()

    # 1. 同じスコアを持つドキュメントが存在するかを確認
    existing_score_count = func_mongo.db_count(
        client, coll_rank, {mongo_const.FI_SCORE: target_score}
    )

    # 2. 更新条件の設定
    if 0 < existing_score_count:
        # 重複ありの場合
        update_rank = target_rank + 1
    else:
        # 重複なしの場合
        update_rank = target_rank

    # 3. 更新
    cond = {
        mongo_const.FI_DIV: app_name,
        mongo_const.FI_RANK: {mongo_const.OPERATOR_GREATER_THAN_OR_EQUAL: update_rank},
    }
    update_data = {mongo_const.OPERATOR_INCREMENT: {mongo_const.FI_RANK: 1}}
    func_mongo.db_update_many(client, coll_rank, cond, update_data)

    # 4. 登録
    func_mongo.db_insert(client, coll_rank, insert_data)

    func_mongo.db_close(client)


if __name__ == const.MAIN_FUNCTION:
    app_name = const.APP_SUDOKU
    ranking_top = get_ranking_top(app_name)
    print(ranking_top)
