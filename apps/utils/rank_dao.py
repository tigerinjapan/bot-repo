import apps.utils.constants as const
import apps.utils.function_mongo as func_mongo
import apps.utils.rank_dto as rank_dto

# ランク情報
COLL = const.COLL_RANK_INFO


# ランク情報取得
def get_rank_info(number: int):
    client = func_mongo.db_connect()
    cond = {rank_dto.FI_NUMBER: number}
    rank_info = func_mongo.db_find_one(client, COLL, cond)
    if not rank_info:
        rank_info = const.NONE_CONSTANT
    func_mongo.db_close(client)
    return rank_info


# ランク情報更新（API）
def update_rank_info_of_api(json_data):
    update_data = rank_dto.get_update_data_for_rank_info(json_data)
    client = func_mongo.db_connect()
    cond = {rank_dto.FI_NUMBER: update_data[rank_dto.FI_NUMBER]}
    count = func_mongo.db_count(client, COLL, cond)
    if count == 0:
        func_mongo.db_insert(client, COLL, update_data)
    else:
        func_mongo.db_update(client, COLL, cond, update_data)
    func_mongo.db_close(client)


if __name__ == const.MAIN_FUNCTION:
    number = 1000
    rank_info = get_rank_info(number)
    print(rank_info)
