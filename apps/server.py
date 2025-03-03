# 説明：サーバー処理

from threading import Thread

from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from uvicorn import Config, Server

import apps.lcc as lcc
import apps.news as news
import apps.ranking as ranking
import apps.study as study
import apps.today as today
import apps.tv as tv
import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.message_constants as msg_const

# fast api
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="secret_key")
templates = Jinja2Templates(directory="templates")

# アプリケーションリスト
LIST_APP_DIV = [today, news, news, ranking, lcc, tv, study]

# ユーザーデータ
users_data = func.get_input_data(const.STR_AUTH, const.STR_USER)


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
        data_list = get_data_list(self.name)
        return data_list


def run():
    host, port = func.get_host_port()

    # uvicornサーバー起動
    config = Config(app, host=host, port=port)
    server = Server(config)
    server.run()


# スレッド開始
def start_thread():
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
        func.print_info_msg(user["userName"], msg_const.MSG_INFO_LOGIN)

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
    user_name = request.session[const.STR_USER]["userName"]
    func.print_info_msg(user_name, msg_const.MSG_INFO_LOGOUT)
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
    app_div = news
    app_name = const.APP_KOREA
    return exec_result(request, app_div, app_name)


@app.get(const.PATH_RANKING)
async def ranking_info(request: Request):
    app_div = ranking
    return exec_result(request, app_div)


@app.get(const.PATH_LCC)
async def lcc_news(request: Request):
    app_div = lcc
    return exec_result(request, app_div)


@app.get(const.PATH_TV)
async def tv_list(request: Request):
    app_div = tv
    return exec_result(request, app_div)


@app.get(const.PATH_STUDY)
async def study_korean(request: Request):
    app_div = study
    return exec_result(request, app_div)


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
async def test():
    return {"message": "[test] Server is on test."}


# 【画面】取得結果
def exec_result(request: Request, app_div, sub_div: str = const.SYM_BLANK):
    app_name = app_div.app_name
    app_title = app_div.app_title

    if sub_div:
        app_name = sub_div
        if sub_div == const.APP_KOREA:
            app_title = news.app_title_korea

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


# 【画面】データリスト取得
def get_data_list(app_name: str) -> list[tuple[list[str], list[str]]]:
    data_list = []
    df, file_path = func.get_df_from_json(app_name)
    if df.empty:
        update_news(app_name)
        df = func.get_df_read_json(file_path)

    column_list = df.columns.to_list()
    data_val_list = df.values.tolist()

    data_info = [column_list, data_val_list]
    data_list.append(data_info)
    return data_list


# 【画面】ウェブページの更新
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


if __name__ == const.MAIN_FUNCTION:
    # start_thread()
    # update_news()
    app_name = const.APP_RANKING
    update_news(app_name)
