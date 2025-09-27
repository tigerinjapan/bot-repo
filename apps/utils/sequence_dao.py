# 説明: シーケンスDAO

import apps.utils.constants as const
import apps.utils.function_mongo as func_mongo
from apps.utils.function import get_now

# 掲示板情報
COLL = const.COLL_SEQUENCE


# シーケンス取得
def get_sequence(client, div: str) -> int:
    cond = {"sDiv": div}
    select_data = {"nSeq": 1}
    result = func_mongo.db_find_one(client, COLL, cond, select_data)
    seq = result["nSeq"]
    return seq


# シーケンス更新
def update_sequence(client, div: str, seq_val: int):
    cond = {"sDiv": div}
    update_data = {"$inc": {"nSeq": seq_val}, "$set": {"dUpdateDate": get_now()}}
    func_mongo.db_find_update(client, COLL, cond, update_data)
