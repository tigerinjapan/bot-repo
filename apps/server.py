# 説明: サーバー処理
# FastAPIによるWebサーバー。認証・セッション管理・各種APIエンドポイントを提供

from threading import Thread
from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from functools import wraps
from datetime import datetime, timedelta
from starlette.middleware.sessions import SessionMiddleware
from uvicorn import Config, Server

import apps.appl as appl
import apps.line as line
import apps.test as test
import apps.utils.board_dao as board_dao
import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_line as func_line
import apps.utils.message_constants as msg_const
import apps.utils.user_dao as user_dao
import apps.utils.user_dto as user_dto
import apps.utils.rank_dao as rank_dao

# FastAPIインスタンス生成とセッションミドルウェア追加
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="secret_key")
templates = Jinja2Templates(directory="templates")

# OAuth2トークン認証設定
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# トークン有効期限（分）
TOKEN_EXPIRATION_MINUTES = 10


# サーバー起動
def run_server():
    func.print_info_msg(msg_const.MSG_INFO_SERVER_START)
    host, port = func.get_host_port()
    config = Config(app, host=host, port=port)
    server = Server(config)
    server.run()


# サーバーを別スレッドで起動
def start_thread():
    t = Thread(target=run_server)
    t.start()


# トークン認証
def token_required(func_):
    @wraps(func_)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs.get(const.STR_REQUEST)
        try:
            token = request.query_params.get("token")
            chk_msg = await protected_resource(request, token)
            if chk_msg:
                raise HTTPException(status_code=403, detail=chk_msg)
            return await func_(*args, **kwargs)
        except HTTPException as e:
            func.print_error_msg(e.detail)
            raise e

    return wrapper


# トークン検証API
@app.get("/protected-resource")
async def protected_resource(request: Request, token: str):
    chk_msg = const.SYM_BLANK
    token_store = await issue_token(request)
    if token_store:
        access_token = token_store[const.STR_TOKEN]
        if access_token:
            if token != access_token:
                chk_msg = msg_const.MSG_ERR_INVALID_TOKEN
        else:
            chk_msg = msg_const.MSG_ERR_TOKEN_NOT_EXIST
    else:
        chk_msg = msg_const.MSG_ERR_TOKEN_NOT_EXIST
    return chk_msg


# トークン発行API
@app.post("/token")
async def issue_token(request: Request):
    access_token = "token_" + const.DATE_TODAY
    expiration = datetime.now() + timedelta(minutes=TOKEN_EXPIRATION_MINUTES)
    token_data = {
        const.STR_TOKEN: access_token,
        const.STR_TYPE: "bearer",
    }
    request.session[const.STR_TOKEN] = token_data
    return token_data


# ルートページ（ログイン状態でリダイレクト）
@app.get(const.PATH_ROOT)
async def root(request: Request):
    user = request.session.get(const.STR_USER)
    if user:
        response = RedirectResponse(url=const.PATH_APP_NEWS, status_code=303)
    else:
        context = {const.STR_REQUEST: request, const.STR_TITLE: const.SYSTEM_NAME}
        response = templates.TemplateResponse(const.HTML_INDEX, context)
    return response


# ログイン処理
@app.post(const.PATH_LOGIN)
async def login(request: Request, userId: str = Form(...), userPw: str = Form(...)):
    user_info = user_dao.get_user_info(userId)
    chk_msg = user_dao.check_login(userId, userPw, user_info)
    if chk_msg:
        request.session.clear()
        context = {
            const.STR_REQUEST: request,
            const.STR_TITLE: const.SYSTEM_NAME,
            const.STR_MESSAGE: chk_msg,
        }
        response = templates.TemplateResponse(const.HTML_INDEX, context)
    else:
        request.session[const.STR_USER] = user_info
        user_id = func.get_masking_data(userId)
        update_data = {
            user_dto.FI_USER_ID: user_id,
            user_dto.FI_LAST_LOGIN_DATE: datetime.now(),
        }
        user_dao.update_user_info_on_form(update_data, form_flg=const.FLG_OFF)
        response = RedirectResponse(url=const.PATH_APP_NEWS, status_code=303)
        func.print_info_msg(user_info[user_dto.FI_USER_NAME], msg_const.MSG_INFO_LOGIN)
    return response


# ログアウト処理
@app.get(const.PATH_LOGOUT)
async def logout(request: Request):
    user_name = request.session[const.STR_USER][user_dto.FI_USER_NAME]
    func.print_info_msg(user_name, msg_const.MSG_INFO_LOGOUT)
    request.session.clear()
    context = {
        const.STR_REQUEST: request,
        const.STR_TITLE: const.SYSTEM_NAME,
        const.STR_MESSAGE: msg_const.MSG_INFO_LOGOUT,
    }
    return templates.TemplateResponse(const.HTML_INDEX, context)


# アプリケーション実行（ユーザー・数値・結果）
@app.get("/app/{app_name}")
async def app_exec(request: Request, app_name: str):
    try:
        if app_name == const.APP_USER:
            target_html, context = appl.exec_user(request, app_name)
        elif const.APP_NUMBER in app_name:
            target_html, context = appl.exec_number(request, app_name)
        else:
            target_html, context = appl.exec_result(request, app_name)
    except Exception as e:
        func.print_error_msg(app_name, e)
        target_html = const.HTML_INDEX
        context = {
            const.STR_REQUEST: request,
            const.STR_TITLE: const.SYSTEM_NAME,
            const.STR_MESSAGE: msg_const.MSG_INFO_SESSION_EXPIRED,
        }
    return templates.TemplateResponse(target_html, context)


# HTMLテンプレートファイルの返却
@app.get("/apps/{app_name}")
async def apps(request: Request, app_name: str):
    if "_design" in app_name:
        file_path = f"templates/{app_name}.{const.FILE_TYPE_HTML}"
        return FileResponse(file_path)
    else:
        target_html = const.HTML_RESULT_2
        context = {const.STR_REQUEST: request, "app_name": app_name}
        return templates.TemplateResponse(target_html, context)


# ユーザー情報更新（フォーム）
@app.post("/user/update")
async def user_update(request: Request, userId: str = Form(...)):
    form_data = await request.form()
    dict_data = dict(form_data)
    user_dao.update_user_info_on_form(dict_data)
    user_info = user_dao.get_user_info(userId)
    request.session[const.STR_USER] = user_info
    target_html, context = appl.exec_user(request, const.APP_USER)
    return templates.TemplateResponse(target_html, context)


# JSONデータ取得（認証付き）（例：/json/today?token=token）
@app.get("/json/{app_name}")
@token_required
async def app_json(request: Request):
    app_name = request.path_params["app_name"]
    result = func.get_json_data(app_name, const.STR_OUTPUT)
    return result


# APIデータ取得（例：/api/zipCode/1000000）
@app.get("/api/{api_name}/{param}")
async def app_api(request: Request):
    api_name = request.path_params["api_name"]
    param = request.path_params["param"]
    json_data = func.get_json_data(api_name)
    result = json_data.get(param)
    return result


# ランキング情報更新
@app.post("/number/ranking")
async def ranking_update(request: Request):
    json_data = await request.json()
    if func.is_network():
        rank_dao.update_rank_info_of_api(json_data)
    result = {const.STR_MESSAGE: msg_const.MSG_INFO_PROC_COMPLETED}
    return result


# 掲示板データ保存
@app.post("/board/add")
async def board_add(request: Request):
    try:
        json_data = await request.json()
        board_dao.insert_board_data_of_api(json_data)
        message = msg_const.MSG_INFO_PROC_COMPLETED

        if not func.is_local_env():
            msg = json_data
            func_line.send_text_msg(msg)

    except Exception as e:
        func.print_error_msg(const.COLL_BOARD, e)
        message = msg_const.MSG_ERR_PROC_FAILED

    result = {const.STR_MESSAGE: message}
    return result


# 掲示板データ・ステータス更新
@app.get("/board/update/{seq}")
async def board_update(seq):
    try:
        board_dao.update_board_status(seq)
    except Exception as e:
        func.print_error_msg(const.COLL_BOARD, e)

    return RedirectResponse(url=const.PATH_APP_BOARD)


# LINEメッセージ送信
@app.get("/line/send")
async def send_msg():
    line.main()
    result = {const.STR_MESSAGE: "Line Message sent."}
    return result


# ニュース情報更新
@app.get(const.PATH_UPDATE)
async def update_news():
    appl.update_news()
    line.get_msg_data_today()
    result = {const.STR_MESSAGE: msg_const.MSG_INFO_PROC_COMPLETED}
    return result


# テンプレートファイル取得
@app.get("/templates/{file_name}")
async def temp(file_name: str):
    file_ext = func.get_path_split(file_name, extension_flg=const.FLG_ON)
    file_path = f"templates/{file_ext}/{file_name}"
    return FileResponse(file_path)


# 画像ファイル取得（例：/img/today）
@app.get(f"/{const.STR_IMG}" + "/{file_name}")
async def img(file_name: str):
    file_div = const.STR_INPUT
    if const.APP_TODAY in file_name:
        file_div = const.STR_OUTPUT
    image_path = func.get_file_path(file_name, const.FILE_TYPE_JPEG, file_div)
    return FileResponse(image_path)


# フォントファイル取得（例：/font/meiryo）
@app.get(f"/{const.STR_FONT}" + "/{file_name}")
async def font(file_name: str):
    font_path = func.get_file_path(file_name, const.FILE_TYPE_TTC)
    return FileResponse(font_path)


# サーバーのヘルスチェック
@app.get("/check")
def health_check():
    appl.no_sleep()
    info_msg = msg_const.MSG_INFO_SERVER_KEEP_WORKING
    func.print_info_msg(info_msg)
    result = {const.STR_MESSAGE: info_msg}
    return result


# テストAPI
@app.get("/test")
def api_test():
    message = test.main()
    if not message:
        message = "Server is on test."
    return {const.STR_MESSAGE: message}


# メイン関数（サーバースレッド起動）
if __name__ == const.MAIN_FUNCTION:
    start_thread()
    # health_check()
