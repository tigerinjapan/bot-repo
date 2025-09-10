import apps.utils.constants as const
import apps.utils.function_mongo as func_mongo
import apps.utils.board_dto as dto

# 掲示板情報
COLL = const.COLL_BOARD

# ステータス
STS_NEW = "new"


# 掲示板データ取得
def get_board_info(status: str = STS_NEW):
    client = func_mongo.db_connect()
    cond = {dto.FI_STATUS: status}  # TODO: 条件検討要（完了以外、または直近1ヶ月）
    select_data = {
        "_id": 0,
        "sApp": 1,
        "sCategory": 1,
        "sContents": 1,
        "sRemark": 1,
        "sStatus": 1,
        "sUserName": 1,
        "dUpdateDate": 1,
    }
    result = func_mongo.db_find(client, COLL, cond, select_data)
    board_data = []
    if result:
        for board_info in result:
            board_data.append(board_info)

    func_mongo.db_close(client)
    return board_data


# データ登録（API）
def insert_board_data_of_api(json_data):
    client = func_mongo.db_connect()
    data_list = json_data[const.STR_DATA]
    for data in data_list:
        update_data = dto.get_update_data_for_board_info(data)
        func_mongo.db_insert(client, COLL, update_data)
    func_mongo.db_close(client)


if __name__ == const.MAIN_FUNCTION:
    status = "new"
    board_info = get_board_info(status)
    print(board_info)
