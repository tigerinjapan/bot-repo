"""
アプリケーション実行
"""

import sys

from fastapi import Request

import apps.drama as drama
import apps.lcc as lcc
import apps.log as log
import apps.number as number
import apps.news as news
import apps.ranking as ranking
import apps.site as site
import apps.study as study
import apps.today as today
import apps.today_korea as today_korea
import apps.tv as tv
import apps.user as user
import apps.utils.board_dto as board_dto
import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_api as func_api
import apps.utils.message_constants as msg_const
import apps.utils.mongo_constants as mongo_const
import apps.utils.rank_dao as rank_dao

# スクリプト名
SCRIPT_NAME = func.get_app_name(__file__)

# アプリケーションリスト
LIST_APP_DIV = [today, news, drama, ranking, lcc, tv, study]
LIST_APP_DIV_SITE = [site] * 4
LIST_APP_DIV_KOREA = [today_korea]
LIST_ALL_APP_DIV = LIST_APP_DIV + LIST_APP_DIV_SITE + LIST_APP_DIV_KOREA


class AppExec:
    """
    アプリケーション実行クラス
    """

    def __init__(self, app, name):
        """
        初期化メソッド（コンストラクタ）
        """
        self.app = app
        self.name = name

    def start(self):
        """
        アプリケーション開始
        """
        func.print_start(self.name)

    def end(self):
        """
        アプリケーション終了
        """
        func.print_end(self.name)

    def data(self):
        """
        データ取得
        """
        df = get_df_info(self.name)
        data_list = get_data_list(df)
        return data_list


def get_context_data(request: Request, app_name: str):
    """
    【画面】データ取得
    """
    context = {}

    if not app_name in const.LIST_APP_ALL:
        return context

    if not func.check_in_list(app_name, const.LIST_APP_AUTH_OFF):
        user_info = request.session[const.STR_USER]
        user_div, user_name, app_menu = (
            user_info[mongo_const.FI_USER_DIV],
            user_info[mongo_const.FI_USER_NAME],
            user_info[mongo_const.FI_MENU],
        )
    else:
        user_div = user_name = app_menu = const.SYM_BLANK

    app_div_idx = const.LIST_APP_ALL.index(app_name)
    app_div = LIST_ALL_APP_DIV[app_div_idx]

    app_title = app_name
    if const.APP_TODAY in app_name:
        app_title = const.TITLE_TODAY_NEWS

    num_flg = (
        const.FLG_OFF
        if func.check_in_list(app_name, const.LIST_APP_NUM_OFF)
        else const.FLG_ON
    )

    app_exec = AppExec(app_div, app_name)
    app_exec.start()

    if app_name in const.LIST_APP_SITE:
        df = site.get_df_data(app_name, user_div)
        data_list = get_data_list(df)
    else:
        data_list = app_exec.data()

    app_exec.end()

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
    return context


def get_context_data_2(request: Request, app_name: str):
    """
    【画面】データ取得
    """
    context = {}

    user_name = const.SYM_BLANK
    session_user = request.session.get(const.STR_USER)
    if session_user:
        user_name = session_user[mongo_const.FI_USER_NAME]

    lang_cd = const.LANG_CD_JA
    split_str = const.SYM_UNDER
    if (
        split_str in app_name
        and const.STR_DESIGN not in app_name
        and const.STR_PROMPT not in app_name
    ):
        lang_cd = app_name.split(split_str)[1]
        app_name = app_name.split(split_str)[0]

    if not (lang_cd in const.LIST_LANG_CD and app_name in const.LIST_APPS_ALL):
        return context

    data_list = []
    if app_name == const.APP_NUMBER:
        data_list = func.get_json_data(app_name, const.STR_OUTPUT)

    elif app_name == const.APP_SUDOKU or app_name == const.APP_IT_QUIZ:
        data_list = rank_dao.get_ranking_top(app_name)

    elif app_name == const.APP_REVIEW:
        data_list.append(const.LIST_BOARD_APP)
        data_list.append(const.LIST_BOARD_CATEGORY)
        data_list.append(const.LIST_BOARD_TYPE)

    context = {
        const.STR_REQUEST: request,
        const.STR_TITLE: app_name,
        "app_name": app_name,
        "user_name": user_name,
        "lang_cd": lang_cd,
        "data_list": data_list,
    }

    return context


def get_context_for_user(request: Request, app_name: str):
    """
    【画面】ユーザーデータ取得
    """
    user_info = request.session[const.STR_USER]
    context = {
        const.STR_REQUEST: request,
        const.STR_TITLE: app_name,
        "app_name": app_name,
        "user_info": user_info,
        "update_flg": const.FLG_ON,
    }
    return context


def get_data_list(df) -> list[tuple[list[str], list[str]]]:
    """
    【画面】データリスト取得
    """
    data_list = []
    column_list = df.columns.to_list()
    data_val_list = df.values.tolist()

    data_info = [column_list, data_val_list]
    data_list.append(data_info)
    return data_list


def get_df_info(app_name: str):
    """
    DataFrameデータ取得
    """
    df, file_path = func.get_df_from_json(app_name)
    if df.empty:
        update_news(app_name)
        df = func.get_df_read_json(file_path)
    return df


def update_news(app_name: str = const.SYM_BLANK):
    """
    データ更新
    """
    curr_func_nm = sys._getframe().f_code.co_name
    func.print_start(curr_func_nm)

    app_div_list = LIST_APP_DIV
    app_name_list = const.LIST_APP_SERVER

    if app_name:
        if app_name == const.APP_TODAY_KOREA:
            app_div_list = [today_korea]
            app_name_list = [const.APP_TODAY_KOREA]

        elif app_name == const.APP_NUMBER:
            app_div_list = [number]
            app_name_list = [const.APP_NUMBER]

        else:
            app_div_idx = app_name_list.index(app_name)
            app_div_list = [app_div_list[app_div_idx]]
            app_name_list = [app_name]

    for app_div, app_name in zip(app_div_list, app_name_list):
        app_exec = AppExec(app_div, app_name)
        app_exec.start()

        skip_flg = const.FLG_OFF

        try:
            item_list = app_div.get_item_list()
            df = func.init_df()

            if item_list:
                col_list = app_div.col_list
                df = func.get_df(item_list, col_list)

            if df.empty:
                func.print_debug_msg(app_name, msg_const.MSG_INFO_DATA_NOT_EXIST)
                skip_flg = const.FLG_ON

        except Exception as e:
            func.print_error_msg(SCRIPT_NAME, curr_func_nm, app_name, e)
            skip_flg = const.FLG_ON

        if skip_flg:
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

    func.print_end(curr_func_nm)


def no_sleep():
    """
    スリープ状態にならないようサーバーアクセス
    """
    func_api.get_json_data_on_app(const.APP_TODAY)


if __name__ == const.MAIN_FUNCTION:
    # update_news(const.APP_STUDY)
    app_name_list = [const.APP_TODAY_KOREA, const.APP_TODAY]
    for app_name in app_name_list:
        update_news(app_name)
