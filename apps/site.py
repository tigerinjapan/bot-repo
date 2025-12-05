"""
サイトメニュー
"""

import numpy as np

import apps.utils.board_dao as board_dao
import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.mongo_constants as mongo_const

# カラムリスト
col_list = [
    const.STR_DIV,
    const.STR_TITLE,
    const.STR_CONTENTS,
]
col_list_cafe = [const.STR_NAME, const.STR_ADDR, "menu", "interior"]
col_list_travel = [const.STR_DIV, const.STR_CONTENTS, const.STR_ACCESS, const.STR_IMG]
col_list_board = [
    mongo_const.ITEM_SEQ,
    mongo_const.ITEM_APP,
    mongo_const.ITEM_CATEGORY,
    mongo_const.ITEM_TYPE,
    mongo_const.ITEM_CONTENTS,
    mongo_const.ITEM_REMARK,
    mongo_const.ITEM_STATUS,
    const.STR_USER,
    const.STR_UPDATE,
]
col_list_board_all = col_list_board + [const.STR_CHECK]

menu_travel_div = ["両替所", "観光地", "レストラン", "その他"]

# URL
URL_SERVER = func.get_server_url()


def get_df_data(app_div: str, user_div: str = const.AUTH_DEV):
    """
    DataFrameのデータ取得
    """
    # JSONデータ取得
    if app_div == const.APP_BOARD:
        json_data = board_dao.get_board_info(user_div)
    else:
        json_data = func.get_input_data(app_div)

    # DataFrame変換
    df_all = func.get_df(json_data)

    if app_div == const.APP_BOARD:
        df = df_all
        col_list_ = col_list_board

        # データ型を int から str に変換
        df[mongo_const.FI_SEQ] = df[mongo_const.FI_SEQ].astype(str)

        user_auth = func.get_auth_num(user_div)
        if user_auth == const.NUM_AUTH_ADMIN:
            # numpy.where()を使って新しい列を作成
            df[const.STR_URL] = func.get_dialog_button(
                df[mongo_const.FI_SEQ],
                df[mongo_const.FI_REMARK],
                np.where(
                    df[mongo_const.FI_STATUS]
                    == const.LIST_BOARD_STATUS[const.STATUS_DONE],
                    "✅",
                    "▶️",
                ),
            )

            col_list_ = col_list_board_all

        df.columns = col_list_

    elif app_div == const.APP_SITE:
        user_auth = func.get_auth_num(user_div)
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


if __name__ == const.MAIN_FUNCTION:
    app_div = const.APP_BOARD
    data_list = get_df_data(app_div)
    func.print_test_data(data_list.values.tolist())
