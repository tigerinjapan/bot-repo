"""
ユーザー情報DAO
"""

from pymongo import DESCENDING

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_mongo as func_mongo
import apps.utils.message_constants as msg_const
import apps.utils.mongo_constants as mongo_const
import apps.utils.user_dto as user_dto


def get_user_info(userId: str):
    """
    ユーザー情報取得
    """
    client = func_mongo.db_connect()
    user_id = func.get_masking_data(userId)
    user_info = find_user_info(client, user_id)
    if not user_info:
        return const.NONE_CONSTANT
    func_mongo.db_close(client)
    return user_info


def find_user_info(client, user_id: str):
    """
    ユーザー情報検索
    """
    cond = {mongo_const.FI_USER_ID: user_id}
    count = func_mongo.db_count(client, mongo_const.COLL_USER_INFO, cond)

    select_data = {
        mongo_const.FI_ID: 0,
        mongo_const.FI_MODIFIED_DATE: 0,
        mongo_const.FI_LAST_LOGIN_DATE: 0,
    }
    result = (
        const.NONE_CONSTANT
        if count == 0
        else func_mongo.db_find_one(
            client, mongo_const.COLL_USER_INFO, cond, select_data
        )
    )
    return result


def get_user_seq():
    """
    連番取得
    """
    client = func_mongo.db_connect()
    cond = {mongo_const.FI_USER_DIV: {mongo_const.OPERATOR_EQUAL: const.AUTH_GUEST}}
    select_data = {mongo_const.FI_SEQ: 1}
    sort = [(mongo_const.FI_SEQ, DESCENDING)]
    result = func_mongo.db_find(
        client, mongo_const.COLL_USER_INFO, cond, select_data, sort
    )
    seq = result[0].get(mongo_const.FI_SEQ) + 1
    func_mongo.db_close(client)
    return seq


def insert_user_info(client, insert_data):
    """
    ユーザー情報登録
    """
    func_mongo.db_insert(client, mongo_const.COLL_USER_INFO, insert_data)


def update_user_info(client, update_data):
    """
    ユーザー情報更新
    """
    user_id = update_data[mongo_const.FI_USER_ID]
    cond = {mongo_const.FI_USER_ID: user_id}
    func_mongo.db_update(client, mongo_const.COLL_USER_INFO, cond, update_data)


def insert_user_info_on_form(form_data):
    """
    ユーザー情報登録（フォーム）
    """
    client = func_mongo.db_connect()
    insert_data = user_dto.get_json_data_for_user_info(form_data)
    insert_user_info(client, insert_data)
    func_mongo.db_close(client)


def update_user_info_on_form(form_data, form_flg: bool = const.FLG_ON):
    """
    ユーザー情報更新（フォーム）
    """
    client = func_mongo.db_connect()
    update_data = form_data
    if form_flg:
        update_data = user_dto.get_json_data_for_user_info(form_data)
    update_user_info(client, update_data)
    func_mongo.db_close(client)


def check_login(input_id: str, input_pw: str, user_info) -> str:
    """
    ログインチェック
    """
    chk_msg = const.SYM_BLANK

    network_flg = func.is_network()
    if network_flg:
        if input_id and input_pw and user_info:
            user_id = user_info[mongo_const.FI_USER_ID]
            user_id = func.get_decoding_masking_data(user_id)
            user_pw = user_info[mongo_const.FI_USER_PW]
            user_pw = func.get_decoding_masking_data(user_pw)

            if input_id != user_id:
                chk_msg = msg_const.MSG_ERR_USER_NOT_EXIST
            elif input_pw != user_pw:
                chk_msg = msg_const.MSG_ERR_PASSWORD_INCORRECT
        else:
            chk_msg = msg_const.MSG_ERR_USER_NOT_EXIST
    else:
        chk_msg = msg_const.MSG_ERR_CONNECTION_FAILED

    if chk_msg:
        func.print_info_msg(const.STR_LOGIN, chk_msg)

    return chk_msg


if __name__ == const.MAIN_FUNCTION:
    user_id = "dev@jh.com"
    user_info = get_user_info(user_id)
    print(user_info)
