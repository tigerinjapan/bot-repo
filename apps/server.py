# 説明：サーバー処理

from threading import Thread

from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from uvicorn import Config, Server

import apps.korea as korea
import apps.lcc as lcc
import apps.news as news
import apps.today as today
import apps.tv as tv
import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.message_constants as msg_const
from apps.utils.function_selenium import test_access_webdriver

# fast api
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="secret_key")
templates = Jinja2Templates(directory="templates")

# ユーザーデータ
users_data = func.get_auth_data(const.STR_USER)


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
        data_list = get_data_list(self.app, self.name)
        return data_list


def run():
    host, port = func.get_host_port()

    # uvicornサーバー起動
    config = Config(app, host=host, port=port)
    server = Server(config)
    server.run()


# スレッド開始
def start_thread():
    # test_access_webdriver()  # TODO テスト後、削除
    t = Thread(target=run)
    t.start()


@app.get(const.PATH_ROOT)
async def root(request: Request):

    if func.is_local_env():
        request.session.clear()
        request.session[const.STR_USER] = users_data.get(const.AUTH_DEV)

    user = request.session.get(const.STR_USER)
    if user:
        response = RedirectResponse(url=const.PATH_TODAY, status_code=303)
    else:
        response = templates.TemplateResponse(
            "index.html", {const.STR_REQUEST: request}
        )
    return response


@app.post(const.PATH_LOGIN)
async def login(
    request: Request, userId: str = Form(...), userPassword: str = Form(...)
):
    user_div = userId.split(const.SYM_AT)[0]
    user = users_data.get(user_div)
    if user and user["userId"] == userId and user["userPassword"] == userPassword:
        request.session[const.STR_USER] = user
        response = RedirectResponse(url=const.PATH_TODAY, status_code=303)

    else:
        chk_msg = msg_const.MSG_ERR_PASSWORD_INCORRECT
        if not user or user["userId"] != userId:
            chk_msg = msg_const.MSG_ERR_USER_NOT_EXIST
        request.session.clear()
        context = {const.STR_REQUEST: request, "chk_msg": chk_msg}
        response = templates.TemplateResponse(const.HTML_INDEX, context)

    return response


@app.get(const.PATH_LOGOUT)
async def logout(request: Request):
    request.session.clear()
    context = {const.STR_REQUEST: request, "chk_msg": msg_const.MSG_INFO_LOGOUT}
    return templates.TemplateResponse(const.HTML_INDEX, context)


@app.get(const.PATH_TODAY)
async def today_info(request: Request):
    app_div = today
    return exec_result(request, app_div)


@app.get(const.PATH_NEWS)
async def news_info(request: Request):
    app_div = news
    return exec_result(request, app_div)


@app.get(const.PATH_KOREA)
async def korea_info(request: Request):
    app_div = korea
    return exec_result(request, app_div)


@app.get(const.PATH_LCC)
async def lcc_news(request: Request):
    app_div = lcc
    return exec_result(request, app_div)


@app.get(const.PATH_TV)
async def tv_list(request: Request):
    app_div = tv
    return exec_result(request, app_div)


def exec_result(request: Request, app_div):
    app_name = app_div.app_name
    app_title = app_div.app_title

    app_exec = AppExec(app_div, app_name)
    app_exec.start()
    data_list = app_exec.data()
    app_exec.end()

    user = request.session[const.STR_USER]
    context = {
        const.STR_REQUEST: request,
        "user_div": user["userDiv"],
        "user_name": user["userName"],
        "app_name": app_name,
        "title": app_title,
        "data_list": data_list,
    }
    return templates.TemplateResponse(const.HTML_RESULT, context)


# データリスト取得
def get_data_list(app_div, app_name: str) -> list[tuple[list[str], list[str]]]:

    if app_name in ["news", "korea"]:
        return app_div.get_data_list()  # TODO データリスト修正

    data_list = []
    df = func.get_df_from_json(app_name)
    column_list = df.columns.to_list()
    data_val_list = df.values.tolist()

    data_info = [column_list, data_val_list]
    data_list.append(data_info)
    return data_list


# ニュース更新：ウェブページの更新
def update_news():
    # app_div_list = [today, news, korea, lcc, tv] # TODO
    app_div_list = [today, lcc, tv]
    app_name_list = ["today", "lcc", "tv"]

    for app_div, app_name in zip(app_div_list, app_name_list):
        item_list = app_div.get_item_list()
        df = func.get_df(item_list, app_div.col_list)
        func.df_to_json(app_name, df)


@app.get("/templates/{file_name}")
async def temp(file_name: str):
    file_ext = func.get_path_split(file_name, extension_flg=const.FLG_ON)

    file_path = f"templates/{file_ext}/{file_name}"
    return FileResponse(file_path)


@app.get("/img/{file_name}")
async def img(file_name: str):
    image_path = func.get_file_path(file_name, const.FILE_TYPE_JPEG, const.STR_OUTPUT)
    return FileResponse(image_path)


@app.get("/test")
async def test():
    return {"message": "[test] Server is on test."}


if __name__ == const.MAIN_FUNCTION:
    start_thread()
