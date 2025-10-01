import apps.utils.constants as const

# コレクション名 #
COLL_USER_INFO = "userInfo"
COLL_AUTH = "auth"
COLL_RANK_INFO = "rankInfo"
COLL_BOARD = "board"
COLL_SEQUENCE = "sequence"

# 項目ID: 共通
ITEM_USER_ID = "userId"
ITEM_USER_NAME = "userName"
ITEM_USER_PW = "userPw"

ITEM_SEQ = "seq"
ITEM_UPDATE_DATE = "updateDate"

# 項目ID: auth
ITEM_USER_DIV = "userDiv"
ITEM_DUE_DATE = "dueDate"

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

# 項目ID: board
ITEM_APP = "app"
ITEM_CATEGORY = "category"
ITEM_TYPE = "type"
ITEM_CONTENTS = "contents"
ITEM_REMARK = "remark"
ITEM_STATUS = "status"

# 項目ID: rank info
ITEM_NUMBER = "number"
ITEM_RANK_TIME = "rankTime"

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

OPERATOR_SET = "$set"
OPERATOR_INCREMENT = "$inc"


# フィールド変換
def convert_field(type_div, id):
    div = "ao" if type_div == const.TYPE_LIST else type_div[0]
    # func[capitalize]:Converts the first character of a string to an uppercase letter
    id_new = id.capitalize()[0] + id[1:]
    field = f"{div}{id_new}"
    return field


# フィールド: 共通
FI_ID = "_id"
FI_USER_ID = convert_field(const.TYPE_STR, ITEM_USER_ID)
FI_USER_NAME = convert_field(const.TYPE_STR, ITEM_USER_NAME)
FI_USER_PW = convert_field(const.TYPE_STR, ITEM_USER_PW)

FI_DIV = convert_field(const.TYPE_STR, const.STR_DIV)
FI_SEQ = convert_field(const.TYPE_NUM, ITEM_SEQ)
FI_UPDATE_DATE = convert_field(const.TYPE_DATE, ITEM_UPDATE_DATE)

# フィールド: user info
FI_USER_DIV = convert_field(const.TYPE_STR, ITEM_USER_DIV)
FI_YEAR = convert_field(const.TYPE_NUM, ITEM_YEAR)
FI_SEX = convert_field(const.TYPE_NUM, ITEM_SEX)
FI_ZIP_CD = convert_field(const.TYPE_STR, ITEM_ZIP_CD)
FI_PREF = convert_field(const.TYPE_STR, ITEM_PREF)
FI_TOWN = convert_field(const.TYPE_STR, ITEM_TOWN)
FI_LINE = convert_field(const.TYPE_STR, ITEM_LINE)
FI_STATION = convert_field(const.TYPE_STR, ITEM_STATION)
FI_TEL = convert_field(const.TYPE_STR, ITEM_TEL)
FI_MENU = convert_field(const.TYPE_STR, ITEM_MENU)
FI_MODIFIED_DATE = convert_field(const.TYPE_DATE, ITEM_MODIFIED_DATE)
FI_LAST_LOGIN_DATE = convert_field(const.TYPE_DATE, ITEM_LAST_LOGIN_DATE)

# フィールド: auth
FI_TOKEN = convert_field(const.TYPE_STR, const.STR_TOKEN)
FI_DUE_DATE = convert_field(const.TYPE_STR, ITEM_DUE_DATE)

# フィールド: board
FI_APP = convert_field(const.TYPE_NUM, ITEM_APP)
FI_CATEGORY = convert_field(const.TYPE_NUM, ITEM_CATEGORY)
FI_TYPE = convert_field(const.TYPE_NUM, ITEM_TYPE)
FI_CONTENTS = convert_field(const.TYPE_STR, ITEM_CONTENTS)
FI_REMARK = convert_field(const.TYPE_STR, ITEM_REMARK)
FI_STATUS = convert_field(const.TYPE_NUM, ITEM_STATUS)

# フィールド: rank info
FI_NUMBER = convert_field(const.TYPE_NUM, ITEM_NUMBER)
FI_RANK_TIME = convert_field(const.TYPE_STR, ITEM_RANK_TIME)
