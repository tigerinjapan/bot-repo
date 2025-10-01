# 説明: サーバー処理
# FastAPIによるWebサーバー。認証・セッション管理・各種APIエンドポイントを提供

import sys

from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates

from functools import wraps
from starlette.middleware.sessions import SessionMiddleware
from threading import Thread
from uvicorn import Config, Server

import apps.appl as appl
import apps.kakao as kakao
import apps.line as line
import apps.test as test
import apps.utils.board_dao as board_dao
import apps.utils.board_dto as board_dto
import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_gemini as func_gemini
import apps.utils.function_kakao as func_kakao
import apps.utils.function_line as func_line
import apps.utils.message_constants as msg_const
import apps.utils.mongo_constants as mongo_const
import apps.utils.rank_dao as rank_dao
import apps.utils.user_dao as user_dao

# スクリプト名
SCRIPT_NAME = func.get_app_name(__file__)

# トークン有効期限（分）
TOKEN_EXPIRATION_MINUTES = 10

# FastAPIインスタンス生成とセッションミドルウェア追加
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="secret_key")
templates = Jinja2Templates(directory="templates")

# OAuth2トークン認証設定
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# サーバー起動
def run_server():
    func.print_start(SCRIPT_NAME, msg_const.MSG_INFO_SERVER_START)
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
                err_msg = f"{chk_msg} {request.url._url}"
                raise HTTPException(
                    status_code=const.STATUS_CODE_UNAUTHORIZED, detail=err_msg
                )
            return await func_(*args, **kwargs)

        except HTTPException as e:
            curr_func_nm = sys._getframe().f_code.co_name
            func.print_error_msg(SCRIPT_NAME, curr_func_nm, e.detail)
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
    access_token = "token_" + func.get_now(const.DATE_TODAY)
    # expiration = func.get_calc_date(TOKEN_EXPIRATION_MINUTES, const.DATE_MIN)
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
            mongo_const.FI_USER_ID: user_id,
            mongo_const.FI_LAST_LOGIN_DATE: func.get_now(),
        }
        user_dao.update_user_info_on_form(update_data, form_flg=const.FLG_OFF)
        response = RedirectResponse(url=const.PATH_APP_NEWS, status_code=303)
        func.print_info_msg(
            user_info[mongo_const.FI_USER_NAME],
            msg_const.MSG_INFO_LOGIN,
        )
    return response


# ログアウト処理
@app.get(const.PATH_LOGOUT)
async def logout(request: Request):
    user_name = request.session[const.STR_USER][mongo_const.FI_USER_NAME]
    func.print_info_msg(user_name, msg_const.MSG_INFO_LOGOUT)
    request.session.clear()
    context = {
        const.STR_REQUEST: request,
        const.STR_TITLE: const.SYSTEM_NAME,
        const.STR_MESSAGE: msg_const.MSG_INFO_LOGOUT,
    }
    return templates.TemplateResponse(const.HTML_INDEX, context)


# アプリケーション実行
@app.get("/app/{app_name}")
async def app_exec(request: Request, app_name: str):
    curr_func_nm = sys._getframe().f_code.co_name

    try:
        if app_name == const.APP_USER:
            target_html, context = appl.exec_user(request, app_name)
        elif const.APP_NUMBER in app_name:
            target_html, context = appl.exec_number(request, app_name)
        else:
            if not app_name in const.LIST_ALL_APP_NAME:
                except_http_error(curr_func_nm, request.url._url)

            target_html, context = appl.exec_result(request, app_name)

    except Exception as e:
        func.print_error_msg(SCRIPT_NAME, curr_func_nm, app_name, e)
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
    if not app_name in const.LIST_APPS_NAME:
        curr_func_nm = sys._getframe().f_code.co_name
        except_http_error(curr_func_nm, request.url._url)

    data_list = []
    if app_name == const.APP_REVIEW:
        data_list.append(board_dto.LIST_APP)
        data_list.append(board_dto.LIST_CATEGORY)
        data_list.append(board_dto.LIST_TYPE)

    context = {const.STR_REQUEST: request, "app_name": app_name, "data_list": data_list}

    target_html = const.HTML_RESULT_2
    return templates.TemplateResponse(target_html, context)


# HTMLテンプレートファイルの返却
@app.get("/apps/v1/{app_name}")
async def apps_v1(app_name: str):
    if not app_name in const.LIST_APPS_NAME_2:
        curr_func_nm = sys._getframe().f_code.co_name
        except_http_error(curr_func_nm, app_name)

    target_html = const.get_html(app_name)
    file_path = f"templates/{target_html}"
    return FileResponse(file_path)


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

    if json_data:
        result = json_data.get(param)
        return result
    else:
        curr_func_nm = sys._getframe().f_code.co_name
        except_http_error(curr_func_nm, request.url._url)


# GEMINI
@app.post("/gemini/api")
async def gemini_api(request: Request):
    curr_func_nm = sys._getframe().f_code.co_name

    json_data = await request.json()
    mode = json_data["mode"]
    contents = json_data["prompt"]
    message = const.SYM_BLANK

    try:
        if mode == const.STR_IMG:
            message = func_gemini.get_gemini_image(contents=contents)
            func.print_info_msg(line.MSG_TYPE_IMG, func_line.URL_GEMINI_IMG)
        else:
            response = func_gemini.get_gemini_response(curr_func_nm, contents)
            message = const.SYM_NEW_LINE.join(response)

    except Exception as e:
        message = msg_const.MSG_ERR_PROC_FAILED
        func.print_error_msg(SCRIPT_NAME, curr_func_nm, message, e)

    result = {const.STR_MESSAGE: message}
    return result


# ランキング情報更新
@app.post("/number/ranking")
async def number_ranking(request: Request):
    json_data = await request.json()
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
            func_line.send_msg_for_admin(msg)

    except Exception as e:
        curr_func_nm = sys._getframe().f_code.co_name
        message = msg_const.MSG_ERR_PROC_FAILED
        func.print_error_msg(SCRIPT_NAME, curr_func_nm, message, e)

    result = {const.STR_MESSAGE: message}
    return result


# 掲示板データ・ステータス更新
@app.get("/board/update/{seq}")
async def board_update(seq: str):
    try:
        board_dao.update_board_status(seq)
    except Exception as e:
        curr_func_nm = sys._getframe().f_code.co_name
        func.print_error_msg(SCRIPT_NAME, curr_func_nm, seq, e)

    return RedirectResponse(url=const.PATH_APP_BOARD)


@app.get("/kakao", response_class=HTMLResponse)
async def kakao_root(request: Request):
    """開始ページ"""

    token = func_kakao.get_token(request)
    content = func_kakao.get_login_content(token)
    return content


@app.get("/kakao/login")
async def kakao_login(request: Request):
    """ログイン"""

    auth_url = func_kakao.URL_KAKAO_AUTH
    return RedirectResponse(auth_url)
    # request.session[func_kakao.STR_KAKAO_API_TOKEN] = func_kakao.get_access_token()
    # return RedirectResponse("/kakao")


@app.get("/kakao/logout")
async def kakao_logout(request: Request):
    """ログアウト"""

    token = func_kakao.get_token(request)
    if not token:
        return RedirectResponse(url="/kakao")

    content = func_kakao.get_logout_content(token)

    # セッションクリア
    request.session.clear()

    return HTMLResponse(content=content)


@app.get("/kakao/oauth", response_class=HTMLResponse)
async def kakao_oauth(request: Request, code: str):
    """
    認証コードで、アクセストークン発行
    （初回のみ実施、リフレッシュトークンの確認にも使用）

    引数:
        code(str): 認証コード
    """

    token, content = func_kakao.get_auth_content(code)
    if token:
        func.print_info_msg(const.STR_KAKAO, msg_const.MSG_INFO_AUTH_SUCCESS)
        request.session[func_kakao.STR_KAKAO_API_TOKEN] = token

    return content


@app.get("/kakao/{app_name}")
async def kakao_apps(request: Request, app_name: str):
    if app_name in kakao.LIST_APP_KOREA:
        if app_name == const.APP_TODAY:
            app_name == const.APP_TODAY_KOREA
            url = f"/app/{app_name}"

        else:
            if app_name == const.TYPE_LIST:
                app_name = const.APP_KAKAO_DESIGN

            url = f"/apps/{app_name}"
        return RedirectResponse(url)

    else:
        curr_func_nm = sys._getframe().f_code.co_name
        except_http_error(curr_func_nm, request.url._url)


# テンプレートファイル取得
@app.get("/templates/{file_name}")
async def templates_file(file_name: str):
    file_ext = func.get_path_split(file_name, extension_flg=const.FLG_ON)
    file_path = f"templates/{file_ext}/{file_name}"
    return FileResponse(file_path)


# ファイル取得（例：/img/today、/font/meiryo、/log/error）
@app.get("/{div}/{file_name}")
async def file_response(request: Request, div: str, file_name: str):
    except_flg = const.FLG_OFF

    file_div = const.STR_OUTPUT
    if (
        div == const.STR_IMG and ("0" in file_name or "1" in file_name)
    ) or div == const.STR_FONT:
        file_div = const.STR_INPUT

    file_type = const.FILE_TYPE_JPEG
    if div in [const.STR_IMG, const.STR_FONT, const.STR_LOG]:
        if div == const.STR_FONT:
            file_type = const.FILE_TYPE_TTC
        elif div == const.STR_LOG:
            file_type = const.FILE_TYPE_LOG

        file_name_list = func.get_file_name_list(file_type, file_div)
        if file_name not in file_name_list:
            except_flg = const.FLG_ON
    else:
        except_flg = const.FLG_ON

    if not except_flg:
        file_path = func.get_file_path(file_name, file_type, file_div)
        return FileResponse(file_path)
    else:
        curr_func_nm = sys._getframe().f_code.co_name
        except_http_error(curr_func_nm, request.url._url)


# サーバーのヘルスチェック
@app.get("/check")
def health_check():
    appl.no_sleep()
    info_msg = msg_const.MSG_INFO_SERVER_KEEP_WORKING
    func.print_info_msg(SCRIPT_NAME, info_msg)
    result = {const.STR_MESSAGE: info_msg}
    return result


# テストAPI
@app.get("/test")
def api_test():
    message = test.main()
    if not message:
        message = "Server is on test."
    return {const.STR_MESSAGE: message}


# HTTPエラー
def except_http_error(func_name: str, url: str):
    http_status_code = const.STATUS_CODE_NOT_FOUND
    status_msg = msg_const.HTTP_STATUS_MESSAGES.get(http_status_code)
    err_msg = f"{status_msg} {url}"
    func.print_error_msg(SCRIPT_NAME, func_name, err_msg)
    raise HTTPException(status_code=http_status_code, detail=err_msg)


# メイン関数（サーバースレッド起動）
if __name__ == const.MAIN_FUNCTION:
    start_thread()
    # health_check()
