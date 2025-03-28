from pymongo import MongoClient

import apps.utils.constants as const
import apps.utils.message_constants as msg_const
import apps.utils.function as func

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
        func.print_error_msg(app_name, msg_const.MSG_ERR_CONNECTION_FAILED)
        func.print_msg_exit(app_name, str(e))


# 接続情報取得
def get_connect_info(db_div: str = const.STR_MONGO):
    client_url = const.SYM_BLANK

    auth_data = func.get_input_data(const.STR_AUTH, const.STR_MONGO)
    if auth_data:
        db_user = db_div + func.convert_upper_lower(
            const.STR_USER, div=const.STR_CAPITALIZE
        )
        db_pw = db_div

        host = auth_data[const.STR_HOST]
        client_url = f"mongodb+srv://{db_user}:{db_pw}@{host}.mongodb.net/{DB_NAME}?retryWrites=true&w=majority"

    return client_url


# DB終了
def db_close(client):
    client.close()
    func.print_end(app_name)


# コレクション取得
def get_collection(client, collection_name: str):
    if not client:
        client = db_connect()

    # データベース指定
    db = client[DB_NAME]

    # コレクション取得
    collection = db[collection_name]
    return collection


# 件数取得
def db_count(client, coll_nm: str, cond):
    coll = get_collection(client, coll_nm)
    result = coll.count_documents(cond)
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
    coll.insert_one(document=insert_data)


# データ更新
def db_update(client, coll_nm: str, cond, update_data):
    coll = get_collection(client, coll_nm)
    coll.update_one(filter=cond, update=update_data)


# ログインチェック
def check_login(input_id: str, input_pw: str, user_info) -> str:
    chk_msg = const.SYM_BLANK

    network_flg = func.is_network()
    if network_flg:
        if input_id and input_pw and user_info:
            user_id = user_info[const.FI_USER_ID]
            user_pw = user_info[const.FI_USER_PW]

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
    client = db_connect()
    user_info = get_collection(client, const.COLL_USER_INFO)
    db_close(client)
    func.print_test_data(user_info)
