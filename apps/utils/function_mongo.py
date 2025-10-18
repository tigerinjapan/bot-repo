# 説明: mongoDB操作

import sys

from pymongo import MongoClient

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.message_constants as msg_const
import apps.utils.mongo_constants as mongo_const

# スクリプト名
SCRIPT_NAME = func.get_app_name(__file__)

# アプリケーション
app_name = const.STR_MONGO

# DB名
DB_NAME = app_name + func.convert_upper_lower(const.STR_DB)


# DB接続
def db_connect():
    try:
        func.print_start(app_name)
        client_url = get_connect_info()
        client = MongoClient(client_url)
        return client
    except Exception as e:
        curr_func_nm = sys._getframe().f_code.co_name
        func.print_error_msg(
            SCRIPT_NAME,
            curr_func_nm,
            msg_const.MSG_ERR_CONNECTION_FAILED,
            str(e),
            sys_exit=const.FLG_ON,
        )


# 接続情報取得
def get_connect_info(db_div: str = const.STR_MONGO) -> str:
    client_url = const.SYM_BLANK

    auth_data = func.get_input_data(const.STR_AUTH, const.STR_MONGO)
    if auth_data:
        db_user = db_div + func.convert_upper_lower(
            const.STR_USER, const.STR_CAPITALIZE
        )
        db_pw = db_div

        host = auth_data[const.STR_HOST]
        host = func.get_decoding_masking_data(host)
        client_url = f"mongodb+srv://{db_user}:{db_pw}@{host}.mongodb.net/{DB_NAME}?retryWrites=true&w=majority"

    return client_url


# DB終了
def db_close(client):
    client.close()
    func.print_end(app_name)


# コレクション取得
def get_collection(client, collection_name: str):
    # データベース指定
    db = client[DB_NAME]

    # コレクション取得
    collection = db[collection_name]
    return collection


# 件数取得
def db_count(client, coll_nm: str, cond):
    coll = get_collection(client, coll_nm)

    try:
        result = coll.count_documents(cond)
    except Exception as e:
        curr_func_nm = sys._getframe().f_code.co_name
        func.print_error_msg(
            SCRIPT_NAME, curr_func_nm, msg_const.MSG_ERR_DB_PROC_FAILED, str(e)
        )

    func.print_info_msg("count", coll_nm)
    return result


# データ検索
def db_find(
    client,
    coll_nm: str,
    cond=const.NONE_CONSTANT,
    select_data=const.NONE_CONSTANT,
    sort=const.NONE_CONSTANT,
    one_flg=const.FLG_OFF,
):

    coll = get_collection(client, coll_nm)

    coll_find = coll.find
    if one_flg:
        coll_find = coll.find_one

    if cond:
        if select_data and sort:
            result = coll_find(filter=cond, projection=select_data, sort=sort)
        elif select_data:
            result = coll_find(filter=cond, projection=select_data)
        elif sort:
            result = coll_find(filter=cond, sort=sort)
        else:
            result = coll_find(filter=cond)
    elif select_data:
        if sort:
            result = coll_find(projection=select_data, sort=sort)
        else:
            result = coll_find(projection=select_data)
    elif sort:
        result = coll_find(sort=sort)
    else:
        result = coll_find()
    return result


# データ検索（1件）
def db_find_one(
    client,
    coll_nm: str,
    cond=const.NONE_CONSTANT,
    select_data=const.NONE_CONSTANT,
    sort=const.NONE_CONSTANT,
):

    result = db_find(client, coll_nm, cond, select_data, sort, one_flg=const.FLG_ON)
    return result


# データ登録
def db_insert(client, coll_nm: str, insert_data):
    coll = get_collection(client, coll_nm)

    try:
        coll.insert_one(document=insert_data)
    except Exception as e:
        curr_func_nm = sys._getframe().f_code.co_name
        func.print_error_msg(
            SCRIPT_NAME, curr_func_nm, msg_const.MSG_ERR_DB_PROC_FAILED, str(e)
        )


# データ更新
def db_update_one(client, coll_nm: str, cond, update_data):
    coll = get_collection(client, coll_nm)
    update_data = {mongo_const.OPERATOR_SET: update_data}

    try:
        coll.update_one(filter=cond, update=update_data)
    except Exception as e:
        curr_func_nm = sys._getframe().f_code.co_name
        func.print_error_msg(
            SCRIPT_NAME, curr_func_nm, msg_const.MSG_ERR_DB_PROC_FAILED, str(e)
        )


# データ更新
def db_update_many(client, coll_nm: str, cond, update_data):
    coll = get_collection(client, coll_nm)

    try:
        coll.update_many(filter=cond, update=update_data)
    except Exception as e:
        curr_func_nm = sys._getframe().f_code.co_name
        func.print_error_msg(
            SCRIPT_NAME, curr_func_nm, msg_const.MSG_ERR_DB_PROC_FAILED, str(e)
        )


# データ検索＆更新
def db_find_update(client, coll_nm: str, cond, update_data):
    coll = get_collection(client, coll_nm)

    result = coll.find_one(filter=cond)

    try:
        coll.update_one(filter=cond, update=update_data)
    except Exception as e:
        curr_func_nm = sys._getframe().f_code.co_name
        func.print_error_msg(
            SCRIPT_NAME, curr_func_nm, msg_const.MSG_ERR_DB_PROC_FAILED, str(e)
        )

    return result


if __name__ == const.MAIN_FUNCTION:
    client = db_connect()
    user_info = get_collection(client, mongo_const.COLL_USER_INFO)
    db_close(client)
    func.print_test_data(user_info)
