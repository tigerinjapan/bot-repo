import apps.utils.constants as const
import apps.utils.function_mongo as func_mongo
import apps.utils.board_dto as dto

# 掲示板情報
COLL = const.COLL_BOARD


# 掲示板データ取得
def get_board_info(status: str):
    client = func_mongo.db_connect()
    cond = {dto.FI_STATUS: status}  # TODO: 条件検討要（完了以外、または直近1ヶ月）
    result = func_mongo.db_find(client, COLL, cond)
    if not result:
        result = const.NONE_CONSTANT
    func_mongo.db_close(client)
    return result


# データ登録（API）
def insert_board_data_of_api(json_data):
    client = func_mongo.db_connect()
    data_list = json_data[const.STR_DATA]
    for data in data_list:
        update_data = dto.get_update_data_for_board_info(data)
        func_mongo.db_insert(client, COLL, update_data)
    func_mongo.db_close(client)


if __name__ == const.MAIN_FUNCTION:
    project = const.APP_TRIP
    board_info = get_board_info(project)
    print(board_info)
