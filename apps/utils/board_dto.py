# 説明: 掲示板情報DTO

from dataclasses import asdict, dataclass
from datetime import datetime

import apps.utils.constants as const
import apps.utils.mongo_constants as mongo_const
from apps.utils.function import convert_date_to_str, get_now

# リスト: board
LIST_APP = ["LINE", "Travel", "Kakao", "Server"]
LIST_CATEGORY = ["Review", "Memo", "Error", "Etc."]
LIST_TYPE = ["Add", "Modify", "Design", "Etc."]
LIST_STATUS = ["New", "Progress", "Pend", "Done"]

# ステータス: board
STATUS_NEW = 0
STATUS_PROGRESS = 1
STATUS_PEND = 2
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
    dUpdateDate: datetime = get_now()

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
    seq = data[mongo_const.FI_SEQ]
    app = LIST_APP[data[mongo_const.FI_APP]]
    category = LIST_CATEGORY[data[mongo_const.FI_CATEGORY]]
    type = LIST_TYPE[data[mongo_const.FI_TYPE]]
    contents = data[mongo_const.FI_CONTENTS]
    remark = data[mongo_const.FI_REMARK]
    status = LIST_STATUS[data[mongo_const.FI_STATUS]]
    userName = data[mongo_const.FI_USER_NAME]
    updateDate = convert_date_to_str(
        data[mongo_const.FI_UPDATE_DATE], const.DATE_FORMAT_YYYYMMDD_SLASH
    )

    json_data = asdict(
        board(seq, app, category, type, contents, remark, status, userName, updateDate)
    )
    return json_data
