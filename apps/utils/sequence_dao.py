import apps.utils.constants as const
import apps.utils.function_mongo as func_mongo

# 掲示板情報
COLL = const.COLL_SEQUENCE


# シーケンス取得し、インクリメント
def get_sequence_and_update(client, div: str, seq_val: int) -> int:
    cond = {"sDiv": div}
    update_data = {"$inc": {"nSeq": seq_val}}
    result = func_mongo.db_find_update(client, COLL, cond, update_data)
    seq = result["nSeq"]
    return seq
