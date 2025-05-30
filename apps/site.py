# 説明: メニュー

import pandas as pd

import apps.utils.constants as const
import apps.utils.function as func

# アプリケーション名
app_name = func.get_app_name(__file__)

# タイトル
app_title = "お気に入りサイト"
app_title_cafe = "おしゃれカフェ"
app_title_trip = "旅行"

# カラムリスト
col_list = [
    const.STR_DIV_JA,
    const.STR_TITLE_JA,
    const.STR_CONTENTS_JA,
]

# col_list_cafe = ["店名", "特徴", "住所", "営業時間", "モーニング", "メニュー", "内観"]
col_list_cafe = ["店名", "住所", "メニュー", "内観"]
col_list_trip = ["区分", "内容", "アクセス", "画像"]

menu_trip_div = ["両替所", "観光地", "レストラン", "その他"]

# URL
URL_KOYEB_APP = "https://" + func.get_env_val("URL_KOYEB")


# データリスト取得
def get_df_data(user_div: str, app_div: str):
    # JSONデータ取得
    json_data = func.get_input_data(app_div)

    # DataFrame変換
    df_all = pd.DataFrame(json_data)
    if app_div == const.APP_SITE:
        user_auth = get_user_auth_num(user_div)
        search_query = f'auth <= "{user_auth}"'
        df_query = df_all.query(search_query)

        df_info = df_query
        df_info[const.STR_TITLE] = func.get_a_tag(
            df_info[const.STR_URL], df_info[const.STR_TITLE]
        )
        column_list = df_info.columns[1:4]
        df = df_info[column_list]
        df.columns = col_list

    else:
        df_info = df_all
        df_info[const.STR_NAME] = func.get_a_tag(
            df_info[const.STR_URL], df_info[const.STR_NAME]
        )
        img_path = f"{URL_KOYEB_APP}/{const.STR_IMG}/"
        file_name = df_info[const.STR_IMG]

        if app_div == const.APP_CAFE:
            df_info[const.STR_IMG] = func.get_img_tag(img_path, file_name, "_menu")
            df_info[const.STR_URL] = func.get_img_tag(img_path, file_name, "_in")
            df = df_info[[const.STR_NAME, const.STR_ADDR, const.STR_IMG, const.STR_URL]]
            df.columns = col_list_cafe

        elif app_div == const.APP_TRIP:
            df_info[const.STR_IMG] = func.get_img_tag(img_path, file_name)
            df = df_info[
                [const.STR_NAME, const.STR_DESCRIPTION, const.STR_ACCESS, const.STR_IMG]
            ]
            df.columns = col_list_trip

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
