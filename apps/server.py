"""
サーバー処理

FastAPIによるWebサーバー。
認証・セッション管理・各種APIエンドポイントを提供
"""

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
import apps.dashboard as dashboard
import apps.kakao as kakao
import apps.line as line
import apps.test as test
import apps.utils.auth_dao as auth_dao
import apps.utils.board_dao as board_dao
import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_gemini as func_gemini
import apps.utils.function_kakao as func_kakao
import apps.utils.function_line as func_line
import apps.utils.html_constants as html_const
import apps.utils.message_constants as msg_const
import apps.utils.mongo_constants as mongo_const
import apps.utils.rank_dao as rank_dao
import apps.utils.user_dao as user_dao

# スクリプト名
SCRIPT_NAME = func.get_app_name(__file__)

# FastAPIインスタンス生成とセッションミドルウェア追加
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="secret_key")
templates = Jinja2Templates(directory="templates")

# OAuth2トークン認証設定
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def run_server():
    """
    サーバー起動
    """
    func.print_start(SCRIPT_NAME, msg_const.MSG_INFO_SERVER_START)
    host, port = func.get_host_port()
    config = Config(app, host=host, port=port)
    server = Server(config)
    server.run()


def start_thread():
    """
    サーバーを別スレッドで起動
    """
    t = Thread(target=run_server)
    t.start()
    # t.join()


def token_required(func_):
    """
    トークン認証
    """

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


@app.get("/protected-resource")
async def protected_resource(request: Request, token: str):
    """
    トークン検証
    """
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


@app.post("/token")
async def issue_token(request: Request):
    """
    トークン発行
    """
    access_token = "token_" + func.get_now(const.DATE_TODAY)
    # expiration = func.get_calc_date(const.MAX_TOKEN_EXPIRATION_MINUTES, const.DATE_MIN)
    token_data = {
        const.STR_TOKEN: access_token,
        const.STR_TYPE: "bearer",
    }
    request.session[const.STR_TOKEN] = token_data
    return token_data


@app.get(const.PATH_ROOT)
async def root(request: Request):
    """
    ルートページ（ログイン状態でリダイレクト）
    """
    user = request.session.get(const.STR_USER)
    if user:
        response = RedirectResponse(url=const.PATH_APP_NEWS, status_code=303)
    else:
        context = {const.STR_REQUEST: request, const.STR_PATH: const.PATH_LOGIN}
        response = templates.TemplateResponse(const.HTML_INDEX, context)
    return response


@app.post(const.PATH_LOGIN)
async def login(request: Request, userId: str = Form(...), userPw: str = Form(...)):
    """
    ログイン処理
    """
    user_info = user_dao.get_user_info(userId)
    chk_msg = user_dao.check_login(userId, userPw, user_info)
    if chk_msg:
        request.session.clear()
        context = {
            const.STR_REQUEST: request,
            const.STR_PATH: const.PATH_LOGIN,
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


@app.get(const.PATH_LOGOUT)
async def logout(request: Request):
    """
    ログアウト処理
    """
    user_name = request.session[const.STR_USER][mongo_const.FI_USER_NAME]
    func.print_info_msg(user_name, msg_const.MSG_INFO_LOGOUT)
    request.session.clear()
    context = {
        const.STR_REQUEST: request,
        const.STR_PATH: const.PATH_LOGIN,
        const.STR_MESSAGE: msg_const.MSG_INFO_LOGOUT_EN,
    }
    return templates.TemplateResponse(const.HTML_INDEX, context)


@app.get("/app/{app_name}")
async def app_exec(request: Request, app_name: str):
    """
    アプリケーション実行
    """
    try:
        if app_name == const.APP_USER:
            target_html = const.HTML_USER_INFO
            context = appl.get_context_for_user(request, app_name)
        else:
            target_html = const.HTML_RESULT
            context = appl.get_context_data(request, app_name)

            if not context:
                except_http_error(app_name, request.url._url)

        dashboard.write_dashboard_log(request, app_name)

    except Exception as e:
        target_html = const.HTML_INDEX

        curr_func_nm = sys._getframe().f_code.co_name
        context = get_context_except(curr_func_nm, request, e)

    return templates.TemplateResponse(target_html, context)


@app.get("/apps/{app_name}")
async def apps(request: Request, app_name: str):
    """
    アプリケーション実行
    """
    try:
        target_html = const.HTML_RESULT_2
        context = appl.get_context_data_2(request, app_name)

        if not context:
            except_http_error(app_name, request.url._url)

        dashboard.write_dashboard_log(request, app_name)

    except Exception as e:
        target_html = const.HTML_INDEX

        curr_func_nm = sys._getframe().f_code.co_name
        context = get_context_except(curr_func_nm, request, e)

    return templates.TemplateResponse(target_html, context)


@app.get("/json/{app_name}")
# @token_required
async def app_json(request: Request, app_name: str):
    """
    JSONデータ取得
        （例）
        /json/today?token=token
    """
    if not app_name in const.LIST_APP_SERVER_ALL:
        except_http_error(app_name, request.url._url)

    result = func.get_json_data(app_name, const.STR_OUTPUT)
    return result


@app.get("/api/{api_name}/{param}")
async def app_api(request: Request):
    """
    APIデータ取得
        （例）
        /api/zipCode/1000000
        /api/zipCode/1000000
    """
    api_name = request.path_params["api_name"]
    param = request.path_params["param"]

    json_data = func.get_json_data(api_name)
    if json_data:
        result = json_data.get(param)
        return result
    else:
        except_http_error(api_name, request.url._url)


@app.post("/gemini/api")
async def gemini_api(request: Request):
    """
    GEMINI
    """
    message = const.SYM_BLANK
    curr_func_nm = sys._getframe().f_code.co_name

    try:
        json_data = await request.json()
        mode = json_data["mode"]
        contents = json_data["prompt"]

        if mode == const.STR_IMG:
            message = func_gemini.get_gemini_image(contents=contents)
            func.print_debug_msg(const.MSG_TYPE_IMG, func_line.URL_GEMINI_IMG)
        else:
            response = func_gemini.get_gemini_response(curr_func_nm, contents)
            message = const.SYM_NEW_LINE.join(response)

    except Exception as e:
        message = msg_const.MSG_ERR_SERVER_PROC_FAILED
        func.print_error_msg(SCRIPT_NAME, curr_func_nm, message, e)

    result = {const.STR_MESSAGE: message}
    return result


@app.post("/user/update")
async def user_update(request: Request, userId: str = Form(...)):
    """
    ユーザー情報更新（フォーム）
    """
    curr_func_nm = sys._getframe().f_code.co_name

    try:
        form_data = await request.form()
        dict_data = dict(form_data)
        user_dao.update_user_info_on_form(dict_data)
        user_info = user_dao.get_user_info(userId)
        request.session[const.STR_USER] = user_info
        target_html = const.HTML_USER_INFO
        context = appl.get_context_for_user(request, const.APP_USER)

    except Exception as e:
        target_html = const.HTML_INDEX
        context = get_context_except(curr_func_nm, request, e)

    return templates.TemplateResponse(target_html, context)


@app.post("/ranking/{app_name}")
async def update_ranking(request: Request, app_name: str):
    """
    ランキング情報更新
    """
    json_data = await request.json()
    if app_name == const.APP_NUMBER:
        rank_dao.update_rank_info_of_api(json_data)
    else:
        rank_dao.update_ranking_of_api(app_name, json_data)
    result = {const.STR_MESSAGE: msg_const.MSG_INFO_PROC_COMPLETED}
    return result


@app.post("/board/{div}")
async def board_update(request: Request, div: str):
    """
    掲示板データ登録・更新
    """
    curr_func_nm = sys._getframe().f_code.co_name

    try:
        json_data = await request.json()
        if div == const.STR_ADD:
            insert_data_list = board_dao.insert_board_data_of_api(json_data)

            # LINE通知
            line.sub(curr_func_nm, insert_data_list)

        else:
            board_dao.update_board_status(json_data)

        message = msg_const.MSG_INFO_PROC_COMPLETED

    except Exception as e:
        message = msg_const.MSG_ERR_SERVER_PROC_FAILED
        func.print_error_msg(SCRIPT_NAME, curr_func_nm, message, e)

    result = {const.STR_MESSAGE: message}
    return result


@app.get("/kakao", response_class=HTMLResponse)
async def kakao_root(request: Request):
    """
    Kakao 認証開始
    """
    token = func_kakao.get_token(request.session)
    content = func_kakao.get_auth_content(token)
    return content


@app.get("/kakao/main")
async def kakao_main(request: Request):
    """
    Kakao メイン
    """
    token = func_kakao.get_token(request.session)
    if token:
        response = RedirectResponse(url=const.PATH_KAKAO_TODAY, status_code=303)
    else:
        context = {const.STR_REQUEST: request, const.STR_PATH: const.PATH_KAKAO_LOGIN}
        response = templates.TemplateResponse(const.HTML_INDEX, context)

    return response


@app.post("/kakao/login")
async def kakao_login(request: Request, userId: str = Form(...)):
    """
    Kakao ログイン
    """
    user_pw = auth_dao.get_auth_token(userId, key=mongo_const.FI_USER_PW)
    if user_pw:
        user_name = userId.split(const.SYM_AT)[0]
        user_info = {
            mongo_const.FI_USER_DIV: const.STR_KAKAO,
            mongo_const.FI_USER_NAME: user_name,
            mongo_const.FI_MENU: const.SYM_BLANK,
        }
        request.session[const.STR_USER] = user_info

        # request.session[mongo_const.FI_USER_PW] = user_pw
        response = RedirectResponse(url=const.PATH_KAKAO_TODAY, status_code=303)
    else:
        request.session.clear()
        context = {
            const.STR_REQUEST: request,
            const.STR_PATH: const.PATH_KAKAO_LOGIN,
            const.STR_MESSAGE: msg_const.MSG_ERR_INCORRECT_ACCESS_EN,
        }
        response = templates.TemplateResponse(const.HTML_INDEX, context)

    return response


@app.get("/kakao/logout", response_class=HTMLResponse)
async def kakao_logout(request: Request):
    """
    Kakao ログアウト
    """
    token = func_kakao.get_token(request.session)
    content = func_kakao.get_logout_content(token)

    # セッションクリア
    request.session.clear()

    return content


@app.get("/kakao/auth", response_class=RedirectResponse)
async def kakao_auth():
    """
    Kakao 認証
    """
    auth_url = func_kakao.URL_KAKAO_AUTH
    return auth_url


@app.get("/kakao/oauth", response_class=HTMLResponse)
async def kakao_oauth(request: Request, code: str):
    """
    認証コードで、アクセストークン発行
    （初回のみ実施、リフレッシュトークンの確認にも使用）

    引数:
        code (str): 認証コード
    """

    token, content = func_kakao.get_auth_result_content(code)
    if token:
        func.print_info_msg(const.STR_KAKAO, msg_const.MSG_INFO_AUTH_SUCCESS)
        request.session[func_kakao.STR_KAKAO_API_TOKEN] = token

    return content


# [MEMO] 認証時のみ使用
@app.get("/kakao/send-test", response_class=HTMLResponse)
async def kakao_send_test(request: Request):
    """
    Kakao メッセージ送信テスト
    """
    token = func_kakao.get_token(request.session)
    content = func_kakao.get_test_message_content(token)
    return content


@app.get("/kakao/{app_name}")
async def kakao_apps(request: Request, app_name: str):
    """
    アプリケーション実行
    """
    if app_name in const.LIST_APP_KOREA:
        url = "/app/"
        if app_name == const.APP_TODAY:
            app_name = const.APP_TODAY_KOREA
        else:
            url = url.replace("app", "apps")
            if app_name == const.TYPE_LIST:
                app_name = const.APP_KAKAO_DESIGN

        url += app_name
        return RedirectResponse(url)

    else:
        except_http_error(app_name, request.url._url)


@app.get("/templates/{file_name}", response_class=FileResponse)
async def templates_file(file_name: str):
    """
    テンプレートファイル取得
    """
    file_ext = func.get_path_split(file_name, extension_flg=const.FLG_ON)
    file_path = f"templates/{file_ext}/{file_name}"
    return file_path


@app.get("/{div}/{file_name}", response_class=FileResponse)
async def file_response(request: Request, div: str, file_name: str):
    """
    ファイル取得
        （例）
        /img/today
        /font/meiryo
        /log/error
    """
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
        return file_path
    else:
        except_http_error(file_name, request.url._url)


@app.get("/check")
def health_check():
    """
    サーバーのヘルスチェック
    """
    appl.no_sleep()
    info_msg = msg_const.MSG_INFO_SERVER_KEEP_WORKING
    func.print_info_msg(SCRIPT_NAME, info_msg)
    result = {const.STR_MESSAGE: info_msg}
    return result


@app.get("/test")
def api_test():
    """
    テストAPI
    """
    message = test.main()
    if not message:
        message = "Server is on test."
    return {const.STR_MESSAGE: message}


def get_context_except(curr_func_nm: str, request, e):
    """
    [例外] データ取得
    """
    message = msg_const.MSG_ERR_SERVER_PROC_FAILED
    func.print_error_msg(SCRIPT_NAME, curr_func_nm, message, e)

    context = {
        const.STR_REQUEST: request,
        const.STR_PATH: const.PATH_LOGIN,
        const.STR_MESSAGE: message,
    }
    return context


def except_http_error(div: str, url: str):
    """
    [例外] HTTPエラー
    """
    http_status_code = const.STATUS_CODE_NOT_FOUND
    status_msg = msg_const.HTTP_STATUS_MESSAGES.get(http_status_code)
    err_msg = f"{status_msg} {url}"
    func.print_info_msg(div, err_msg)
    raise HTTPException(status_code=http_status_code, detail=err_msg)


if __name__ == const.MAIN_FUNCTION:
    start_thread()
    # health_check()
