# 説明: メニュー

import numpy as np
import pandas as pd

import apps.utils.board_dao as board_dao
import apps.utils.constants as const
import apps.utils.function as func

# タイトル
app_title = "お気に入りサイト"
app_title_cafe = "おしゃれカフェ"
app_title_travel = "旅行"
app_title_board = "掲示板"

# カラムリスト
col_list = [
    const.STR_DIV_JA,
    const.STR_TITLE_JA,
    const.STR_CONTENTS_JA,
]

col_list_cafe = ["店名", "住所", "メニュー", "内観"]
col_list_travel = ["区分", "内容", "アクセス", "画像"]
col_list_board = [
    "番号",
    "アプリ",
    "カテゴリー",
    "区分",
    "内容",
    "備考",
    "状態",
    "作成者",
    "作成日",
    "完了",
]

menu_travel_div = ["両替所", "観光地", "レストラン", "その他"]

# URL
URL_SERVER = func.get_server_url()


# データリスト取得
def get_df_data(app_div: str, user_div: str = const.AUTH_DEV):
    # JSONデータ取得
    if app_div == const.APP_BOARD:
        json_data = board_dao.get_board_info()
    else:
        json_data = func.get_input_data(app_div)

    # DataFrame変換
    df_all = pd.DataFrame(json_data)

    if app_div == const.APP_BOARD:
        df = df_all

        # データ型を int から str に変換
        df["nSeq"] = df["nSeq"].astype(str)

        # numpy.where()を使って新しい列を作成
        df[const.STR_URL] = np.where(
            df["nStatus"] == "対応完了",
            "-",
            func.get_a_tag(
                f"{URL_SERVER}/board/update/" + df["nSeq"], "☑", const.FLG_ON
            ),
        )

        df.columns = col_list_board

    elif app_div == const.APP_SITE:
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

        img_path = f"{URL_SERVER}/{const.STR_IMG}/"
        file_name = df_info[const.STR_IMG]

        if app_div == const.APP_CAFE:
            df_info[const.STR_IMG] = func.get_img_tag(img_path, file_name, "_menu")
            df_info[const.STR_URL] = func.get_img_tag(img_path, file_name, "_in")
            df = df_info[[const.STR_NAME, const.STR_ADDR, const.STR_IMG, const.STR_URL]]
            df.columns = col_list_cafe

        elif app_div == const.APP_TRAVEL:
            df_info[const.STR_IMG] = func.get_img_tag(img_path, file_name)
            df = df_info[
                [const.STR_NAME, const.STR_DESCRIPTION, const.STR_ACCESS, const.STR_IMG]
            ]
            df.columns = col_list_travel

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
    app_div = const.APP_BOARD
    data_list = get_df_data(app_div)
    func.print_test_data(data_list.values.tolist())
