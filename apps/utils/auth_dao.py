"""
権限情報DAO
"""

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_mongo as func_mongo
import apps.utils.mongo_constants as mongo_const


def get_auth_info(div: str):
    """
    権限情報取得
    """
    client = func_mongo.db_connect()

    cond = {mongo_const.FI_DIV: div}
    auth_info = func_mongo.db_find_one(client, mongo_const.COLL_AUTH, cond)

    func_mongo.db_close(client)
    return auth_info


def get_auth_token(div: str, key: str = mongo_const.FI_TOKEN):
    """
    権限情報取得 (トークン)
    """
    auth_info = get_auth_info(div)
    if key == mongo_const.FI_TOKEN:
        token = auth_info[key]
    else:
        token = const.FLG_ON if auth_info else const.FLG_OFF
    return token


def update_auth_token(div: str, token: str):
    """
    権限情報更新
    """
    client = func_mongo.db_connect()

    cond = {mongo_const.FI_DIV: div}
    update_data = {
        mongo_const.FI_TOKEN: token,
        mongo_const.FI_UPDATE_DATE: func.get_now(),
    }
    func_mongo.db_update(client, mongo_const.COLL_AUTH, cond, update_data)

    func_mongo.db_close(client)
