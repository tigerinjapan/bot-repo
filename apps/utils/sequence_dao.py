"""
シーケンスDAO
"""

import apps.utils.function_mongo as func_mongo
import apps.utils.mongo_constants as mongo_const
from apps.utils.function import get_now


def get_sequence(client, div: str) -> int:
    """
    シーケンス取得
    """
    cond = {mongo_const.FI_DIV: div}
    select_data = {mongo_const.FI_SEQ: 1}
    result = func_mongo.db_find_one(
        client, mongo_const.COLL_SEQUENCE, cond, select_data
    )
    seq = result[mongo_const.FI_SEQ]
    return seq


def update_sequence(client, div: str, seq_val: int):
    """
    シーケンス更新
    """
    cond = {mongo_const.FI_DIV: div}
    update_data = {
        mongo_const.OPERATOR_INCREMENT: {mongo_const.FI_SEQ: seq_val},
        mongo_const.OPERATOR_SET: {mongo_const.FI_UPDATE_DATE: get_now()},
    }
    func_mongo.db_find_update(client, mongo_const.COLL_SEQUENCE, cond, update_data)
