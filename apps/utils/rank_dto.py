# 説明: ランク情報DTO

from dataclasses import asdict, dataclass
from datetime import datetime

import apps.utils.constants as const
import apps.utils.mongo_constants as mongo_const
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


@dataclass
class ranking:
    """
    ランキング情報のデータクラス
    """

    userId: str
    score: int
    lastLoginDate: str

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


# JSONデータ取得（ランキング情報の取得）
def get_ranking_data(json_data):
    userId = json_data[mongo_const.FI_USER_NAME]
    score = json_data[mongo_const.FI_SCORE]
    lastLoginDate = json_data[mongo_const.FI_UPDATE_DATE]

    json_data = asdict(
        ranking(
            userId,
            score,
            lastLoginDate,
        )
    )
    return json_data
