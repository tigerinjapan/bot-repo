# 説明：サーバー処理

from fastapi import Request

import apps.drama as drama
import apps.lcc as lcc
import apps.line as line
import apps.news as news
import apps.ranking as ranking
import apps.site as site
import apps.study as study
import apps.test as test
import apps.today as today
import apps.tv as tv
import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_api as func_api
import apps.utils.function_mongo as func_mongo
import apps.utils.message_constants as msg_const
from apps.utils.function_beautiful_soup import get_data_from_url

# アプリケーションリスト
LIST_APP_DIV = [today, news, drama, ranking, lcc, tv, study]
LIST_ALL_APP_DIV = LIST_APP_DIV + [site, site]

LIST_APP_NUM_OFF = [const.APP_TODAY, const.APP_STUDY, const.APP_SITE, const.APP_CAFE]


# クラスの定義
class AppExec:
    # 初期化メソッド（コンストラクタ）
    def __init__(self, app, name):
        self.app = app
        self.name = name

    # アプリケーション開始
    def start(self):
        func.print_start(self.name)

    # アプリケーション終了
    def end(self):
        func.print_end(self.name)

    # データ取得
    def data(self):
        df = get_df_info(self.name)
        data_list = get_data_list(df)
        return data_list


# 【画面】取得結果
def exec_result(request: Request, app_name: str):
    user_info = request.session[const.STR_USER]
    user_div, user_name = (
        user_info[const.FI_USER_DIV],
        user_info[const.FI_USER_NAME],
    )

    app_div_idx = const.LIST_ALL_APP_NAME.index(app_name)
    app_div = LIST_ALL_APP_DIV[app_div_idx]

    app_title = app_div.app_title

    if app_name == const.APP_CAFE:
        app_title = site.app_title_cafe

    num_flg = const.FLG_ON
    if func.check_in_list(app_name, LIST_APP_NUM_OFF):
        num_flg = const.FLG_OFF

    app_exec = AppExec(app_div, app_name)
    app_exec.start()

    if app_name in [const.APP_SITE, const.APP_CAFE]:
        df = site.get_df_data(user_div, app_name)
        data_list = get_data_list(df)
    else:
        data_list = app_exec.data()

    app_exec.end()

    target_html = const.HTML_RESULT
    context = {
        const.STR_REQUEST: request,
        "user_div": user_div,
        "user_name": user_name,
        "app_name": app_name,
        const.STR_TITLE: app_title,
        "data_list": data_list,
        "num_flg": num_flg,
    }
    return target_html, context


# 【画面】取得結果
def exec_user(request: Request, app_name: str):
    user_info = request.session[const.STR_USER]
    target_html = const.HTML_USER_INFO
    context = {
        const.STR_REQUEST: request,
        const.STR_TITLE: "ユーザー情報",
        "app_name": app_name,
        "user_info": user_info,
        "update_flg": const.FLG_ON,
    }
    return target_html, context


# 【画面】データリスト取得
def get_data_list(df) -> list[tuple[list[str], list[str]]]:
    data_list = []
    column_list = df.columns.to_list()
    data_val_list = df.values.tolist()

    data_info = [column_list, data_val_list]
    data_list.append(data_info)
    return data_list


# データフレーム取得
def get_df_info(app_name: str):
    df, file_path = func.get_df_from_json(app_name)
    if df.empty:
        update_news(app_name)
        df = func.get_df_read_json(file_path)
    return df


# データ更新
def update_news(app_name: str = const.SYM_BLANK):
    func.print_info_msg(const.FILE_TYPE_JSON, msg_const.MSG_INFO_PROC_START)

    app_div_list = LIST_APP_DIV
    app_name_list = const.LIST_APP_NAME

    if app_name:
        app_div_idx = app_name_list.index(app_name)
        app_div_list = [app_div_list[app_div_idx]]
        app_name_list = [app_name]

    for app_div, app_name in zip(app_div_list, app_name_list):
        app_exec = AppExec(app_div, app_name)
        app_exec.start()

        item_list = app_div.get_item_list()
        col_list = app_div.col_list

        df = func.get_df(item_list, col_list)

        if df.empty:
            func.print_info_msg(msg_const.MSG_ERR_DATA_NOT_EXIST)
            continue

        if app_name == const.APP_TV:
            df_sort = df.sort_values(
                by=app_div.sort_list,
                ascending=app_div.ascending_div,
            ).drop_duplicates(subset=app_div.duplicates_list, keep=const.STR_FIRST)
            df = df_sort

        func.df_to_json(app_name, df)

        app_exec.end()

    func.print_info_msg(const.FILE_TYPE_JSON, msg_const.MSG_INFO_PROC_COMPLETED)


# スリープ状態にならないようサーバーアクセス
def no_sleep():
    url = line.URL_KOYEB_APP
    get_data_from_url(url, headers=const.NONE_CONSTANT, sleep_flg=const.FLG_OFF)
    func.print_info_msg(msg_const.MSG_INFO_SERVER_KEEP_ALIVE)


# テストAPI
def test_api():
    url = f"{get_local_url}/protected-resource?token=token_{const.DATE_TODAY}"
    headers = {"Content-Type": "application/json"}
    response = func_api.get_response_result(url, headers=headers)
    response_json = func.get_loads_json(response.text)
    func.print_test_data(response_json, type_flg=const.FLG_ON)
    return response_json


# ローカルURL取得
def get_local_url() -> str:
    host, port = func.get_host_port()
    local_url = f"http://{host}:{port}"
    return local_url


if __name__ == const.MAIN_FUNCTION:
    update_news()
    # app_name = const.APP_STUDY
    # update_news(app_name)
    # test_api()
