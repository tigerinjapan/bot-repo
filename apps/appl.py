# 説明: アプリケーション実行

import sys

from fastapi import Request

import apps.drama as drama
import apps.lcc as lcc
import apps.number as number
import apps.news as news
import apps.ranking as ranking
import apps.site as site
import apps.study as study
import apps.today as today
import apps.today_korea as today_korea
import apps.tv as tv
import apps.user as user
import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_api as func_api
import apps.utils.message_constants as msg_const
import apps.utils.user_dto as dto

# スクリプト名
SCRIPT_NAME = func.get_app_name(__file__)

# アプリケーションリスト
LIST_APP_DIV = [today, news, drama, ranking, lcc, tv, study]
LIST_APP_DIV_KOREA = [today_korea]
LIST_ALL_APP_DIV = LIST_APP_DIV + ([site] * 4) + LIST_APP_DIV_KOREA

LIST_APP_NUM_OFF = [
    const.APP_TODAY,
    const.APP_STUDY,
    const.APP_SITE,
    const.APP_CAFE,
    const.APP_TRAVEL,
    const.APP_BOARD,
    const.APP_TODAY_KOREA,
]

LIST_APP_AUTH_OFF = [const.APP_CAFE, const.APP_TRAVEL, const.APP_TODAY_KOREA]


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
    if not func.check_in_list(app_name, LIST_APP_AUTH_OFF):
        user_info = request.session[const.STR_USER]
        user_div, user_name, app_menu = (
            user_info[dto.FI_USER_DIV],
            user_info[dto.FI_USER_NAME],
            user_info[dto.FI_MENU],
        )
    else:
        user_div = user_name = app_menu = const.SYM_BLANK

    app_title, data_list, num_flg = get_context_data(app_name, user_div)

    target_html = const.HTML_RESULT
    context = {
        const.STR_REQUEST: request,
        const.STR_TITLE: app_title,
        "user_div": user_div,
        "user_name": user_name,
        "app_name": app_name,
        "app_menu": app_menu,
        "data_list": data_list,
        "num_flg": num_flg,
    }
    return target_html, context


# 【画面】パラメータ取得
def get_context_data(app_name: str, user_div: str = const.AUTH_DEV):
    app_div_idx = const.LIST_ALL_APP_NAME.index(app_name)
    app_div = LIST_ALL_APP_DIV[app_div_idx]

    app_title = app_div.app_title

    if app_name == const.APP_CAFE:
        app_title = site.app_title_cafe
    elif app_name == const.APP_TRAVEL:
        app_title = site.app_title_travel
    elif app_name == const.APP_BOARD:
        app_title = site.app_title_board

    num_flg = const.FLG_ON
    if func.check_in_list(app_name, LIST_APP_NUM_OFF):
        num_flg = const.FLG_OFF

    app_exec = AppExec(app_div, app_name)
    app_exec.start()

    if app_name in const.LIST_APP_SITE:
        df = site.get_df_data(app_name, user_div)
        data_list = get_data_list(df)
    else:
        data_list = app_exec.data()

    app_exec.end()

    return app_title, data_list, num_flg


# 【画面】表示データ取得
def exec_user(request: Request, app_name: str):
    user_info = request.session[const.STR_USER]
    target_html = const.HTML_USER_INFO
    context = {
        const.STR_REQUEST: request,
        const.STR_TITLE: user.app_title,
        "app_name": app_name,
        "user_info": user_info,
        "update_flg": const.FLG_ON,
    }
    return target_html, context


# 【画面】表示データ取得
def exec_number(request: Request, app_name: str):
    lang = const.LANG_JA
    level = const.STR_HARD
    num = number.get_random_number(level)
    ans = number.get_answer_by_number(num)
    rank_user, rank_time = number.get_ranking_info(num)

    if const.SYM_UNDER in app_name:
        lang = app_name.split(const.SYM_UNDER)[1]
        app_name = app_name.split(const.SYM_UNDER)[0]

    target_html = const.HTML_NUMBER_PLATE
    context = {
        const.STR_REQUEST: request,
        const.STR_TITLE: number.app_title,
        "app_name": app_name,
        "lang": lang,
        "level": level,
        "num": num,
        "ans": ans,
        "rank_user": rank_user,
        "rank_time": rank_time,
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
    curr_func_nm = sys._getframe().f_code.co_name
    func.print_start(curr_func_nm, msg_const.MSG_INFO_PROC_START)

    app_div_list = LIST_APP_DIV
    app_name_list = const.LIST_APP_NAME

    if app_name:
        if app_name == const.APP_TODAY_KOREA:
            app_div_list = [today_korea]
            app_name_list = [const.APP_TODAY_KOREA]

        else:
            app_div_idx = app_name_list.index(app_name)
            app_div_list = [app_div_list[app_div_idx]]
            app_name_list = [app_name]

    for app_div, app_name in zip(app_div_list, app_name_list):
        app_exec = AppExec(app_div, app_name)
        app_exec.start()

        try:
            item_list = app_div.get_item_list()
            if not item_list:
                raise Exception
        except Exception as e:
            func.print_error_msg(SCRIPT_NAME, curr_func_nm, app_name, e)
            app_exec.end()
            continue

        col_list = app_div.col_list

        df = func.get_df(item_list, col_list)

        if df.empty:
            func.print_error_msg(
                SCRIPT_NAME, curr_func_nm, app_name, msg_const.MSG_ERR_DATA_NOT_EXIST
            )
            app_exec.end()
            continue

        if app_name == const.APP_TV:
            df_sort = df.sort_values(
                by=app_div.sort_list,
                ascending=app_div.ascending_div,
            ).drop_duplicates(subset=app_div.duplicates_list, keep=const.STR_FIRST)
            df = df_sort

        func.df_to_json(app_name, df)

        app_exec.end()

    func.print_end(curr_func_nm, msg_const.MSG_INFO_PROC_COMPLETED)


# スリープ状態にならないようサーバーアクセス
def no_sleep():
    func_api.get_result_on_app(const.APP_TODAY)


if __name__ == const.MAIN_FUNCTION:
    # update_news()
    app_name_list = [const.APP_TODAY, const.APP_TODAY_KOREA]
    for app_name in app_name_list:
        update_news(app_name)
