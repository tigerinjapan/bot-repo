# 説明: LINEメッセージAPI

import sys

import apps.utils.auth_dao as auth_dao
import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_api as func_api
import apps.utils.function_line as func_line
import apps.utils.html_constants as html_const
import apps.utils.message_constants as msg_const

# スクリプト名
SCRIPT_NAME = func.get_app_name(__file__)

# アプリケーション名
app_name = const.STR_KAKAO

# Kakao API情報
STR_KAKAO_API_TOKEN = f"KakaoAPI{const.STR_TOKEN}"
KAKAO_API_KEY = func.get_env_val("KAKAO_API_KEY")
KAKAO_API_SECRET = func.get_env_val("KAKAO_API_SECRET")

# URL
URL_KAKAO_OAUTH = "https://kauth.kakao.com/oauth"
URL_TOKEN = f"{URL_KAKAO_OAUTH}/token"

URL_KAKAO_API = "https://kapi.kakao.com"
URL_KAKAO_API_LOGOUT = f"{URL_KAKAO_API}/v1/user/logout"
URL_KAKAO_API_UNLINK = f"{URL_KAKAO_API}/v1/user/unlink"
URL_KAKAO_API_SEND_ME = f"{URL_KAKAO_API}/v2/api/talk/memo/default/send"
URL_KAKAO_API_USER_ME = f"{URL_KAKAO_API}/v2/user/me"

# TODO: チャネル登録必要のため、保留
URL_KAKAO_API_FRIENDS = f"{URL_KAKAO_API}/v1/api/talk/friends"
URL_KAKAO_API_SEND_FRIENDS = f"{URL_KAKAO_API}/message/default/send"

URL_ICO = f"{func_line.URL_KOYEB_APP}/templates/favicon.ico"
URL_TODAY_KOREA_IMG = f"{func_line.URL_KOYEB_IMG}/{const.APP_TODAY_KOREA}"

# リダイレクトURI
# URL_SERVER = func.get_server_url()
# REDIRECT_URI = f"{URL_SERVER}/kakao/oauth"
REDIRECT_URI = f"{func_line.URL_KOYEB_APP}/kakao/oauth"

auth_url = (
    f"{URL_KAKAO_OAUTH}/authorize?client_id={KAKAO_API_KEY}&redirect_uri={REDIRECT_URI}"
)
auth_url += "&response_type=code&scope=talk_message&prompt=login"
URL_KAKAO_AUTH = auth_url

# 認証タイプ
GRANT_TYPE_AUTH_CODE = "認証コード"
GRANT_TYPE_REFRESH_TOKEN = "リフレッシュトークン"
ISSUE_TYPE_ACCESS_TOKEN = "アクセストークン"
ISSUE_TYPE_REFRESH_TOKEN = GRANT_TYPE_REFRESH_TOKEN

# Kakaoメッセージタイプ
OBJECT_TYPE_FEED = "feed"
OBJECT_TYPE_TEXT = "text"
OBJECT_TYPE_LIST = "list"  # TODO: 実装要

# 結果コード
RESULT_CODE_OK = 0
RESULT_CODE_NG = 1


# アクセストークン取得（トークン発行、更新）
def get_access_token(code: str = const.SYM_BLANK) -> str:
    curr_func_nm = sys._getframe().f_code.co_name

    token = const.SYM_BLANK
    token_url = URL_TOKEN

    if code:
        data = {
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URI,
            "code": code,
        }

    else:
        auth_token = auth_dao.get_auth_token(app_name)
        refresh_token = func.get_decoding_masking_data(auth_token)
        if not refresh_token:
            msg = f"{app_name}: {msg_const.MSG_ERR_TOKEN_NOT_EXIST}"
            func.print_error_msg(SCRIPT_NAME, curr_func_nm, msg)
            return const.SYM_BLANK

        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }

    client_data = {"client_id": KAKAO_API_KEY, "client_secret": KAKAO_API_SECRET}
    data.update(client_data)

    result = func_api.get_response_result(
        token_url,
        request_type=const.REQUEST_TYPE_POST,
        data=data,
        header_json_flg=const.FLG_OFF,
    )

    if not result:
        return const.SYM_BLANK

    # トークン・タイプ
    token_type = result["token_type"]

    # アクセストークン（有効期限：6時間）
    access_token = result["access_token"]

    grant_type = GRANT_TYPE_REFRESH_TOKEN
    issue_type = ISSUE_TYPE_ACCESS_TOKEN

    if token_type and access_token:
        token = f"{token_type} {access_token}"

    if code:
        grant_type = GRANT_TYPE_AUTH_CODE
        issue_type = ISSUE_TYPE_REFRESH_TOKEN
        # 認証コード：毎回アクセスし、アクセストークン取得が必要であるため、
        # リフレッシュトークン方式でアクセストークン発行（有効期限：1か月）
        refresh_token = result["refresh_token"]
        auth_token = func.get_masking_data(refresh_token)
        auth_dao.update_auth_token(app_name, auth_token)
        func.print_info_msg(app_name, msg_const.MSG_INFO_TOKEN_UPDATE_SUCCESS)

    msg_div = f"{grant_type}で{issue_type}の発行、"
    if token:
        msg = msg_const.MSG_INFO_TOKEN_ISSUED_SUCCESS
        func.print_info_msg(msg_div, msg)
    else:
        msg = msg_const.MSG_ERR_TOKEN_NOT_EXIST
        func.print_error_msg(msg_div, msg)

    return token


# ユーザー情報取得
def get_user_me(access_token: str = const.SYM_BLANK) -> list[str]:
    curr_func_nm = sys._getframe().f_code.co_name

    if not access_token:
        access_token = get_access_token()

    url = URL_KAKAO_API_USER_ME
    headers = {"Authorization": access_token}
    result = func_api.get_response_result(url, headers=headers)
    if result:
        try:
            account_info = result["kakao_account"]
            uuid = result["for_partner"]["uuids"]

        except KeyError as ke:
            msg = msg_const.MSG_ERR_DATA_NOT_EXIST
            func.print_error_msg(SCRIPT_NAME, curr_func_nm, msg, ke)

    return result


# 友達リスト検索 # TODO: チャネル登録必要のため、保留
def get_receiver_uuids(access_token: str = const.SYM_BLANK) -> list[str]:
    receiver_uuids = []

    if not access_token:
        access_token = get_access_token()

    url = URL_KAKAO_API_FRIENDS
    headers = {"Authorization": access_token}
    result = func_api.get_response_result(url, headers=headers)
    if result:
        elements = result["elements"]
        receiver_uuids = [element["uuid"] for element in elements]
        # total_count = result["total_count"]

    return receiver_uuids


# メッセージ送信
def send_kakao_msg(
    access_token: str,
    object_type: str = OBJECT_TYPE_FEED,
    title: str = const.SYM_BLANK,
    message: str = const.SYM_BLANK,
    link: str = const.SYM_BLANK,
    link_mo: str = const.SYM_BLANK,
    receiver_uuids=[],
):
    url = URL_KAKAO_API_SEND_ME
    headers = {"Authorization": access_token}

    data = {}
    if object_type == const.STR_LOGIN:
        url = URL_KAKAO_AUTH
    elif object_type == const.STR_LOGOUT:
        url = URL_KAKAO_API_LOGOUT
    else:
        template_object = get_template_object(
            object_type, title, message, link, link_mo
        )
        data = {"template_object": template_object}
        if receiver_uuids:
            url = URL_KAKAO_API_SEND_FRIENDS
            data.update({"receiver_uuids": receiver_uuids})

    result = func_api.get_response_result(
        url,
        request_type=const.REQUEST_TYPE_POST,
        headers=headers,
        data=data,
        header_json_flg=const.FLG_OFF,
    )
    return result


# テンプレート取得
def get_template_object(
    object_type: str = OBJECT_TYPE_FEED,
    title: str = const.SYM_BLANK,
    message: str = const.SYM_BLANK,
    link: str = const.SYM_BLANK,
    link_mo: str = const.SYM_BLANK,
    img_url: str = URL_TODAY_KOREA_IMG,
):
    if object_type == OBJECT_TYPE_FEED:
        template_object = {
            "object_type": object_type,
            "content": {
                "title": title,
                "description": message,
                "image_url": img_url,
                "image_width": const.KAKAO_IMG_SIZE_W,
                "image_height": const.KAKAO_IMG_SIZE_H,
                "link": {"web_url": link, "mobile_web_url": link_mo},
            },
        }

    elif object_type == OBJECT_TYPE_TEXT:
        template_object = {
            "object_type": object_type,
            "text": message,
            "link": {
                "web_url": link,
                "mobile_web_url": link_mo,
            },
            "button_title": title,
        }

    else:
        current_time = func.get_now().strftime(const.DATE_FORMAT_YYYYMMDD_HHMM)
        template_object = {
            "object_type": OBJECT_TYPE_TEXT,
            "text": f"📢 메시지 보내기 테스트 📢\n\n테스트 중입니다.\n전송 시간: {current_time}",
            "link": {
                "web_url": const.URL_NAVER,
                "mobile_web_url": const.URL_NAVER_MO,
            },
            "button_title": "자세히 보기",
        }
        func.print_info_msg(object_type, template_object[const.INPUT_TYPE_TEXT])

    template_object = func.get_dumps_json(template_object)
    return template_object


# トークン取得
def get_token(request):
    token = const.SYM_BLANK
    request_session = request.session
    if request_session:
        token = request_session[STR_KAKAO_API_TOKEN]
    return token


# ログインHTML取得
def get_login_content(token: str):
    title = "카카오 인증"

    if token:
        body = f"""
            <h1>{title}</h1>
            <p>인증이 완료되었습니다.</p>
            <p>아래의 링크 리스트를 즐겨찾기에 등록해서 웹서비스를 이용해주세요.</p>
            <p>매일 오전 9시에 카카오톡 메시지로 「오늘의 뉴스」를 전송할 예정입니다.</p>
            <div class="button-group">
                {html_const.HTML_KAKAO_LIST}<br>
                {html_const.HTML_KAKAO_LOGOUT}
            </div>
        """

    else:
        body = f"""
            <h1>{title}</h1>
            <p>카카오 로그인이 필요합니다.</p>
            <p>카카오 로그인 후에 메시지수신동의를 체크해주세요.</p>
            {html_const.HTML_KAKAO_LOGIN}
        """

    content = get_html_context(title, body)
    return content


# ログアウトHTML取得
def get_logout_content(token: str) -> str:
    body = const.SYM_BLANK

    try:
        # ログアウト
        result = send_kakao_msg(token, const.STR_LOGOUT)

        # 結果表示
        body = f"""
            <h1>로그아웃 <span class="success">완료</span></h1>
            <p>카카오 계정에서 로그아웃되었습니다.</p>
            <pre>{result}</pre><br>
        """

    except Exception as e:
        # 結果表示
        body = f"""
            <h1>로그아웃 <span class="warning">부분 완료</span></h1>
            <p>로컬 세션에서 로그아웃되었지만, 카카오 서버 로그아웃 중 오류가 발생했습니다:</p>
            <pre>{str(e)}</pre><br>
        """

    title = "로그아웃 결과"
    body += html_const.HTML_KAKAO_GO_HOME
    content = get_html_context(title, body)
    return content


# アカウント認証
def get_auth_content(code: str) -> tuple[str, str]:
    token = const.SYM_BLANK
    if code:
        token = get_access_token(code)

    if token:
        title = "인증 성공"
        body = f"""
            <h1>카카오 인증 <span class="success">성공!</span></h1>
            <p>인증이 성공하였습니다.</p><br>
            <p>아래의 링크 리스트를 즐겨찾기에 등록해서 웹서비스를 이용해주세요.</p><br>
            <p>매일 오전 9시에 카카오톡 메시지로 「오늘의 뉴스」를 전송할 예정입니다.</p><br>
            <div class="button-group">
                {html_const.HTML_KAKAO_LIST}<br>
                {html_const.HTML_KAKAO_LOGOUT}
            </div>
        """
    else:
        title = "인증 실패"
        body = f"""
            <h1>카카오 인증 <span class="error">실패</span></h1>
            <p>인증 과정에서 오류가 발생했습니다.</p>
            <p><a href="/kakao" class="button">다시 시도하기</a></p>
        """

    content = get_html_context(title, body)
    return token, content


# アカウント連携解除
def get_unlink_content(token: str) -> str:
    try:
        # 連携解除
        result = send_kakao_msg(token, const.STR_UNLINK)

        # 結果表示
        body = f"""
            <h1>앱 연결 <span class="success">해제 완료</span></h1>
            <p>카카오 계정과 앱의 연결이 해제되었습니다.</p><br>
            <pre>{result}</pre><br>
        """

    except Exception as e:
        body = f"""
            <h1>앱 연결 해제 <span class="error">실패</span></h1>
            <p>연결 해제 중 오류가 발생했습니다.</p><br>
            <pre>{str(e)}</pre><br><br>
        """

    title = "연결 해제 결과"
    body += html_const.HTML_KAKAO_GO_HOME
    content = get_html_context(title, body)
    return content


# テストメッセージのHTML取得
def get_test_message_content(token: str = const.SYM_BLANK) -> str:
    if not token:
        token = get_access_token()

    object_type = const.STR_TEST
    result = send_kakao_msg(token, object_type)
    result_code = RESULT_CODE_OK
    result_data = const.SYM_BLANK
    if result:
        result_code = result["result_code"]
        result_data = func.get_dumps_json(result)
    success_flg = const.FLG_ON if result_code == RESULT_CODE_OK else const.FLG_OFF

    title = "메시지 전송 결과"

    body = f"""
        <h1>메시지 전송 <span class="{'success' if success_flg else 'error'}">
            {('성공!' if success_flg else '실패')}
        </span></h1>
        <p>결과</p><br>
        <pre>{result_data}</pre><br>
        <p>메시지 전송이 성공이지만 수신되지 않은 경우,<br>로그아웃 하고나서 다시 테스트 해 주세요.</p><br>
        <div class="button-group">
            {html_const.HTML_KAKAO_LOGOUT}<br>
            {html_const.HTML_KAKAO_LOGOUT}<br>
            {html_const.HTML_KAKAO_GO_HOME}
        </div>
    """

    content = get_html_context(title, body)
    return content


# HTMLテキスト取得
def get_html_context(title: str, body: str) -> str:
    html_context = f"""
<!DOCTYPE html>
<html lang="ja">

<head>
    <title>{title}</title>
    <meta http-equiv="Content-Type" content="text/html" charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="{URL_ICO}"></script>
    {html_const.HTML_KAKAO_STYLE}
</head>
<body>
    {body}
</body>

</html>
    """

    return html_context


if __name__ == const.MAIN_FUNCTION:
    # get_access_token()
    get_test_message_content()
