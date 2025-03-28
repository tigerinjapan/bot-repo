from dataclasses import asdict, dataclass
from datetime import datetime

import apps.utils.constants as const


class Document:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_dict_data(self):
        return self.__dict__


@dataclass
class userInfo:
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
    nSeq: int
    dModifiedDate: datetime = const.DATETIME_NOW
    dLastLoginDate: datetime = const.DATETIME_NOW  # TODO ログイン時に、更新する

    def get_data(self):
        return asdict(self)


# JSONデータ取得（ユーザー情報の登録・更新）
def get_json_data_for_user_info(form_data):
    user_id = form_data[const.ITEM_USER_ID]
    user_name = form_data[const.ITEM_USER_NAME]
    user_div = form_data[const.ITEM_USER_DIV]
    user_pw = form_data[const.ITEM_USER_PW]
    year = int(form_data[const.ITEM_YEAR])
    sex = int(form_data[const.ITEM_SEX])
    zip_cd = form_data[const.ITEM_ZIP_CD]
    pref = form_data[const.ITEM_PREF]
    town = form_data[const.ITEM_TOWN]
    line = form_data[const.ITEM_LINE]
    station = form_data[const.ITEM_STATION]
    tel = form_data[const.ITEM_TEL]
    seq = int(form_data[const.ITEM_SEQ])

    json_data = asdict(
        userInfo(
            user_id,
            user_name,
            user_div,
            user_pw,
            year,
            sex,
            zip_cd,
            pref,
            town,
            line,
            station,
            tel,
            seq,
        )
    )
    return json_data
