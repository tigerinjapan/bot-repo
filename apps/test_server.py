"""
サーバー処理

FastAPIによるWebサーバー。
認証・セッション管理・各種APIエンドポイントを提供
"""

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
from uvicorn import Config, Server

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_api as func_api
import apps.utils.function_kakao as func_kakao
import apps.utils.message_constants as msg_const

# スクリプト名
SCRIPT_NAME = func.get_app_name(__file__)

# FastAPI
app = FastAPI(title="カカオトーク - メッセージ送信テスト")
app.add_middleware(SessionMiddleware, secret_key="secret_key")


def run_server():
    """
    サーバー起動
    """
    func.print_start(SCRIPT_NAME, msg_const.MSG_INFO_SERVER_START)
    host, port = func.get_host_port()
    config = Config(app, host=host, port=port)
    server = Server(config)
    server.run()


@app.get("/kakao", response_class=HTMLResponse)
async def root(request: Request):
    """
    開始ページ
    """
    token = func_kakao.get_token(request.session)
    content = func_kakao.get_auth_content(token)
    return content


@app.get("/kakao/login")
async def login():
    """
    ログイン
    """
    auth_url = func_kakao.URL_KAKAO_AUTH
    return RedirectResponse(auth_url)


@app.get("/kakao/logout")
async def logout(request: Request):
    """
    ログアウト
    """
    token = func_kakao.get_token(request.session)
    if not token:
        return RedirectResponse(url="/kakao")

    content = func_kakao.get_logout_content(token)

    # セッションクリア
    request.session.clear()

    return HTMLResponse(content=content)


@app.get("/kakao/oauth?code={code}", response_class=HTMLResponse)
async def oauth(request: Request, code: str):
    """
    認証コードで、アクセストークン発行
     (初回のみ実施、リフレッシュトークンの確認にも使用)

    引数:
        code (str): 認証コード
    """

    token, content = func_kakao.get_auth_result_content(code)
    if token:
        request.session[func_kakao.STR_KAKAO_API_TOKEN] = token

    return content


@app.get("/kakao/unlink")
async def unlink(request: Request):
    """
    アカウント連携解除
    """
    token = func_kakao.get_token(request.session)
    if not token:
        return RedirectResponse(url="/kakao")

    content = func_kakao.get_unlink_content(token)

    # セッションクリア
    request.session.clear()

    return HTMLResponse(content=content)


@app.get("/kakao/send-test", response_class=HTMLResponse)
async def send_test(request: Request):
    """
    メッセージ送信テスト
    """
    token = func_kakao.get_token(request.session)
    content = func_kakao.get_test_message_content(token)
    return HTMLResponse(content=content)


@app.get("/kakao/test")
async def kakao_test():
    """
    テスト
    """
    url = func_kakao.URL_KAKAO_USER_ME
    access_token = func_kakao.get_access_token()
    headers = {"Authorization": access_token}
    result = func_api.get_response_result(url, headers=headers)
    if result:
        try:
            id = result["id"]
            last_login_date = result["connected_at"]
            func.print_debug_msg(SCRIPT_NAME, f"{id} {last_login_date}")

        except KeyError as ke:
            msg = msg_const.MSG_ERR_DATA_NOT_EXIST
            func.print_error_msg(SCRIPT_NAME, url, msg, ke)

    return result


# メイン関数 (サーバースレッド起動)
if __name__ == const.MAIN_FUNCTION:
    run_server()
