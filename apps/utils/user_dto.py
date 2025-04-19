from dataclasses import asdict, dataclass
from datetime import datetime

import apps.utils.constants as const
from apps.utils.function import get_masking_data


def convert_field(type_div, id):
    div = "ao" if type_div == const.TYPE_LIST else type_div[0]
    # func[capitalize]:Converts the first character of a string to an uppercase letter
    id_new = id.capitalize()[0] + id[1:]
    field = f"{div}{id_new}"
    return field


# 項目ID:user info
ITEM_USER_ID = "userId"
ITEM_USER_DIV = "userDiv"
ITEM_USER_NAME = "userName"
ITEM_USER_PW = "userPw"
ITEM_YEAR = "year"
ITEM_SEX = "sex"
ITEM_ZIP_CD = "zipCd"
ITEM_PREF = "pref"
ITEM_TOWN = "town"
ITEM_LINE = "line"
ITEM_STATION = "station"
ITEM_TEL = "tel"
ITEM_MENU = "menu"
ITEM_SEQ = "seq"
ITEM_MODIFIED_DATE = "modifiedDate"
ITEM_LAST_LOGIN_DATE = "lastLoginDate"

# フィールド:user info
FI_USER_ID = convert_field(const.TYPE_STR, ITEM_USER_ID)
FI_USER_DIV = convert_field(const.TYPE_STR, ITEM_USER_DIV)
FI_USER_NAME = convert_field(const.TYPE_STR, ITEM_USER_NAME)
FI_USER_PW = convert_field(const.TYPE_STR, ITEM_USER_PW)
FI_YEAR = convert_field(const.TYPE_NUM, ITEM_YEAR)
FI_SEX = convert_field(const.TYPE_NUM, ITEM_SEX)
FI_ZIP_CD = convert_field(const.TYPE_STR, ITEM_ZIP_CD)
FI_PREF = convert_field(const.TYPE_STR, ITEM_PREF)
FI_TOWN = convert_field(const.TYPE_STR, ITEM_TOWN)
FI_LINE = convert_field(const.TYPE_STR, ITEM_LINE)
FI_STATION = convert_field(const.TYPE_STR, ITEM_STATION)
FI_TEL = convert_field(const.TYPE_STR, ITEM_TEL)
FI_MENU = convert_field(const.TYPE_STR, ITEM_MENU)
FI_SEQ = convert_field(const.TYPE_NUM, ITEM_SEQ)
FI_MODIFIED_DATE = convert_field(const.TYPE_DATE, ITEM_MODIFIED_DATE)
FI_LAST_LOGIN_DATE = convert_field(const.TYPE_DATE, ITEM_LAST_LOGIN_DATE)


class Document:
    def __init__(self, **kwargs):
        """
        コンストラクタ

        引数:
            **kwargs: キーワード引数を任意の数だけ受け取る。
                      各キーが属性名、値がその属性の値として設定
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    # インスタンスの属性を辞書形式で返す
    def get_dict_data(self):
        return self.__dict__


@dataclass
class userInfo:
    """
    ユーザー情報のデータクラス
    """

    sUserId: str
    sUserName: str
    sUserDiv: str
    sUserPw: str
    nYear: int
    nSex: int
    sZipCd: str
    sPref: str
    sTown: str
    sLine: str
    sStation: str
    sTel: str
    sMenu: str
    nSeq: int
    dModifiedDate: datetime = datetime.now()
    dLastLoginDate: datetime = datetime.now()

    def get_data(self):
        return asdict(self)


# JSONデータ取得（ユーザー情報の登録・更新）
def get_json_data_for_user_info(form_data):
    user_id = form_data[ITEM_USER_ID]
    user_name = form_data[ITEM_USER_NAME]
    user_div = form_data[ITEM_USER_DIV]
    user_pw = form_data[ITEM_USER_PW]
    year = form_data[ITEM_YEAR]
    sex = form_data[ITEM_SEX]
    zip_cd = form_data[ITEM_ZIP_CD]
    pref = form_data[ITEM_PREF]
    town = form_data[ITEM_TOWN]
    line = form_data[ITEM_LINE]
    station = form_data[ITEM_STATION]
    tel = form_data[ITEM_TEL]
    seq = form_data[ITEM_SEQ]

    menu_val_list = []
    for idx in range(10):
        try:
            menu_val = form_data[f"{ITEM_MENU}{idx}"]
            menu_val_list.append(menu_val)
        except:
            continue

    json_data = asdict(
        userInfo(
            get_masking_data(user_id),
            user_name,
            user_div,
            get_masking_data(user_pw),
            int(year),
            int(sex),
            zip_cd,
            pref,
            town,
            line,
            station,
            tel,
            const.SYM_BLANK.join(menu_val_list),
            int(seq),
        )
    )
    return json_data
