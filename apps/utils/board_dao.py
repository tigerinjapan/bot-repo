"""
掲示板情報DAO
"""

import apps.utils.board_dto as board_dto
import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_mongo as func_mongo
import apps.utils.mongo_constants as mongo_const
import apps.utils.sequence_dao as seq_dao


def get_board_info(user_div: str = const.AUTH_DEV, json_flg: bool = const.FLG_ON):
    """
    掲示板データ取得
    """
    board_data_list = []

    client = func_mongo.db_connect()

    # 取得対象：直近4週間データ
    target_date = func.get_calc_date(-const.MAX_TARGET_DAYS_BOARD)

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
    if user_div != const.AUTH_ADMIN:
        add_cond = {
            mongo_const.FI_USER_NAME: {mongo_const.OPERATOR_NOT_EQUAL: const.AUTH_ADMIN}
        }
        cond.update(add_cond)

    sort = {
        mongo_const.FI_STATUS: mongo_const.SORT_ASCENDING,
        mongo_const.FI_UPDATE_DATE: mongo_const.SORT_DESCENDING,
        mongo_const.FI_SEQ: mongo_const.SORT_DESCENDING,
    }

    result = func_mongo.db_find(client, mongo_const.COLL_BOARD, cond, sort=sort)
    if result:
        for board_info in result:
            if json_flg:
                board_data = board_dto.get_board_data(board_info)
            else:
                board_data = board_info[mongo_const.FI_CONTENTS]
            board_data_list.append(board_data)

    func_mongo.db_close(client)
    return board_data_list


def insert_board_data_of_api(json_data):
    """
    掲示板データ登録 (API)
    """
    client = func_mongo.db_connect()
    data_list = json_data[const.STR_DATA]
    inc_val = len(data_list)
    seq = get_board_seq(client)

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


def get_board_seq(client, coll: str = mongo_const.COLL_BOARD) -> int:
    """
    掲示板連番取得 (データ登録用)
    """
    # すべての連番を取得し、ソート
    select_data = {mongo_const.FI_SEQ: 1, mongo_const.FI_ID: 0}
    sort = {mongo_const.FI_SEQ: mongo_const.ASCENDING}
    cursor = func_mongo.db_find(client, coll, select_data=select_data, sort=sort)
    current_seqs = [doc[mongo_const.FI_SEQ] for doc in cursor]

    updates_to_perform = {}
    new_seq = current_seqs[0]

    for old_seq in current_seqs:
        if old_seq != new_seq:
            updates_to_perform[old_seq] = new_seq

        new_seq += 1

    # 大きい連番から順に操作をリストに追加
    sorted_updates = sorted(
        updates_to_perform.items(), key=lambda item: item[0], reverse=const.FLG_ON
    )

    bulk_operations = []

    for old_seq, new_seq in sorted_updates:
        # UpdateOne(検索条件, 更新内容) を使って操作オブジェクトを作成
        cond = {mongo_const.FI_SEQ: old_seq}
        update_data = {mongo_const.FI_SEQ: new_seq}
        operation = func_mongo.get_update_one(cond, update_data)
        bulk_operations.append(operation)

    func_mongo.bulk_write(client, coll, bulk_operations)
    return new_seq


def update_board_status(json_data):
    """
    ステータス更新
    """
    seq = int(json_data[const.STR_TITLE])
    remark = json_data[const.MSG_TYPE_TXT]
    status = int(json_data[const.STR_STATUS])

    client = func_mongo.db_connect()
    cond = {mongo_const.FI_SEQ: seq}

    if status == const.STATUS_DELETE:
        func_mongo.db_delete(client, mongo_const.COLL_BOARD, cond)
    else:
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
