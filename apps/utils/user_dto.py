"""
ログインチェユーザー情報DTOック
"""

from dataclasses import asdict, dataclass
from datetime import datetime

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.mongo_constants as mongo_const


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
    dModifiedDate: datetime
    dLastLoginDate: datetime

    def get_data(self):
        return asdict(self)


def get_json_data_for_user_info(form_data):
    """
    JSONデータ取得 (ユーザー情報の登録・更新)
    """
    user_id = form_data[mongo_const.ITEM_USER_ID]
    user_name = form_data[mongo_const.ITEM_USER_NAME]
    user_div = form_data[mongo_const.ITEM_USER_DIV]
    user_pw = form_data[mongo_const.ITEM_USER_PW]
    year = form_data[mongo_const.ITEM_YEAR]
    sex = form_data[mongo_const.ITEM_SEX]
    zip_cd = form_data[mongo_const.ITEM_ZIP_CD]
    pref = form_data[mongo_const.ITEM_PREF]
    town = form_data[mongo_const.ITEM_TOWN]
    line = form_data[mongo_const.ITEM_LINE]
    station = form_data[mongo_const.ITEM_STATION]
    tel = form_data[mongo_const.ITEM_TEL]
    seq = form_data[mongo_const.ITEM_SEQ]
    updateDate = func.get_now()

    menu_val_list = []
    for idx in range(const.MAX_USER_MENU):
        try:
            menu_val = form_data[f"{mongo_const.ITEM_MENU}{idx}"]
            menu_val_list.append(menu_val)
        except:
            continue

    json_data = userInfo(
        func.get_masking_data(user_id),
        user_name,
        user_div,
        func.get_masking_data(user_pw),
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
        updateDate,
        updateDate,
    ).get_data()
    return json_data
