# 説明: 権限情報DAO

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_mongo as func_mongo
import apps.utils.mongo_constants as mongo_const

# 掲示板情報
COLL = mongo_const.COLL_AUTH


# 権限情報取得
def get_auth_info(div: str):
    client = func_mongo.db_connect()

    cond = {mongo_const.FI_DIV: div}
    auth_info = func_mongo.db_find_one(client, COLL, cond)

    func_mongo.db_close(client)
    return auth_info


# 権限情報取得
def get_auth_token(div: str, key: str = mongo_const.FI_TOKEN):
    auth_info = get_auth_info(div)
    token = auth_info[key]
    return token


# 権限情報更新
def update_auth_token(div: str, token: str):
    client = func_mongo.db_connect()

    cond = {mongo_const.FI_DIV: div}
    update_data = {
        mongo_const.FI_TOKEN: token,
        mongo_const.FI_UPDATE_DATE: func.get_now(),
    }
    func_mongo.db_update(client, COLL, cond, update_data)

    func_mongo.db_close(client)
