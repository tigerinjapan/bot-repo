# 説明：メニュー

import pandas as pd

import apps.utils.constants as const
import apps.utils.function as func

# アプリケーション名
app_name = func.get_app_name(__file__)

# タイトル
app_title = "お気に入りサイト"

# カラムリスト
col_list = [
    const.STR_DIV_JA,
    const.STR_TITLE_JA,
    const.STR_CONTENTS_JA,
]


# データリスト取得
def get_df_data(user_div: str):
    # JSONデータ取得
    json_data = func.get_input_data(const.APP_SITE, "item")

    # DataFrame変換
    df_all = pd.DataFrame(json_data)
    user_auth = get_user_auth_num(user_div)
    search_query = f'auth <= "{user_auth}"'
    df_query = df_all.query(search_query)

    column_list = df_query.columns[1:]
    df_info = df_query[column_list]
    df_info[const.STR_TITLE] = func.get_df_link(
        df_info[const.STR_URL], df_info[const.STR_TITLE]
    )
    df = df_info[column_list[:3]]
    df.columns = col_list
    return df


# ユーザー権限取得
def get_user_auth_num(user_div):
    user_auth_num = const.NUM_AUTH_GUEST
    if user_div == const.AUTH_ADMIN:
        user_auth_num = const.NUM_AUTH_ADMIN
    elif user_div == const.AUTH_DEV:
        user_auth_num = const.NUM_AUTH_DEV
    return user_auth_num


if __name__ == const.MAIN_FUNCTION:
    user_div = const.AUTH_DEV
    data_list = get_df_data(user_div)
    func.print_test_data(data_list)
