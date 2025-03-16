# 説明：メニュー

import pandas as pd

import apps.utils.constants as const
import apps.utils.function as func

# アプリケーション名
app_name = func.get_app_name(__file__)

# タイトル
app_title = "お気に入りサイト"
app_title_cafe = "おしゃれカフェ"

# カラムリスト
col_list = [
    const.STR_DIV_JA,
    const.STR_TITLE_JA,
    const.STR_CONTENTS_JA,
]

col_list_cafe = ["店名", "特徴", "住所", "営業時間", "メニュー", "写真#1", "写真#2"]

# URL
URL_KOYEB_APP = "https://" + func.get_env_val("URL_KOYEB")


# データリスト取得
def get_df_data(user_div: str, app_div: str):
    # JSONデータ取得
    json_data = func.get_input_data(app_div, const.STR_ITEM)

    # DataFrame変換
    df_all = pd.DataFrame(json_data)
    if app_div == const.APP_SITE:
        user_auth = get_user_auth_num(user_div)
        search_query = f'auth <= "{user_auth}"'
        df_query = df_all.query(search_query)

        # column_list = df_query.columns[1:]
        # df_info = df_query[column_list]
        df_info = df_query
        df_info[const.STR_TITLE] = func.get_df_link(
            df_info[const.STR_URL], df_info[const.STR_TITLE]
        )
        column_list = df_info.columns[1:4]
        df = df_info[column_list]
    else:
        df_info = df_all
        df_info[const.STR_NAME] = func.get_df_link(
            df_info[const.STR_URL], df_info[const.STR_NAME]
        )
        img_file_div = df_info[const.STR_IMG].values[0]
        img_file_name = (
            f"{URL_KOYEB_APP}/{const.STR_IMG}/{const.STR_INPUT}/{img_file_div}"
        )
        df_info[const.STR_IMG] = img_file_name + "_in"
        df_info[const.STR_URL] = img_file_name + "_menu"
        df_info[const.STR_IMG] = f"{URL_KOYEB_APP}/{const.STR_IMG}/test"
        df = df_info

    df.columns = col_list_cafe if app_div == const.APP_CAFE else col_list
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
    app_div = const.APP_CAFE
    data_list = get_df_data(user_div, app_div)
    func.print_test_data(data_list.values.tolist())
