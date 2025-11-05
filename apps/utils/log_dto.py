"""
ログDTO
"""

from dataclasses import asdict, dataclass
from datetime import datetime

import apps.utils.constants as const
import apps.utils.mongo_constants as mongo_const
from apps.utils.function import convert_date_to_str, get_now


@dataclass
class log:
    """
    ログのデータクラス
    """

    sDiv: str
    sMessage: str
    dTargetDate: str
    dUpdateDate: datetime = get_now()

    def get_data(self):
        return asdict(self)


def get_json_data_for_log(data):
    """
    ログデータ取得
    """
    div = data[mongo_const.FI_DIV]
    message = data[mongo_const.FI_MESSAGE]
    target_date = data[mongo_const.FI_TARGET_DATE]
    updateDate = convert_date_to_str(
        data[mongo_const.FI_UPDATE_DATE], const.DATE_FORMAT_YYYYMMDD_SLASH
    )

    json_data = asdict(
        log(
            div,
            message,
            target_date,
            updateDate,
        )
    )
    return json_data


def get_insert_data_for_log(data: list[str]):
    """
    登録データ取得
    """
    div = data[0]
    message = data[1]
    target_date = data[2]

    json_data = asdict(log(div, message, target_date))
    return json_data
