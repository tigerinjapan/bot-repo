from datetime import datetime, timedelta

import apps.utils.constants as const
import apps.utils.function_mongo as func_mongo
import apps.utils.board_dto as dto
import apps.utils.sequence_dao as seq_dao

# 掲示板情報
COLL = const.COLL_BOARD


# 掲示板データ取得
def get_board_info():
    board_data = []

    client = func_mongo.db_connect()

    # 30日前のデータ
    target_date = datetime.now() + timedelta(days=-30)

    cond = {
        "$or": [
            {dto.FI_STATUS: {"$ne": dto.STATUS_DONE}},
            {dto.FI_UPDATE_DATE: {"$gte": target_date}},
        ]
    }
    sort = {dto.FI_STATUS: 1, dto.FI_APP: 1, dto.FI_UPDATE_DATE: -1}

    result = func_mongo.db_find(client, COLL, cond, sort=sort)
    if result:
        for board_info in result:
            json_data = dto.get_board_data(board_info)
            board_data.append(json_data)

    func_mongo.db_close(client)
    return board_data


# データ登録（API）
def insert_board_data_of_api(json_data):
    client = func_mongo.db_connect()
    data_list = json_data[const.STR_DATA]
    seq_val = len(data_list)
    seq = seq_dao.get_sequence_and_update(client, const.APP_BOARD, seq_val)

    for idx, data in enumerate(data_list):
        seq += idx
        update_data = dto.get_update_data_for_board_info(data, seq)
        func_mongo.db_insert(client, COLL, update_data)
    func_mongo.db_close(client)


# ステータス更新
def update_board_status(seq: str, status: int = dto.STATUS_DONE):
    client = func_mongo.db_connect()
    cond = {dto.FI_SEQ: int(seq)}
    update_data = {dto.FI_STATUS: status}
    func_mongo.db_update(client, COLL, cond, update_data)
    func_mongo.db_close(client)


if __name__ == const.MAIN_FUNCTION:
    board_info = get_board_info()
    print(board_info)
