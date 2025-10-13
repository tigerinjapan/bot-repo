# 説明: 掲示板情報DAO

import apps.utils.board_dto as board_dto
import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_mongo as func_mongo
import apps.utils.mongo_constants as mongo_const
import apps.utils.sequence_dao as seq_dao


# 掲示板データ取得
def get_board_info():
    board_data = []

    client = func_mongo.db_connect()

    # 30日前のデータ
    target_date = func.get_calc_date(-30)

    cond = {
        mongo_const.OPERATOR_OR: [
            {
                mongo_const.FI_STATUS: {
                    mongo_const.OPERATOR_NOT_EQUAL: board_dto.STATUS_DONE
                }
            },
            {
                mongo_const.FI_UPDATE_DATE: {
                    mongo_const.OPERATOR_GREATER_THAN_OR_EQUAL: target_date
                }
            },
        ]
    }
    sort = {
        mongo_const.FI_STATUS: 1,
        mongo_const.FI_UPDATE_DATE: -1,
        mongo_const.FI_USER_NAME: -1,
    }

    result = func_mongo.db_find(client, mongo_const.COLL_BOARD, cond, sort=sort)
    if result:
        for board_info in result:
            json_data = board_dto.get_board_data(board_info)
            board_data.append(json_data)

    func_mongo.db_close(client)
    return board_data


# データ登録（API）
def insert_board_data_of_api(json_data):
    client = func_mongo.db_connect()
    data_list = json_data[const.STR_DATA]
    inc_val = len(data_list)
    seq = seq_dao.get_sequence(client, const.APP_BOARD)

    for idx, data in enumerate(data_list):
        seq_val = seq + idx
        update_data = board_dto.get_update_data_for_board_info(data, seq_val)
        func_mongo.db_insert(client, mongo_const.COLL_BOARD, update_data)

    seq = seq_dao.update_sequence(client, const.APP_BOARD, inc_val)
    func_mongo.db_close(client)


# ステータス更新
def update_board_status(json_data):
    seq = int(json_data[const.STR_TITLE])
    remark = json_data[const.INPUT_TYPE_TEXT]
    status = int(json_data[const.STR_STATUS])

    client = func_mongo.db_connect()
    cond = {mongo_const.FI_SEQ: seq}
    update_data = {
        mongo_const.FI_REMARK: remark,
        mongo_const.FI_STATUS: status,
        mongo_const.FI_UPDATE_DATE: func.get_now(),
    }
    func_mongo.db_update_one(client, mongo_const.COLL_BOARD, cond, update_data)
    func_mongo.db_close(client)


if __name__ == const.MAIN_FUNCTION:
    board_info = get_board_info()
    print(board_info)
