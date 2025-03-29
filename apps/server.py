# 説明：サーバー処理

from threading import Thread

from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from functools import wraps
from datetime import datetime, timedelta
import secrets

from starlette.middleware.sessions import SessionMiddleware
from uvicorn import Config, Server

import apps.line as line
import apps.user as user
import apps.app_exec as sub
import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.message_constants as msg_const
from apps.utils.function_mongo import check_login
from apps.utils.user_dao import get_user_info

# fast api
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="secret_key")
templates = Jinja2Templates(directory="templates")

# トークン認証
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# トークン情報を保存する辞書 (メモリ内)
token_store = {}
TOKEN_EXPIRATION_MINUTES = 10  # トークン有効期限 (10分)
VALID_TOKEN = "secret-token"

# 開発データ
dev_user = func.get_input_data(const.STR_AUTH, const.STR_USER)


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
            access_token = "token_" + const.DATE_TODAY
            if token != access_token:
                raise HTTPException(status_code=403)
            return await func_(*args, **kwargs)
        except HTTPException as e:
            func.print_error_msg(msg_const.MSG_ERR_INVALID_TOKEN, e.detail)
            raise e

    return wrapper


@app.post("/token")
async def issue_token():
    # ランダムなトークンを生成
    token = secrets.token_hex(16)  # 32文字のランダムなトークン
    expiration = datetime.now() + timedelta(minutes=TOKEN_EXPIRATION_MINUTES)

    # トークン情報を保存
    token_data = {
        "access_token": token,
        "token_type": "bearer",
        "expiration": expiration,
    }
    return token_data


@app.get("/protected-resource")
async def protected_resource(token: str):
    expiration = datetime.now() + timedelta(minutes=TOKEN_EXPIRATION_MINUTES)

    if token_store:
        # トークンを検証
        token_data = token_store.get(token)  # TODO 追加テスト要
    else:
        access_token = "token_" + const.DATE_TODAY

    token_data = {
        "access_token": access_token,
        "token_type": "bearer",
        "expiration": expiration,
    }

    if not token_data or token != token_data["access_token"]:
        raise HTTPException(status_code=403, detail=msg_const.MSG_ERR_INVALID_TOKEN)

    # トークンの有効期限を確認
    # if expiration < datetime.now():
    #     raise HTTPException(status_code=403, detail="Token has expired")

    return {"message": "Access to the protected resource granted."}


@app.get(const.PATH_ROOT)
async def root(request: Request):

    # if func.is_local_env():
    #     request.session.clear()
    #     request.session[const.STR_USER] = dev_user

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
        response = RedirectResponse(url=const.PATH_NEWS, status_code=303)
        func.print_info_msg(user_info[const.FI_USER_NAME], msg_const.MSG_INFO_LOGIN)

    return response


@app.get(const.PATH_LOGOUT)
async def logout(request: Request):
    user_name = request.session[const.STR_USER][const.FI_USER_NAME]
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
    if app_name == const.APP_USER:
        target_html, context = sub.exec_user(request, app_name)
    else:
        target_html, context = sub.exec_result(request, app_name)
    return templates.TemplateResponse(target_html, context)


@app.post("/user/update")
async def user_update(request: Request, userId: str = Form(...)):
    # フォームデータをすべて取得
    form_data = await request.form()
    dict_data = dict(form_data)
    user.user_info_update(dict_data)
    user_info = get_user_info(userId)
    request.session[const.STR_USER] = user_info
    target_html, context = sub.exec_user(request, const.APP_USER)
    return templates.TemplateResponse(target_html, context)


@app.get("/json/{app_name}")
@token_required
async def app_json(request: Request):
    app_name = request.path_params["app_name"]
    result = func.get_json_data(app_name, const.STR_OUTPUT)
    return result


@app.get("/line/send")
async def send_msg():
    line.main()
    result = {const.STR_MESSAGE: "Line Message sent."}
    return result


@app.get("/templates/{file_name}")
async def temp(file_name: str):
    file_ext = func.get_path_split(file_name, extension_flg=const.FLG_ON)

    file_path = f"templates/{file_ext}/{file_name}"
    return FileResponse(file_path)


@app.get(f"/{const.STR_IMG}" + "/{file_div}/{file_name}")
async def img(file_div: str, file_name: str):
    image_path = func.get_file_path(file_name, const.FILE_TYPE_JPEG, file_div)
    return FileResponse(image_path)


@app.get(f"/{const.STR_FONT}" + "/{file_name}")
async def font(file_name: str):
    font_path = func.get_file_path(file_name, const.FILE_TYPE_TTC)
    return FileResponse(font_path)


@app.get("/test")
def test():
    message = test.main()
    if not message:
        message = "Server is on test."
    return {const.STR_MESSAGE: message}


if __name__ == const.MAIN_FUNCTION:
    start_thread()
