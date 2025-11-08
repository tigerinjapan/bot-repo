"""
掲示板情報DAO
"""

import apps.utils.board_dto as board_dto
import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_mongo as func_mongo
import apps.utils.mongo_constants as mongo_const
import apps.utils.sequence_dao as seq_dao


def get_board_info():
    """
    掲示板データ取得
    """
    board_data = []

    client = func_mongo.db_connect()

    # 取得対象
    target_date = func.get_calc_date(const.MAX_TARGET_DAYS_BOARD)

    cond = {
        mongo_const.OPERATOR_OR: [
            {
                mongo_const.FI_STATUS: {
                    mongo_const.OPERATOR_NOT_EQUAL: const.STATUS_DONE
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


def insert_board_data_of_api(json_data):
    """
    掲示板データ登録（API）
    """
    client = func_mongo.db_connect()
    data_list = json_data[const.STR_DATA]
    inc_val = len(data_list)
    seq = seq_dao.get_sequence(client, const.APP_BOARD)

    insert_data_list = []
    message_data_list = []
    for idx, data in enumerate(data_list):
        seq_val = seq + idx
        update_data = board_dto.get_update_data_for_board_info(data, seq_val)
        insert_data_list.append(update_data)

        if update_data[mongo_const.FI_USER_NAME] != const.AUTH_ADMIN:
            board_data = board_dto.get_board_data(update_data)
            message_data = f"[{board_data[mongo_const.FI_SEQ]}] {board_data[mongo_const.FI_CONTENTS]}"
            message_data_list.append(message_data)

    func_mongo.db_insert(
        client, mongo_const.COLL_BOARD, insert_data_list, many_flg=const.FLG_ON
    )

    seq = seq_dao.update_sequence(client, const.APP_BOARD, inc_val)
    func_mongo.db_close(client)

    return message_data_list


def update_board_status(json_data):
    """
    ステータス更新
    """
    seq = int(json_data[const.STR_TITLE])
    remark = json_data[const.MSG_TYPE_TXT]
    status = int(json_data[const.STR_STATUS])

    client = func_mongo.db_connect()
    cond = {mongo_const.FI_SEQ: seq}
    update_data = {
        mongo_const.FI_REMARK: remark,
        mongo_const.FI_STATUS: status,
        mongo_const.FI_UPDATE_DATE: func.get_now(),
    }
    func_mongo.db_update(client, mongo_const.COLL_BOARD, cond, update_data)
    func_mongo.db_close(client)


if __name__ == const.MAIN_FUNCTION:
    board_info = get_board_info()
    print(board_info)
