"""
mongoDB操作
"""

import sys

from pymongo import MongoClient, UpdateOne

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


def db_connect():
    """
    DB接続
    """
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


def get_connect_info(db_div: str = const.STR_MONGO) -> str:
    """
    接続情報取得
    """
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


def db_close(client):
    """
    DB終了
    """
    client.close()
    func.print_end(app_name)


def get_collection(client, collection_name: str):
    """
    コレクション取得
    """
    # データベース指定
    db = client[DB_NAME]

    # コレクション取得
    collection = db[collection_name]
    return collection


def db_count(client, coll_nm: str, cond):
    """
    件数取得
    """
    curr_func_nm = sys._getframe().f_code.co_name
    coll = get_collection(client, coll_nm)

    try:
        result = coll.count_documents(cond)
        func.print_info_msg(curr_func_nm, coll_nm)

    except Exception as e:
        except_db(coll_nm, curr_func_nm, str(e))

    return result


def db_find(
    client,
    coll_nm: str,
    cond=const.NONE_CONSTANT,
    select_data=const.NONE_CONSTANT,
    sort=const.NONE_CONSTANT,
    one_flg=const.FLG_OFF,
):
    """
    データ検索
    """
    curr_func_nm = sys._getframe().f_code.co_name
    coll = get_collection(client, coll_nm)
    coll_find = coll.find
    if one_flg:
        coll_find = coll.find_one

    try:
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

    except Exception as e:
        except_db(coll_nm, curr_func_nm, str(e))

    return result


def except_db(coll_nm: str, curr_func_nm: str, except_str: str):
    """
    [例外] データエラー
    """
    div = f"{coll_nm} {msg_const.MSG_ERR_DB_PROC_FAILED}"
    func.print_error_msg(SCRIPT_NAME, curr_func_nm, div, except_str)


def db_find_one(
    client,
    coll_nm: str,
    cond=const.NONE_CONSTANT,
    select_data=const.NONE_CONSTANT,
    sort=const.NONE_CONSTANT,
):
    """
    データ検索（1件）
    """
    result = db_find(client, coll_nm, cond, select_data, sort, one_flg=const.FLG_ON)
    return result


def db_insert(client, coll_nm: str, insert_data, many_flg: bool = const.FLG_OFF):
    """
    データ登録
    """
    curr_func_nm = sys._getframe().f_code.co_name
    coll = get_collection(client, coll_nm)

    try:
        if many_flg:
            coll.insert_many(documents=insert_data)
        else:
            coll.insert_one(document=insert_data)

    except Exception as e:
        except_db(coll_nm, curr_func_nm, str(e))


def db_insert_many(client, coll_nm: str, insert_data):
    """
    データ登録（複数件）
    """
    db_insert(client, coll_nm, insert_data, many_flg=const.FLG_ON)


def db_update(client, coll_nm: str, cond, update_data, many_flg: bool = const.FLG_OFF):
    """
    データ更新
    """
    curr_func_nm = sys._getframe().f_code.co_name
    coll = get_collection(client, coll_nm)

    coll_update = coll.update_many
    if not many_flg:
        coll_update = coll.update_one
        update_data = {mongo_const.OPERATOR_SET: update_data}

    try:
        coll_update(filter=cond, update=update_data)
    except Exception as e:
        except_db(coll_nm, curr_func_nm, str(e))


def db_update_many(client, coll_nm: str, cond, update_data):
    """
    データ更新（複数件）
    """
    db_update(client, coll_nm, cond, update_data, many_flg=const.FLG_ON)


def get_update_one(cond, update_data):
    """
    データ更新条件取得
    """
    update_data = {mongo_const.OPERATOR_SET: update_data}
    operation = UpdateOne(filter=cond, update=update_data)
    return operation


def db_delete(client, coll_nm: str, cond, many_flg: bool = const.FLG_OFF):
    """
    データ削除
    """
    curr_func_nm = sys._getframe().f_code.co_name
    coll = get_collection(client, coll_nm)

    coll_delete = coll.delete_many
    if not many_flg:
        coll_delete = coll.delete_one

    try:
        coll_delete(filter=cond)
    except Exception as e:
        except_db(coll_nm, curr_func_nm, str(e))


def db_find_update(client, coll_nm: str, cond, update_data):
    """
    データ検索＆更新
    """
    curr_func_nm = sys._getframe().f_code.co_name
    coll = get_collection(client, coll_nm)

    try:
        result = coll.find_one(filter=cond)
        coll.update_one(filter=cond, update=update_data)

    except Exception as e:
        except_db(coll_nm, curr_func_nm, str(e))

    return result


def bulk_write(client, coll_nm: str, bulk_operations: list):
    """
    複数の書き込み操作（挿入、更新、削除など）
    """
    curr_func_nm = sys._getframe().f_code.co_name
    coll = get_collection(client, coll_nm)

    try:
        result = coll.bulk_write(bulk_operations)
        func.print_debug_msg(
            coll_nm, f"{result.modified_count} 件のドキュメントを更新しました。"
        )
    except Exception as e:
        except_db(coll_nm, curr_func_nm, str(e))


if __name__ == const.MAIN_FUNCTION:
    client = db_connect()
    user_info = get_collection(client, mongo_const.COLL_USER_INFO)
    db_close(client)
    func.print_test_data(user_info)
