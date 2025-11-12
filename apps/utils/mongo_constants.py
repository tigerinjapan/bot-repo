"""
mongoDB定数一覧
"""

from pymongo import ASCENDING, DESCENDING

import apps.utils.constants as const

# ソート
SORT_ASCENDING = ASCENDING
SORT_DESCENDING = DESCENDING

# コレクション名
COLL_USER_INFO = "userInfo"
COLL_AUTH = "auth"
COLL_RANK_INFO = "rankInfo"
COLL_RANKING = "ranking"
COLL_BOARD = "board"
COLL_LOG = "log"
COLL_SEQUENCE = "sequence"

# 項目ID: 共通
ITEM_USER_ID = "userId"
ITEM_USER_NAME = "userName"
ITEM_USER_PW = "userPw"

ITEM_SEQ = "seq"
ITEM_UPDATE_DATE = "updateDate"

# 項目ID: user info
ITEM_USER_DIV = "userDiv"
ITEM_YEAR = "year"
ITEM_SEX = "sex"
ITEM_ZIP_CD = "zipCd"
ITEM_PREF = "pref"
ITEM_TOWN = "town"
ITEM_LINE = "line"
ITEM_STATION = "station"
ITEM_TEL = "tel"
ITEM_MENU = "menu"
ITEM_MODIFIED_DATE = "modifiedDate"
ITEM_LAST_LOGIN_DATE = "lastLoginDate"

# 項目ID: rank info
ITEM_NUMBER = "number"
ITEM_RANK_TIME = "rankTime"

# 項目ID: ranking
ITEM_RANK = "rank"
ITEM_SCORE = "score"

# 項目ID: board
ITEM_APP = "app"
ITEM_CATEGORY = "category"
ITEM_TYPE = "type"
ITEM_CONTENTS = "contents"
ITEM_REMARK = "remark"
ITEM_STATUS = "status"

# 項目ID: log
ITEM_MESSAGE = "message"
ITEM_TARGET_DATE = "targetDate"

# 演算子
OPERATOR_EQUAL = "$eq"
OPERATOR_NOT_EQUAL = "$ne"
OPERATOR_GREATER_THAN = "$gt"
OPERATOR_GREATER_THAN_OR_EQUAL = "$gte"
OPERATOR_LESS_THAN = "$lt"
OPERATOR_LESS_THAN_OR_EQUAL = "$lte"
OPERATOR_IN = "$in"
OPERATOR_NOT_IN = "$nin"
OPERATOR_AND = "$and"
OPERATOR_OR = "$or"
OPERATOR_NOT = "$not"
OPERATOR_EXISTS = "$exists"
OPERATOR_REGEX = "$regex"
OPERATOR_SWITCH = "$switch"
OPERATOR_MAP = "$map"

OPERATOR_SET = "$set"
OPERATOR_INCREMENT = "$inc"
OPERATOR_ADD = "$add"


def convert_field(id: str, type_div: str = const.TYPE_STR):
    """
    フィールド変換
    """
    div = "ao" if type_div == const.TYPE_LIST else type_div[0]
    # func[capitalize]:Converts the first character of a string to an uppercase letter
    id_new = id.capitalize()[0] + id[1:]
    field = f"{div}{id_new}"
    return field


# フィールド: 共通
FI_ID = "_id"
FI_USER_ID = convert_field(ITEM_USER_ID)
FI_USER_NAME = convert_field(ITEM_USER_NAME)
FI_USER_PW = convert_field(ITEM_USER_PW)

FI_DIV = convert_field(const.STR_DIV)
FI_SEQ = convert_field(ITEM_SEQ, const.TYPE_NUM)
FI_UPDATE_DATE = convert_field(ITEM_UPDATE_DATE, const.TYPE_DATE)

# フィールド: user info
FI_USER_DIV = convert_field(ITEM_USER_DIV)
FI_YEAR = convert_field(ITEM_YEAR, const.TYPE_NUM)
FI_SEX = convert_field(ITEM_SEX, const.TYPE_NUM)
FI_ZIP_CD = convert_field(ITEM_ZIP_CD)
FI_PREF = convert_field(ITEM_PREF)
FI_TOWN = convert_field(ITEM_TOWN)
FI_LINE = convert_field(ITEM_LINE)
FI_STATION = convert_field(ITEM_STATION)
FI_TEL = convert_field(ITEM_TEL)
FI_MENU = convert_field(ITEM_MENU)
FI_MODIFIED_DATE = convert_field(ITEM_MODIFIED_DATE, const.TYPE_DATE)
FI_LAST_LOGIN_DATE = convert_field(ITEM_LAST_LOGIN_DATE, const.TYPE_DATE)

# フィールド: auth
FI_TOKEN = convert_field(const.STR_TOKEN)

# フィールド: rank info
FI_NUMBER = convert_field(ITEM_NUMBER, const.TYPE_NUM)
FI_RANK_TIME = convert_field(ITEM_RANK_TIME)

# フィールド: ranking
FI_RANK = convert_field(ITEM_RANK, const.TYPE_NUM)
FI_SCORE = convert_field(ITEM_SCORE, const.TYPE_NUM)

# フィールド: board
FI_APP = convert_field(ITEM_APP, const.TYPE_NUM)
FI_CATEGORY = convert_field(ITEM_CATEGORY, const.TYPE_NUM)
FI_TYPE = convert_field(ITEM_TYPE, const.TYPE_NUM)
FI_CONTENTS = convert_field(ITEM_CONTENTS)
FI_REMARK = convert_field(ITEM_REMARK)
FI_STATUS = convert_field(ITEM_STATUS, const.TYPE_NUM)

# フィールド: log
FI_TARGET_DATE = convert_field(ITEM_TARGET_DATE, const.TYPE_DATE)
FI_MESSAGE = convert_field(ITEM_MESSAGE)
