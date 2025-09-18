# 説明: 掲示板情報DTO

from dataclasses import asdict, dataclass
from datetime import datetime

import apps.utils.constants as const
from apps.utils.function import convert_date_to_str, get_now
from apps.utils.user_dto import convert_field

# 項目ID
ITEM_SEQ = "seq"
ITEM_APP = "app"
ITEM_CATEGORY = "category"
ITEM_TYPE = "type"
ITEM_CONTENTS = "contents"
ITEM_REMARK = "remark"
ITEM_STATUS = "status"
ITEM_USER_NAME = "userName"
ITEM_UPDATE_DATE = "updateDate"

# フィールド
FI_SEQ = convert_field(const.TYPE_NUM, ITEM_SEQ)
FI_APP = convert_field(const.TYPE_NUM, ITEM_APP)
FI_CATEGORY = convert_field(const.TYPE_NUM, ITEM_CATEGORY)
FI_TYPE = convert_field(const.TYPE_NUM, ITEM_TYPE)
FI_CONTENTS = convert_field(const.TYPE_STR, ITEM_CONTENTS)
FI_REMARK = convert_field(const.TYPE_STR, ITEM_REMARK)
FI_STATUS = convert_field(const.TYPE_NUM, ITEM_STATUS)
FI_USER_NAME = convert_field(const.TYPE_STR, ITEM_USER_NAME)
FI_UPDATE_DATE = convert_field(const.TYPE_DATE, ITEM_UPDATE_DATE)

# リスト
LIST_APP = [
    "LINE Message",
    "Trip & Life",
    "Number Plate",
    "その他",
]
LIST_CATEGORY = ["レビュー", "メモ", "その他"]
LIST_TYPE = ["機能追加", "機能修正", "レイアウト", "その他"]
LIST_STATUS = ["新規", "対応中", "保留", "対応完了"]

# ステータス
STATUS_NEW = 0
STATUS_DONE = 3


@dataclass
class board:
    """
    掲示板情報のデータクラス
    """

    nSeq: int
    nApp: int
    nCategory: int
    nType: int
    sContents: str
    sRemark: str
    nStatus: int
    sUserName: str
    dUpdateDate: datetime = get_now

    def get_data(self):
        return asdict(self)


# JSONデータ取得（掲示板情報の登録用）
def get_update_data_for_board_info(data, seq: int):
    app = int(data[0])
    category = int(data[1])
    type = int(data[2])
    contents = data[3]
    remark = const.SYM_DASH
    status = STATUS_NEW
    userName = data[4]

    json_data = asdict(
        board(seq, app, category, type, contents, remark, status, userName)
    )
    return json_data


# 掲示板データ取得
def get_board_data(data):
    seq = data[FI_SEQ]
    app = LIST_APP[data[FI_APP]]
    category = LIST_CATEGORY[data[FI_CATEGORY]]
    type = LIST_TYPE[data[FI_TYPE]]
    contents = data[FI_CONTENTS]
    remark = data[FI_REMARK]
    status = LIST_STATUS[data[FI_STATUS]]
    userName = data[FI_USER_NAME]
    updateDate = convert_date_to_str(
        data[FI_UPDATE_DATE], const.DATE_FORMAT_YYYYMMDD_SLASH
    )

    json_data = asdict(
        board(seq, app, category, type, contents, remark, status, userName, updateDate)
    )
    return json_data
