# 説明: ランク情報DAO

import apps.utils.constants as const
import apps.utils.function_mongo as func_mongo
import apps.utils.mongo_constants as mongo_const
import apps.utils.rank_dto as rank_dto

# ランク情報
COLL = mongo_const.COLL_RANK_INFO


# ランク情報取得
def get_rank_info(number: int):
    client = func_mongo.db_connect()
    cond = {mongo_const.FI_NUMBER: number}
    rank_info = func_mongo.db_find_one(client, COLL, cond)
    if not rank_info:
        rank_info = const.NONE_CONSTANT
    func_mongo.db_close(client)
    return rank_info


# ランク情報更新（API）
def update_rank_info_of_api(json_data):
    update_data = rank_dto.get_update_data_for_rank_info(json_data)
    client = func_mongo.db_connect()
    cond = {mongo_const.FI_NUMBER: update_data[mongo_const.FI_NUMBER]}
    count = func_mongo.db_count(client, COLL, cond)
    if count == 0:
        func_mongo.db_insert(client, COLL, update_data)
    else:
        func_mongo.db_update(client, COLL, cond, update_data)
    func_mongo.db_close(client)


# ランキング情報取得
def get_rank_top_5(app_name: str = const.APP_NUMBER):
    # 5桁で「.」が含まれている
    conditions = {
        mongo_const.OPERATOR_REGEX: "^.{5}$",
        mongo_const.OPERATOR_REGEX: "\\.",
    }

    if app_name == const.APP_IT_QUIZ:
        # 数値のみ
        conditions.update({mongo_const.OPERATOR_REGEX: "^\\d+$"})

    cond = {mongo_const.FI_RANK_TIME: conditions}
    select_data = {
        mongo_const.FI_ID: 0,
        mongo_const.FI_NUMBER: 1,
        mongo_const.FI_RANK_TIME: 1,
        mongo_const.FI_USER_NAME: 1,
        mongo_const.FI_UPDATE_DATE: {
            "$dateToString": {"format": "%Y/%m/%d %H:%M", "date": "$dUpdateDate"}
        },
    }
    sort = {mongo_const.FI_RANK_TIME: 1, mongo_const.FI_UPDATE_DATE: -1}

    client = func_mongo.db_connect()
    rank_info_list = func_mongo.db_find(client, COLL, cond, select_data, sort).limit(5)

    rank_top_5 = []
    for rank_info in rank_info_list:
        rank_top_5.append(rank_info)

    func_mongo.db_close(client)
    return rank_top_5


if __name__ == const.MAIN_FUNCTION:
    rank_top_5 = get_rank_top_5(const.APP_IT_QUIZ)
    print(rank_top_5)
