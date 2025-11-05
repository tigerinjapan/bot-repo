"""
掲示板情報DTO
"""

from dataclasses import asdict, dataclass
from datetime import datetime

import apps.utils.constants as const
import apps.utils.mongo_constants as mongo_const
from apps.utils.function import convert_date_to_str, get_now


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


def get_update_data_for_board_info(data, seq: int):
    """
    JSONデータ取得（掲示板情報の登録用）
    """
    app = int(data[0])
    category = int(data[1])
    type = int(data[2])
    contents = data[3]
    remark = const.SYM_DASH
    status = const.STATUS_NEW
    userName = data[4]

    json_data = asdict(
        board(seq, app, category, type, contents, remark, status, userName)
    )
    return json_data


def get_board_data(data):
    """
    掲示板データ取得
    """
    seq = data[mongo_const.FI_SEQ]
    app = const.LIST_BOARD_APP[data[mongo_const.FI_APP]]
    category = const.LIST_BOARD_CATEGORY[data[mongo_const.FI_CATEGORY]]
    type = const.LIST_BOARD_TYPE[data[mongo_const.FI_TYPE]]
    contents = data[mongo_const.FI_CONTENTS]
    remark = data[mongo_const.FI_REMARK]
    status = const.LIST_BOARD_STATUS[data[mongo_const.FI_STATUS]]
    userName = data[mongo_const.FI_USER_NAME]
    updateDate = convert_date_to_str(
        data[mongo_const.FI_UPDATE_DATE], const.DATE_FORMAT_YYYYMMDD_SLASH
    )

    json_data = asdict(
        board(seq, app, category, type, contents, remark, status, userName, updateDate)
    )
    return json_data
