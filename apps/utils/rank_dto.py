"""
ランク情報DTO
"""

from dataclasses import asdict, dataclass
from datetime import datetime

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.mongo_constants as mongo_const


@dataclass
class rankInfo:
    """
    ランク情報のデータクラス: number
    """

    nNumber: int
    sRankTime: str
    sUserName: str
    dUpdateDate: datetime = func.get_now()

    def get_data(self):
        return asdict(self)


@dataclass
class rankingInfo:
    """
    ランキング情報のデータクラス: sudoku, itQuiz
    """

    rank: int
    score: int
    userName: str
    updateDate: str

    def get_data(self):
        return asdict(self)


@dataclass
class ranking:
    """
    ランキング情報のデータクラス
    """

    sDiv: str
    nRank: int
    nScore: int
    sUserName: str
    dUpdateDate: datetime = func.get_now()

    def get_data(self):
        return asdict(self)


def get_rank_info_data(json_data, update_flg: bool = const.FLG_OFF):
    """
    JSONデータ取得（ランク情報の登録・更新）: number
    """
    if update_flg:
        number = json_data[const.STR_NUMBER]
        rank_time = json_data[const.STR_TIME].zfill(5)
        user_name = json_data[const.STR_USER]
    else:
        number = json_data[mongo_const.FI_NUMBER]
        rank_time = json_data[mongo_const.FI_RANK_TIME]
        user_name = json_data[mongo_const.FI_USER_NAME]

    json_data = rankInfo(number, rank_time, user_name).get_data()
    return json_data


def get_ranking_data(json_data):
    """
    JSONデータ取得（ランキング情報の取得）: itQuiz
    """
    rank = json_data[mongo_const.FI_RANK]
    score = json_data[mongo_const.FI_SCORE]
    userName = json_data[mongo_const.FI_USER_NAME]
    updateDate = json_data[mongo_const.FI_UPDATE_DATE]

    json_data = rankingInfo(rank, userName, score, updateDate).get_data()
    return json_data


def get_update_data_for_ranking(div, json_data):
    """
    JSONデータ取得（ランキング情報の登録・更新）
    """
    rank = json_data[mongo_const.ITEM_RANK]
    score = json_data[mongo_const.ITEM_SCORE]
    userName = json_data[mongo_const.ITEM_USER_ID]

    json_data = ranking(div, rank, score, userName).get_data()
    return json_data, rank, score
