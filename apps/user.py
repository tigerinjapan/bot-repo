# 説明：ユーザー設定

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.user_dao as dao
import apps.utils.constants as const
from apps.utils.function_mongo import db_close, db_connect


# ユーザー情報更新
def user_info_update(form_data):
    client = db_connect()
    dao.update_user_info_on_form(client, form_data)
    db_close(client)


def user_test():
    client = db_connect()
    user_id = "dev@jh.com"
    user_info = dao.find_user_info(client, user_id)
    func.print_info_msg(const.STR_USER, user_info)

    user_seq = dao.get_user_seq(client)
    func.print_info_msg(const.ITEM_SEQ, user_seq)

    db_close(client)


if __name__ == const.MAIN_FUNCTION:
    user_test()
