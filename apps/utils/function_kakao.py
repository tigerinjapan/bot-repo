"""
KakaoメッセージAPI
"""

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
URL_KAKAO_OAUTH = f"{const.URL_KAKAO_AUTH}/oauth"
URL_KAKAO_TOKEN = f"{URL_KAKAO_OAUTH}/token"

URL_KAKAO_API_LOGOUT = f"{const.URL_KAKAO_API}/v1/user/logout"
URL_KAKAO_API_UNLINK = f"{const.URL_KAKAO_API}/v1/user/unlink"
URL_KAKAO_API_SEND_ME = f"{const.URL_KAKAO_API}/v2/api/talk/memo/default/send"
URL_KAKAO_API_USER_ME = f"{const.URL_KAKAO_API}/v2/user/me"

# TODO: [pending] チャネル登録必要
URL_KAKAO_API_FRIENDS = f"{const.URL_KAKAO_API}/v1/api/talk/friends"
URL_KAKAO_API_SEND_FRIENDS = f"{const.URL_KAKAO_API}/message/default/send"

URL_TODAY_KOREA_IMG = f"{func_line.URL_KOYEB_IMG}/{const.APP_TODAY_KOREA}"

# リダイレクトURI
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

# ボタン
BTN_TITLE_FLIGHT = "✈ 최저가 항공권 정보 ✈"
BTN_TITLE_MORE = "더 보기"

# 結果コード
RESULT_CODE_OK = 0
RESULT_CODE_NG = 1


def get_access_token(code: str = const.SYM_BLANK) -> str:
    """
    アクセストークン取得（トークン発行、更新）
    """
    curr_func_nm = sys._getframe().f_code.co_name

    token = const.SYM_BLANK

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
        URL_KAKAO_TOKEN,
        request_type=const.REQUEST_TYPE_POST,
        data=data,
        header_json_flg=const.FLG_OFF,
    )

    if not result:
        return const.SYM_BLANK

    # トークン・タイプ
    token_type = result["token_type"]

    # アクセストークン
    access_token = result["access_token"]

    # 有効期限（有効期限：6時間）
    expires_in = result["expires_in"]
    expires_min = int(expires_in // 60)
    func.print_debug_msg(const.STR_TOKEN, f"{const.STR_EXPIRATION}: {expires_min} min")

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
        func.print_debug_msg(app_name, msg_const.MSG_INFO_TOKEN_UPDATE_SUCCESS)

    msg_div = f"{grant_type}で{issue_type}の発行、"
    if token:
        msg = msg_const.MSG_INFO_TOKEN_ISSUED_SUCCESS
        func.print_debug_msg(msg_div, msg)
    else:
        msg = msg_const.MSG_ERR_TOKEN_NOT_EXIST
        func.print_error_msg(msg_div, msg)

    return token


def get_user_me(access_token: str = const.SYM_BLANK) -> list[str]:
    """
    ユーザー情報取得
    """
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


def get_receiver_uuids(access_token: str = const.SYM_BLANK) -> list[str]:
    """
    友達リスト検索

    [pending] チャネル登録必要
    """
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


def send_kakao_msg(
    access_token: str,
    object_type: str = const.OBJECT_TYPE_TEXT,
    title: str = const.SYM_BLANK,
    message: str = const.SYM_BLANK,
    link: str = const.SYM_BLANK,
    link_mo: str = const.SYM_BLANK,
    receiver_uuids=[],
):
    """
    メッセージ送信
    """
    url = URL_KAKAO_API_SEND_ME
    template_object = get_template_object(object_type, title, message, link, link_mo)
    data = {"template_object": template_object}

    if receiver_uuids:
        url = URL_KAKAO_API_SEND_FRIENDS
        data.update({"receiver_uuids": receiver_uuids})

    result = func_api.api_post_data(url, data, access_token)
    return result


def get_template_object(
    object_type: str,
    title: str,
    message: str,
    link: str = const.SYM_BLANK,
    link_mo: str = const.SYM_BLANK,
    img_url: str = URL_TODAY_KOREA_IMG,
):
    """
    テンプレート取得
    """
    if not link and not link_mo:
        link = const.URL_NAVER
        link_mo = const.URL_NAVER_MO

    if title == const.STR_TEST:
        contents = get_template_contents(object_type, title, message)
    else:
        if object_type == const.OBJECT_TYPE_FEED:
            func.print_debug_msg(const.STR_IMG, img_url)
            content = {
                "image_url": img_url,
                "title": title,
                "description": message,
                "link": {"web_url": link, "mobile_web_url": link_mo},
            }

            contents = {
                "content": content,
            }

        elif object_type == const.OBJECT_TYPE_LIST:
            param_list = message

            content_list = []
            for param in param_list:
                content = {
                    "title": param[0],
                    "link": {"web_url": param[1], "mobile_web_url": param[1]},
                }
                content_list.append(content)

            contents = {
                "header_title": title,
                "header_link": {"web_url": link, "mobile_web_url": link_mo},
                "contents": content_list,
                "button_title": BTN_TITLE_MORE,
            }

        else:
            contents = {
                "text": message,
                "link": {
                    "web_url": link,
                    "mobile_web_url": link_mo,
                },
                "button_title": title,
            }

    template_object = {"object_type": object_type}
    template_object.update(contents)
    template_json = func.get_dumps_json(template_object)
    return template_json


def get_template_contents(
    object_type: str = const.OBJECT_TYPE_TEXT, title: str = const.SYM_BLANK
):
    """
    テンプレートコンテンツ取得
    """
    link = const.URL_NAVER
    link_mo = const.URL_NAVER_MO
    img_url: str = URL_TODAY_KOREA_IMG

    content_list = []
    param_list = [
        [
            "자전거 라이더를 위한 공간\n자전거 라이더를 위한 공간",
            "매거진뉴스1매거진뉴스2매거진뉴스3매거진뉴스4매거진뉴스5매거진",
            img_url,
            link,
            link_mo,
            "main",
            "main",
        ],
        [
            "비쥬얼이 끝내주는 오레오\n비쥬얼이 끝내주는 오레오",
            "매거진뉴스1매거진뉴스2매거진뉴스3매거진뉴스4매거진뉴스5매거진",
            img_url,
            link,
            link_mo,
            "main",
            "main",
        ],
        [
            "이국적 감성 가득한 분위기\n이국적 감성 가득한 분위기",
            "매거진뉴스1매거진뉴스2매거진뉴스3매거진뉴스4매거진뉴스5매거진",
            img_url,
            link,
            link_mo,
            "main",
            "main",
        ],
    ]

    for param in param_list:
        content = {
            "title": param[0],
            "description": param[1],
            "image_url": param[2],
            "image_width": 640,
            "image_height": 640,
            "link": {
                "web_url": param[3],
                "mobile_web_url": param[4],
                "android_execution_params": param[5],
                "ios_execution_params": param[6],
            },
        }
        content_list.append(content)

    button_list = [
        {
            "title": "웹으로 이동",
            "link": {
                "web_url": link,
                "mobile_web_url": link_mo,
            },
        },
        {
            "title": "앱으로 이동",
            "link": {
                "android_execution_params": "main",
                "ios_execution_params": "main",
            },
        },
    ]

    if object_type == const.OBJECT_TYPE_FEED:
        content = content_list[0]
        item_list = [
            {"item": "CakeTe", "item_op": "1,000,000원"},
            {"item": "ケーキテスト", "item_op": "2,000,000원"},
            {"item": "케이크테스트", "item_op": "3,000,000원"},
            {"item": "케이크테스트", "item_op": "4,000,000원"},
            {"item": "케이크테스트", "item_op": "5,000,000원"},
        ]
        contents = {
            "item_content": {
                "profile_image_url": img_url,
                "profile_text": "profile_text",
                "title_image_url": img_url,
                "title_image_text": "title_image_text",
                "title_image_category": "title_image_category",
                "items": item_list,
                "sum": "Total",
                "sum_op": "15,000,000원",
            },
            "content": content,
            "social": {
                "like_count": 1,
                "comment_count": 2,
                "shared_count": 3,
                "view_count": 4,
                "subscriber_count": 5,
            },
            "buttons": button_list,
        }

    elif object_type == const.OBJECT_TYPE_LIST:
        contents = {
            "header_title": title,
            "header_link": {
                "web_url": link,
                "mobile_web_url": link_mo,
                "android_execution_params": "main",
                "ios_execution_params": "main",
            },
            "contents": content_list,
            "buttons": button_list,
        }

    else:
        if not message:
            current_time = func.get_now(
                const.DATE_TODAY, const.DATE_FORMAT_YYYYMMDD_HHMM
            )
            message = f"📢 메시지 보내기 테스트 📢\n\n테스트 중입니다.\n전송 시간: {current_time}"

        contents = {
            "text": message,
            "link": {
                "web_url": link,
                "mobile_web_url": link_mo,
            },
            "button_title": title,
        }

    return contents


def get_token(session):
    """
    トークン取得
    """
    token = const.SYM_BLANK
    if session:
        try:
            token = session[STR_KAKAO_API_TOKEN]
        except:
            token = const.SYM_BLANK
    return token


def get_auth_content(token: str):
    """
    認証
    """
    title = "카카오 인증"

    if token:
        body = f"""
            <h1>{title}</h1>
            <p>인증이 완료되었습니다.</p>
            <p>아래 버튼으로 메시지 보내기를 테스트 할 수 있습니다.</p>
            <div class="button-group">
                {html_const.HTML_KAKAO_SEND_TEST}<br>
                {html_const.HTML_KAKAO_AUTH_SUCCESS}<br>
                {html_const.HTML_KAKAO_GO_MAIN}
            </div>
        """

    else:
        body = f"""
            <h1>{title}</h1>
            <p>카카오 인증이 필요합니다.</p>
            <p>카카오 인증 시에 메시지 수신동의를 체크해주세요.</p>
            <div class="button-group">
                {html_const.HTML_KAKAO_AUTH}
            </div>
        """

    content = html_const.get_html_context(title, body)
    return content


def get_logout_content(token: str) -> str:
    """
    ログアウト
    """
    body = result = const.SYM_BLANK

    try:
        # if token:
        #     # ログアウト：トークン満了されるため、処理しない
        # result = func_api.api_post_data(URL_KAKAO_API_LOGOUT, access_token=token)
        account_str = "카카오 계정 "

        # 結果表示
        body = f"""
            <h1>{account_str}로그아웃 <span class="success">완료</span></h1>
            <p>정상적으로 {account_str}로그아웃되었습니다.</p>
            <pre>{result}</pre><br>
        """

    except Exception as e:
        # 結果表示
        body = f"""
            <h1>로그아웃 <span class="warning">부분 완료</span></h1>
            <p>{account_str}로그아웃은 처리되었지만, 로그아웃 중 서버 오류가 발생했습니다:</p>
            <pre>{str(e)}</pre><br>
        """

    title = f"{account_str}로그아웃 결과"
    body += html_const.HTML_KAKAO_GO_MAIN
    content = html_const.get_html_context(title, body)
    return content


def get_auth_result_content(code: str) -> tuple[str, str]:
    """
    アカウント認証結果
    """
    token = const.SYM_BLANK
    if code:
        token = get_access_token(code)

    if token:
        title = "인증 성공"
        body = f"""
            <h1>카카오 인증 <span class="success">성공!</span></h1>
            <p>인증이 성공하였습니다.</p>
            <p>아래 버튼으로 메시지 보내기를 테스트 할 수 있습니다.</p>
            <div class="button-group">
                {html_const.HTML_KAKAO_SEND_TEST}<br>
                {html_const.HTML_KAKAO_AUTH_SUCCESS}
            </div>
        """
    else:
        title = "인증 실패"
        body = f"""
            <h1>카카오 인증 <span class="error">실패</span></h1>
            <p>인증 과정에서 오류가 발생했습니다.</p>
            <p>다시 인증을 실시 해주세요.</p>
            <div class="button-group">
                {html_const.HTML_KAKAO_GO_HOME}
            </div>
        """

    content = html_const.get_html_context(title, body)
    return token, content


def get_unlink_content(token: str) -> str:
    """
    アカウント連携解除
    """
    try:
        # 連携解除
        result = func_api.api_post_data(URL_KAKAO_API_UNLINK, access_token=token)

        # 結果表示
        body = f"""
            <h1>앱 연결 <span class="success">해제 완료</span></h1>
            <p>카카오 계정과 앱의 연결이 해제되었습니다.</p>
            <pre>{result}</pre><br>
        """

    except Exception as e:
        body = f"""
            <h1>앱 연결 해제 <span class="error">실패</span></h1>
            <p>연결 해제 중 오류가 발생했습니다.</p>
            <pre>{str(e)}</pre><br>
        """

    title = "연결 해제 결과"
    body += html_const.HTML_KAKAO_GO_HOME
    content = html_const.get_html_context(title, body)
    return content


def get_test_message_content(
    token: str = const.SYM_BLANK,
    title: str = const.STR_TEST,
    message: str = const.SYM_BLANK,
) -> str:
    """
    テストメッセージのHTML取得
    """
    if not token:
        token = get_access_token()

    result = send_kakao_msg(token, title, message)
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
        <p>결과</p>
        <pre>{result_data}</pre><br>
        <p>메시지 전송이 성공이지만 수신되지 않은 경우,<br>로그아웃 후에 다시 테스트 해 주세요.</p>
        <div class="button-group">
            {html_const.HTML_KAKAO_LOGOUT}
        </div>
    """

    content = html_const.get_html_context(title, body)
    return content


if __name__ == const.MAIN_FUNCTION:
    # token = get_access_token()
    # object_type = const.OBJECT_TYPE_FEED
    # send_kakao_msg(token, object_type)
    get_test_message_content()
