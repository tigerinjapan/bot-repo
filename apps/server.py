# 説明: サーバー処理

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
import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.message_constants as msg_const
import apps.utils.user_dto as dto
from apps.utils.function_mongo import check_login
from apps.utils.rank_dao import update_rank_info_of_api
from apps.utils.user_dao import get_user_info, update_user_info_on_form


# fast api
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="secret_key")
templates = Jinja2Templates(directory="templates")

# トークン認証
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# トークン有効期限 (10分)
TOKEN_EXPIRATION_MINUTES = 10


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


# トークン認証
def token_required(func_):
    @wraps(func_)
    async def wrapper(*args, **kwargs):
        # トークンを検証
        request: Request = kwargs.get(const.STR_REQUEST)

        try:
            token = request.query_params.get("token")
            # token = await oauth2_scheme(request)

            # トークンを検証
            chk_msg = await protected_resource(request, token)
            if chk_msg:
                raise HTTPException(status_code=403, detail=chk_msg)

            return await func_(*args, **kwargs)
        except HTTPException as e:
            func.print_error_msg(e.detail)
            raise e

    return wrapper


@app.get("/protected-resource")
async def protected_resource(request: Request, token: str):
    chk_msg = const.SYM_BLANK

    # トークンを検証
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


@app.post("/token")
async def issue_token(request: Request):
    # ランダムなトークンを生成
    # access_token = secrets.token_hex(16)  # 32文字のランダムなトークン
    access_token = "token_" + const.DATE_TODAY
    expiration = datetime.now() + timedelta(minutes=TOKEN_EXPIRATION_MINUTES)

    # トークン情報を保存
    token_data = {
        const.STR_TOKEN: access_token,
        const.STR_TYPE: "bearer",
        # const.STR_EXPIRATION: expiration.strftime(const.DATE_FORMAT_OUTPUT_FILE),
    }
    request.session[const.STR_TOKEN] = token_data
    return token_data


@app.get(const.PATH_ROOT)
async def root(request: Request):
    user = request.session.get(const.STR_USER)
    if user:
        response = RedirectResponse(url=const.PATH_NEWS, status_code=303)
    else:
        context = {const.STR_REQUEST: request, const.STR_TITLE: const.SYSTEM_NAME}
        response = templates.TemplateResponse(const.HTML_INDEX, context)
    return response


@app.post(const.PATH_LOGIN)
async def login(request: Request, userId: str = Form(...), userPw: str = Form(...)):
    user_info = get_user_info(userId)

    chk_msg = check_login(userId, userPw, user_info)
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
            dto.FI_USER_ID: user_id,
            dto.FI_LAST_LOGIN_DATE: datetime.now(),
        }
        update_user_info_on_form(update_data, form_flg=const.FLG_OFF)
        response = RedirectResponse(url=const.PATH_NEWS, status_code=303)
        func.print_info_msg(user_info[dto.FI_USER_NAME], msg_const.MSG_INFO_LOGIN)

    return response


@app.get(const.PATH_LOGOUT)
async def logout(request: Request):
    user_name = request.session[const.STR_USER][dto.FI_USER_NAME]
    func.print_info_msg(user_name, msg_const.MSG_INFO_LOGOUT)
    request.session.clear()
    context = {
        const.STR_REQUEST: request,
        const.STR_TITLE: const.SYSTEM_NAME,
        const.STR_MESSAGE: msg_const.MSG_INFO_LOGOUT,
    }
    return templates.TemplateResponse(const.HTML_INDEX, context)


@app.get("/app/{app_name}")
async def app_exec(request: Request, app_name: str):
    try:
        if app_name == const.APP_USER:
            target_html, context = appl.exec_user(request, app_name)
        elif app_name == const.APP_NUMBER:
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


@app.post("/user/update")
async def user_update(request: Request, userId: str = Form(...)):
    # フォームデータをすべて取得
    form_data = await request.form()
    dict_data = dict(form_data)
    update_user_info_on_form(dict_data)
    user_info = get_user_info(userId)
    request.session[const.STR_USER] = user_info
    target_html, context = appl.exec_user(request, const.APP_USER)
    return templates.TemplateResponse(target_html, context)


@app.get("/json/{app_name}")
# /json/today?token=token
@token_required
async def app_json(request: Request):
    app_name = request.path_params["app_name"]
    result = func.get_json_data(app_name, const.STR_OUTPUT)
    return result


@app.get("/api/{api_name}/{param}")
# /api/zipCode/1000000
async def app_api(request: Request):
    api_name = request.path_params["api_name"]
    param = request.path_params["param"]
    json_data = func.get_json_data(api_name)
    result = json_data.get(param)
    return result


@app.post("/number/ranking")
async def ranking_update(request: Request):
    # データ取得
    json_data = await request.json()
    update_rank_info_of_api(json_data)
    result = {const.STR_MESSAGE: "完了しました。"}
    return result


@app.get("/line/send")
async def send_msg():
    line.main()
    result = {const.STR_MESSAGE: "Line Message sent."}
    return result


@app.get(const.PATH_UPDATE)
async def update_news():
    appl.update_news()
    line.get_msg_data_today()
    result = {const.STR_MESSAGE: msg_const.MSG_INFO_PROC_COMPLETED}
    return result


@app.get("/templates/{file_name}")
async def temp(file_name: str):
    file_ext = func.get_path_split(file_name, extension_flg=const.FLG_ON)
    file_path = f"templates/{file_ext}/{file_name}"
    return FileResponse(file_path)


@app.get(f"/{const.STR_IMG}" + "/{file_name}")
# /img/today
async def img(file_name: str):
    file_div = const.STR_INPUT
    if const.APP_TODAY in file_name:
        file_div = const.STR_OUTPUT
    image_path = func.get_file_path(file_name, const.FILE_TYPE_JPEG, file_div)
    return FileResponse(image_path)


@app.get(f"/{const.STR_FONT}" + "/{file_name}")
# /font/meiryo
async def font(file_name: str):
    font_path = func.get_file_path(file_name, const.FILE_TYPE_TTC)
    return FileResponse(font_path)


@app.get("/check")
def health_check():
    # スリープ状態にならないようサーバーアクセス
    appl.no_sleep()
    info_msg = msg_const.MSG_INFO_SERVER_KEEP_ALIVE
    func.print_info_msg(info_msg)
    result = {const.STR_MESSAGE: info_msg}
    return result


@app.get("/test")
def api_test():
    message = test.main()
    if not message:
        message = "Server is on test."
    return {const.STR_MESSAGE: message}


if __name__ == const.MAIN_FUNCTION:
    start_thread()
    # health_check()
