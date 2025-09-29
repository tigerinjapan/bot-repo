# 説明: サーバー処理
# FastAPIによるWebサーバー。認証・セッション管理・各種APIエンドポイントを提供

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse
import httpx
from starlette.middleware.sessions import SessionMiddleware
from uvicorn import Config, Server

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_kakao as func_kakao
import apps.utils.html_constants as html_const
import apps.utils.message_constants as msg_const

# スクリプト名
SCRIPT_NAME = func.get_app_name(__file__)

# REST API キー
REST_API_KEY = func_kakao.KAKAO_API_KEY

# リダイレクトURI
URL_SERVER = func.get_server_url()
REDIRECT_URI = f"{URL_SERVER}/kakao/oauth"

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

    title = "카카오 알림 테스트"

    token = get_token(request)
    if token:
        body = f"""
            <h1>{title}</h1>
            <p>로그인이 완료되었습니다. 메시지 보내기를 할 수 있습니다.</p>
            <div>
                {html_const.HTML_KAKAO_SEND_TEST}
                {html_const.HTML_KAKAO_LOGOUT}
            </div>
        """

    else:
        body = f"""
            <h1>{title}</h1>
            <p>카카오 로그인이 필요합니다.</p>
            {html_const.HTML_KAKAO_LOGIN}
        """

    return get_html_context(title, body)


@app.get("/kakao/login")
async def login():
    """ログイン"""

    auth_url = "https://kauth.kakao.com/oauth/authorize"
    auth_url += f"?client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}"
    auth_url += "&response_type=code&scope=talk_message&prompt=login"
    return RedirectResponse(auth_url)


@app.get("/kakao/logout")
async def logout(request: Request):
    """ログアウト"""

    token = get_token(request)
    if not token:
        return RedirectResponse(url="/")

    body = const.SYM_BLANK

    logout_url = "https://kapi.kakao.com/v1/user/logout"
    headers = {"Authorization": token}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(logout_url, headers=headers)
            result = response.json()

            # セッションクリア
            request.session.clear()

            # 結果表示
            result_json = func.get_dumps_json(result)
            body = f"""
                <h1>로그아웃 <span class="success">완료</span></h1>
                <p>카카오 계정에서 로그아웃되었습니다.</p>
                <pre>{result_json}</pre>
            """

    except Exception as e:
        # セッションクリア
        request.session.clear()

        body = f"""
            <h1>로그아웃 <span class="warning">부분 완료</span></h1>
            <p>로컬 세션에서 로그아웃되었지만, 카카오 서버 로그아웃 중 오류가 발생했습니다:</p>
            <pre>{str(e)}</pre>
        """

    title = "로그아웃 결과"
    body += html_const.HTML_KAKAO_GO_HOME
    content = get_html_context(title, body)
    return HTMLResponse(content=content)


@app.get("/kakao/unlink")
async def unlink(request: Request):
    """アカウント連携解除"""

    token = get_token(request)
    if not token:
        return RedirectResponse(url="/")

    unlink_url = "https://kapi.kakao.com/v1/user/unlink"
    headers = {"Authorization": token}

    body = const.SYM_BLANK

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(unlink_url, headers=headers)
            result = response.json()

            # セッションクリア
            request.session.clear()

            result_json = func.get_dumps_json(result)
            body = f"""
                <h1>앱 연결 <span class="success">해제 완료</span></h1>
                <p>카카오 계정과 앱의 연결이 해제되었습니다.</p>
                <pre>{result_json}</pre>
            """

    except Exception as e:
        # セッションクリア
        request.session.clear()

        body = f"""
            <h1>앱 연결 해제 <span class="error">실패</span></h1>
            <p>연결 해제 중 오류가 발생했습니다:</p>
            <pre>{str(e)}</pre>
        """

    title = "연결 해제 결과"
    body += html_const.HTML_KAKAO_GO_HOME
    content = get_html_context(title, body)
    return HTMLResponse(content=content)


@app.get("/kakao/oauth?code={code}", response_class=HTMLResponse)
async def oauth(request: Request, code: str):
    """
    認証コードで、アクセストークン発行
    （初回のみ実施、リフレッシュトークンの確認にも使用）

    引数:
        code(str): 認証コード
    """

    token_url = func_kakao.URL_TOKEN
    data = {
        "grant_type": "authorization_code",
        "client_id": REST_API_KEY,
        "redirect_uri": REDIRECT_URI,
        "code": code,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data)
        token_info = response.json()

        if "access_token" in token_info:
            token_type = token_info["token_type"]
            access_token = token_info["access_token"]
            token = f"{token_type} {access_token}"
            request.session[const.STR_TOKEN] = token

            title = "인증 성공"
            body = f"""
                <h1>카카오 인증 <span class="success">성공!</span></h1>
                <p>이제 메시지를 보낼 수 있습니다.</p>
                <div class="button-group">
                    {html_const.HTML_KAKAO_SEND_TEST}
                    {html_const.HTML_KAKAO_LOGOUT}
                </div>
            """
        else:
            error_details = func.get_dumps_json(token_info)
            title = "인증 실패"
            body = f"""
                <h1>카카오 인증 <span class="error">실패</span></h1>
                <p>인증 과정에서 오류가 발생했습니다:</p>
                <pre>{error_details}</pre>
                <p><a href="/kakao" class="button">다시 시도하기</a></p>
            """

        content = get_html_context(title, body)
        return content


@app.get("/kakao/send-test", response_class=HTMLResponse)
async def send_test():
    """メッセージ送信テスト"""

    send_url = func_kakao.URL_API_SEND

    token = func_kakao.get_access_token()
    if not token:
        return RedirectResponse(url="/kakao")

    headers = {"Authorization": token}

    template_object = func_kakao.get_template_object()
    data = {"template_object": template_object}

    async with httpx.AsyncClient() as client:
        response = await client.post(send_url, headers=headers, data=data)
        result = response.json()

        success = "result_code" in result and result["result_code"] == 0

        title = "메시지 전송 결과"

        result_json = func.get_dumps_json(result)
        body = f"""
            <h1>메시지 전송 <span class="{'success' if success else 'error'}">
                {('성공!' if success else '실패')}
            </span></h1>
            <p>결과:</p>
            <pre>{result_json}</pre>
            <div class="button-group">
                {html_const.HTML_KAKAO_SEND_TEST}
                {html_const.HTML_KAKAO_GO_HOME}
                {html_const.HTML_KAKAO_LOGOUT}
                {html_const.HTML_KAKAO_UNLINK}
            </div>
            <p style="margin-top: 20px; font-size: 0.9em; color: #666;">
                * '앱 연결 해제'는 카카오 계정과 이 앱의 연결을 완전히 끊습니다. 
                다시 사용하려면 처음부터 인증 과정을 거쳐야 합니다.
            </p>
        """

        content = get_html_context(title, body)
        return HTMLResponse(content=content)


# トークン取得
def get_token(request: Request):
    token = const.SYM_BLANK
    request_session = request.session
    if request_session:
        token = request_session[const.STR_TOKEN]
    return token


# HTMLテキスト取得
def get_html_context(title: str, body: str) -> str:
    html_context = f"""
<!DOCTYPE html>
<html lang="ja">

<head>
    <title>{title}</title>
    <meta http-equiv="Content-Type" content="text/html" charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="{func_kakao.URL_ICO}"></script>
    {html_const.HTML_KAKAO_STYLE}
</head>
<body>
    {body}
</body>

</html>
    """

    return html_context


# メイン関数（サーバースレッド起動）
if __name__ == const.MAIN_FUNCTION:
    run_server()
