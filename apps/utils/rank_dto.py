from dataclasses import asdict, dataclass
from datetime import datetime

from apps.utils.user_dto import convert_field
import apps.utils.constants as const

# 項目ID:rank info
ITEM_NUMBER = "number"
ITEM_RANK_TIME = "rankTime"
ITEM_USER_NAME = "userName"
ITEM_UPDATE_DATE = "updateDate"

# フィールド:rank info
FI_NUMBER = convert_field(const.TYPE_NUM, ITEM_NUMBER)
FI_RANK_TIME = convert_field(const.TYPE_STR, ITEM_RANK_TIME)
FI_USER_NAME = convert_field(const.TYPE_STR, ITEM_USER_NAME)
FI_UPDATE_DATE = convert_field(const.TYPE_DATE, ITEM_UPDATE_DATE)


@dataclass
class rankInfo:
    """
    ランク情報のデータクラス
    """

    nNumber: int
    sRankTime: str
    sUserName: str
    dUpdateDate: datetime = datetime.now()

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
