# 説明：サーバー処理

from threading import Thread

from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from uvicorn import Config, Server

import apps.cafe as cafe
import apps.lcc as lcc
import apps.line as line
import apps.news as news
import apps.ranking as ranking
import apps.site as site
import apps.study as study
import apps.today as today
import apps.tv as tv
import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.message_constants as msg_const
from apps.utils.function_beautiful_soup import get_data_from_url
from apps.utils.function_selenium import test_webdriver

# fast api
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="secret_key")
templates = Jinja2Templates(directory="templates")

# アプリケーションリスト
LIST_APP_DIV = [today, news, news, ranking, lcc, tv, study]
LIST_ALL_APP_DIV = LIST_APP_DIV + [site]

# ユーザーデータ
user_data = func.get_input_data(const.STR_AUTH, const.STR_USER)


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


# uvicornサーバー起動
def run_server():
    func.print_info_msg(msg_const.MSG_INFO_SERVER_START)

    host, port = func.get_host_port()
    config = Config(app, host=host, port=port)
    server = Server(config)
    server.run()


# スレッド開始
def start_thread():
    t = Thread(target=run_server)
    t.start()


@app.get(const.PATH_ROOT)
async def root(request: Request):

    if func.is_local_env():
        request.session.clear()
        request.session[const.STR_USER] = user_data.get(const.AUTH_DEV)

    user = request.session.get(const.STR_USER)
    if user:
        response = RedirectResponse(url=const.PATH_TODAY, status_code=303)
    else:
        context = {const.STR_REQUEST: request, const.STR_TITLE: const.SYSTEM_NAME}
        response = templates.TemplateResponse(const.HTML_INDEX, context)
    return response


@app.post(const.PATH_LOGIN)
async def login(
    request: Request, userId: str = Form(...), userPassword: str = Form(...)
):
    user_div = userId.split(const.SYM_AT)[0]
    user = user_data.get(user_div)
    if user and user["userId"] == userId and user["userPassword"] == userPassword:
        request.session[const.STR_USER] = user
        response = RedirectResponse(url=const.PATH_TODAY, status_code=303)
        func.print_info_msg(user["userName"], msg_const.MSG_INFO_LOGIN)

    else:
        chk_msg = msg_const.MSG_ERR_PASSWORD_INCORRECT
        if not user or user["userId"] != userId:
            chk_msg = msg_const.MSG_ERR_USER_NOT_EXIST
        request.session.clear()
        context = {
            const.STR_REQUEST: request,
            const.STR_TITLE: const.SYSTEM_NAME,
            "chk_msg": chk_msg,
        }
        response = templates.TemplateResponse(const.HTML_INDEX, context)

    return response


@app.get(const.PATH_LOGOUT)
async def logout(request: Request):
    user_name = request.session[const.STR_USER]["userName"]
    func.print_info_msg(user_name, msg_const.MSG_INFO_LOGOUT)
    request.session.clear()
    context = {
        const.STR_REQUEST: request,
        const.STR_TITLE: const.SYSTEM_NAME,
        "chk_msg": msg_const.MSG_INFO_LOGOUT,
    }
    return templates.TemplateResponse(const.HTML_INDEX, context)


@app.get("/app/{app_name}")
async def app_exec(request: Request, app_name: str):
    return exec_result(request, app_name)


@app.get("/json/{app_name}")
async def app_json(app_name: str):
    result = func.get_json_data(app_name, const.STR_OUTPUT)
    return result


@app.get("/line/send")
async def send_msg():
    line.main()
    result = {"message": "Line Message sent."}
    return result


@app.get("/templates/{file_name}")
async def temp(file_name: str):
    file_ext = func.get_path_split(file_name, extension_flg=const.FLG_ON)

    file_path = f"templates/{file_ext}/{file_name}"
    return FileResponse(file_path)


@app.get(f"/{const.STR_IMG}" + "/{file_name}")
async def img(file_name: str):
    image_path = func.get_file_path(file_name, const.FILE_TYPE_JPEG, const.STR_OUTPUT)
    return FileResponse(image_path)


@app.get("/test")
def test():
    message = cafe.main()
    if not message:
        message = "Server is on test."
    return {"message": message}


# 【画面】取得結果
def exec_result(request: Request, app_name: str):
    user = request.session[const.STR_USER]
    user_div, user_name = user["userDiv"], user["userName"]

    app_div_idx = const.LIST_ALL_APP_NAME.index(app_name)
    app_div = LIST_ALL_APP_DIV[app_div_idx]

    app_title = app_div.app_title

    if app_name == const.APP_KOREA:
        app_title = news.app_title_korea

    num_flg = const.FLG_ON
    if func.check_in_list(app_name, [const.APP_TODAY, const.APP_STUDY, const.APP_SITE]):
        num_flg = const.FLG_OFF

    app_exec = AppExec(app_div, app_name)
    app_exec.start()

    if app_name == const.APP_SITE:
        df = site.get_df_data(user_div)
        data_list = get_data_list(df)
    else:
        data_list = app_exec.data()

    app_exec.end()

    context = {
        const.STR_REQUEST: request,
        "user_div": user_div,
        "user_name": user_name,
        "app_name": app_name,
        const.STR_TITLE: app_title,
        "data_list": data_list,
        "num_flg": num_flg,
    }
    return templates.TemplateResponse(const.HTML_RESULT, context)


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

        if app_name == const.APP_KOREA:
            item_list = news.get_item_list(news.DIV_KOREA_NEWS_LIST)
            col_list = news.col_list_korea
        else:
            item_list = app_div.get_item_list()
            col_list = app_div.col_list

        df = func.get_df(item_list, col_list)

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


if __name__ == const.MAIN_FUNCTION:
    update_news()
    # app_name = const.APP_TODAY
    # update_news(app_name)
