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
):
    coll = get_collection(client, coll_nm)
    if cond:
        if select_data and sort:
            result = coll.find(filter=cond, projection=select_data, sort=sort)
        elif select_data:
            result = coll.find(filter=cond, projection=select_data)
        elif sort:
            result = coll.find(filter=cond, sort=sort)
        else:
            result = coll.find(filter=cond)
    elif select_data:
        if sort:
            result = coll.find(projection=select_data, sort=sort)
        else:
            result = coll.find(projection=select_data)
    elif sort:
        result = coll.find(sort=sort)
    else:
        result = coll.find()
    return result


# データ検索（1件）
def db_find_one(client, coll_nm: str, cond=const.NONE_CONSTANT):
    coll = get_collection(client, coll_nm)
    if cond:
        result = coll.find_one(filter=cond)
    else:
        result = coll.find_one()
    return result


# データ登録
def db_insert(client, coll_nm: str, insert_data):
    coll = get_collection(client, coll_nm)
    coll.insert_one(document=insert_data)


# データ更新
def db_update(client, coll_nm: str, cond, update_data):
    coll = get_collection(client, coll_nm)
    coll.update_one(filter=cond, update=update_data)


# ユーザー情報検索
def find_user_info(client, user_id: str):
    coll = const.COLL_USER_INFO
    cond = {const.FI_USER_ID: user_id}
    count = db_count(client, coll, cond)
    result = const.NONE_CONSTANT if count == 0 else db_find_one(client, coll, cond)
    return result


# ユーザー情報取得
def get_user_info(user_id: str):
    client = db_connect()
    user_info = set_user_info(client, user_id)
    db_close(client)

    return user_info


# ユーザー情報設定
def set_user_info(client, user_id: str):
    user_info = find_user_info(client, user_id)
    if not user_info:
        return

    user_name = user_info.get(const.FI_USER_NAME)
    user_div = user_info.get(const.FI_USER_DIV)
    user_pw = user_info.get(const.FI_USER_PW)

    auth_form = {
        const.ITEM_USER_ID: user_id,
        const.ITEM_USER_NAME: user_name,
        const.ITEM_USER_DIV: user_div,
        const.ITEM_USER_PW: user_pw,
    }
    return auth_form


# ログインチェック
def check_login(input_id: str, input_pw: str, user_info) -> str:
    chk_msg = const.SYM_BLANK

    network_flg = func.is_network()
    if network_flg:
        if input_id and input_pw and user_info:
            user_id = user_info[const.ITEM_USER_ID]
            user_pw = user_info[const.ITEM_USER_PW]

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
    func.print_test_data(user_info)
