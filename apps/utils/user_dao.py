from pymongo import DESCENDING

import apps.utils.constants as const
import apps.utils.function_mongo as func_mongo
import apps.utils.user_dto as dto
from apps.utils.function import get_masking_data

# コレクション: ユーザー情報
COLL = const.COLL_USER_INFO


# ユーザー情報取得
def get_user_info(userId: str):
    client = func_mongo.db_connect()
    user_id = get_masking_data(userId)
    user_info = find_user_info(client, user_id)
    if not user_info:
        return const.NONE_CONSTANT
    func_mongo.db_close(client)
    return user_info


# ユーザー情報検索
def find_user_info(client, user_id: str):
    cond = {dto.FI_USER_ID: user_id}
    count = func_mongo.db_count(client, COLL, cond)

    select_data = {"_id": 0, dto.FI_MODIFIED_DATE: 0, dto.FI_LAST_LOGIN_DATE: 0}
    result = (
        const.NONE_CONSTANT
        if count == 0
        else func_mongo.db_find_one(client, COLL, cond, select_data)
    )
    return result


# 連番取得
def get_user_seq():
    client = func_mongo.db_connect()
    cond = {dto.FI_USER_DIV: {"$eq": const.AUTH_GUEST}}
    select_data = {dto.FI_SEQ: 1}
    sort = [(dto.FI_SEQ, DESCENDING)]
    result = func_mongo.db_find(client, COLL, cond, select_data, sort)
    seq = result[0].get(dto.FI_SEQ) + 1
    func_mongo.db_close(client)
    return seq


# ユーザー情報登録
def insert_user_info(client, insert_data):
    func_mongo.db_insert(client, COLL, insert_data)


# ユーザー情報更新
def update_user_info(client, update_data):
    user_id = update_data[dto.FI_USER_ID]
    cond = {dto.FI_USER_ID: user_id}
    update_data = {"$set": update_data}
    func_mongo.db_update(client, COLL, cond, update_data)


# ユーザー情報登録（フォーム）
def insert_user_info_on_form(form_data):
    client = func_mongo.db_connect()
    insert_data = dto.get_json_data_for_user_info(form_data)
    insert_user_info(client, insert_data)
    func_mongo.db_close(client)


# ユーザー情報更新（フォーム）
def update_user_info_on_form(form_data, form_flg: bool = const.FLG_ON):
    client = func_mongo.db_connect()
    update_data = form_data
    if form_flg:
        update_data = dto.get_json_data_for_user_info(form_data)
    update_user_info(client, update_data)
    func_mongo.db_close(client)


if __name__ == const.MAIN_FUNCTION:
    user_id = "dev@jh.com"
    user_info = get_user_info(user_id)
    print(user_info)
