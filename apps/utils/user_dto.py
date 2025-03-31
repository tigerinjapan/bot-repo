from dataclasses import asdict, dataclass
from datetime import datetime

import apps.utils.constants as const
from apps.utils.function import get_masking_data


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
    nSeq: int
    dModifiedDate: datetime = const.DATETIME_NOW
    dLastLoginDate: datetime = const.DATETIME_NOW

    def get_data(self):
        return asdict(self)


# JSONデータ取得（ユーザー情報の登録・更新）
def get_json_data_for_user_info(form_data):
    user_id = form_data[const.ITEM_USER_ID]
    user_name = form_data[const.ITEM_USER_NAME]
    user_div = form_data[const.ITEM_USER_DIV]
    user_pw = form_data[const.ITEM_USER_PW]
    year = form_data[const.ITEM_YEAR]
    sex = form_data[const.ITEM_SEX]
    zip_cd = form_data[const.ITEM_ZIP_CD]
    pref = form_data[const.ITEM_PREF]
    town = form_data[const.ITEM_TOWN]
    line = form_data[const.ITEM_LINE]
    station = form_data[const.ITEM_STATION]
    tel = form_data[const.ITEM_TEL]
    seq = form_data[const.ITEM_SEQ]

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
            int(seq),
        )
    )
    return json_data
