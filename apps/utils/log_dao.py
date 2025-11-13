"""
ログDAO
"""

import apps.utils.constants as const
import apps.utils.log_dto as log_dto
import apps.utils.function_mongo as func_mongo
import apps.utils.mongo_constants as mongo_const


def get_log_data(
    div: str, target_date: str = const.SYM_BLANK, json_flg: bool = const.FLG_OFF
):
    """
    バックアップしたログ取得
    """
    log_data_list = []

    client = func_mongo.db_connect()

    cond_and_list = [{mongo_const.FI_DIV: div}]
    if target_date:
        cond_target_date = {
            mongo_const.FI_TARGET_DATE: {
                mongo_const.OPERATOR_GREATER_THAN_OR_EQUAL: target_date
            }
        }
        cond_and_list.append(cond_target_date)

    cond = {mongo_const.OPERATOR_AND: cond_and_list}

    sort = {}
    if div != const.APP_DASHBOARD:
        sort = {
            mongo_const.FI_TARGET_DATE: mongo_const.SORT_DESCENDING,
        }

    result = func_mongo.db_find(client, mongo_const.COLL_LOG, cond, sort=sort)
    if result:
        for log_info in result:
            if json_flg:
                log_data = log_dto.get_json_data_for_log(log_info)
            else:
                log_data = log_info[mongo_const.FI_MESSAGE]
            log_data_list.append(log_data)

    func_mongo.db_close(client)
    return log_data_list


def insert_log_data(data_list):
    """
    バックアップログの登録
    """
    client = func_mongo.db_connect()
    func_mongo.db_insert_many(client, mongo_const.COLL_LOG, data_list)
    func_mongo.db_close(client)


if __name__ == const.MAIN_FUNCTION:
    log_data = get_log_data(const.STR_ERROR)
    print(log_data)
