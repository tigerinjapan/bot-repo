# 説明: ランク情報DTO

from dataclasses import asdict, dataclass
from datetime import datetime

import apps.utils.constants as const
from apps.utils.function import get_now


@dataclass
class rankInfo:
    """
    ランク情報のデータクラス
    """

    nNumber: int
    sRankTime: str
    sUserName: str
    dUpdateDate: datetime = get_now()

    def get_data(self):
        return asdict(self)


# JSONデータ取得（ランク情報の登録・更新）
def get_update_data_for_rank_info(json_data):
    number = json_data[const.STR_NUMBER]
    rank_time = json_data[const.STR_TIME].zfill(5)
    user_name = json_data[const.STR_USER]

    json_data = asdict(
        rankInfo(
            number,
            rank_time,
            user_name,
        )
    )
    return json_data
