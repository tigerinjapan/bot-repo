# 説明: サーバー処理
# FastAPIによるWebサーバー。認証・セッション管理・各種APIエンドポイントを提供

from fastapi import FastAPI, Query, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
from uvicorn import Config, Server

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_kakao as func_kakao
import apps.utils.message_constants as msg_const

# スクリプト名
SCRIPT_NAME = func.get_app_name(__file__)

# FastAPI
app = FastAPI(title="カカオトーク - メッセージ送信テスト")
app.add_middleware(SessionMiddleware, secret_key="secret_key")


# サーバー起動
def run_server():
    func.print_start(SCRIPT_NAME, msg_const.MSG_INFO_SERVER_START)
    host, port = func.get_host_port()
    config = Config(app, host=host, port=port)
    server = Server(config)
    server.run()


@app.get("/kakao", response_class=HTMLResponse)
async def root(request: Request):
    """開始ページ"""

    token = func_kakao.get_token(request.session)
    content = func_kakao.get_login_content(token)
    return content


@app.get("/kakao/login")
async def login():
    """ログイン"""

    auth_url = func_kakao.URL_KAKAO_AUTH
    return RedirectResponse(auth_url)


@app.get("/kakao/logout")
async def logout(request: Request):
    """ログアウト"""

    token = func_kakao.get_token(request.session)
    if not token:
        return RedirectResponse(url="/kakao")

    content = func_kakao.get_logout_content(token)

    # セッションクリア
    request.session.clear()

    return HTMLResponse(content=content)


# @app.get("/kakao/oauth", response_class=HTMLResponse)
# async def oauth(request: Request, code: str = Query(...)):
@app.get("/kakao/oauth?code={code}", response_class=HTMLResponse)
async def oauth(request: Request, code: str):
    """
    認証コードで、アクセストークン発行
    （初回のみ実施、リフレッシュトークンの確認にも使用）

    引数:
        code(str): 認証コード
    """

    token, content = func_kakao.get_auth_result_content(code)
    if token:
        request.session[func_kakao.STR_KAKAO_API_TOKEN] = token

    return content


@app.get("/kakao/unlink")
async def unlink(request: Request):
    """アカウント連携解除"""

    token = func_kakao.get_token(request.session)
    if not token:
        return RedirectResponse(url="/kakao")

    content = func_kakao.get_unlink_content(token)

    # セッションクリア
    request.session.clear()

    return HTMLResponse(content=content)


@app.get("/kakao/send-test", response_class=HTMLResponse)
async def send_test(request: Request):
    """メッセージ送信テスト"""

    token = func_kakao.get_token(request.session)
    if not token:
        return RedirectResponse(url="/kakao")

    content = func_kakao.get_test_message_content(token)
    return HTMLResponse(content=content)


# メイン関数（サーバースレッド起動）
if __name__ == const.MAIN_FUNCTION:
    run_server()
