from dataclasses import asdict, dataclass
from datetime import datetime

from apps.utils.user_dto import convert_field
import apps.utils.constants as const

# 項目ID
ITEM_APP = "app"
ITEM_CATEGORY = "category"
ITEM_CONTENTS = "contents"
ITEM_REMARK = "remark"
ITEM_STATUS = "status"
ITEM_USER_NAME = "userName"
ITEM_UPDATE_DATE = "updateDate"

# フィールド
FI_APP = convert_field(const.TYPE_STR, ITEM_APP)
FI_CATEGORY = convert_field(const.TYPE_STR, ITEM_CATEGORY)
FI_CONTENTS = convert_field(const.TYPE_STR, ITEM_CONTENTS)
FI_REMARK = convert_field(const.TYPE_STR, ITEM_REMARK)
FI_STATUS = convert_field(const.TYPE_STR, ITEM_STATUS)
FI_USER_NAME = convert_field(const.TYPE_STR, ITEM_USER_NAME)
FI_UPDATE_DATE = convert_field(const.TYPE_DATE, ITEM_UPDATE_DATE)


@dataclass
class board:
    """
    掲示板情報のデータクラス
    """

    sApp: str
    sCategory: str
    sContents: str
    sRemark: str
    sStatus: str
    sUserName: str
    dUpdateDate: datetime = datetime.now()

    def get_data(self):
        return asdict(self)


# JSONデータ取得（掲示板情報の登録）
def get_update_data_for_board_info(data):
    app = data[0]
    category = data[1]
    contents = data[2]
    remark = "-"
    status = "new"
    userName = data[4]

    json_data = asdict(board(app, category, contents, remark, status, userName))
    return json_data
