# 説明: LINEメッセージAPI

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_api as func_api
import apps.utils.html_constants as html_const
import apps.utils.function_line as func_line

# スクリプト名
SCRIPT_NAME = func.get_app_name(__file__)

# Kakao API情報
STR_KAKAO_API_TOKEN = f"KakaoAPI{const.STR_TOKEN}"
KAKAO_API_KEY = func.get_env_val("KAKAO_API_KEY")
KAKAO_API_SECRET = func.get_env_val("KAKAO_API_SECRET")
# KAKAO_API_REFRESH_TOKEN = func.get_env_val("KAKAO_API_REFRESH_TOKEN")
KAKAO_API_REFRESH_TOKEN = (
    "'usBRFwjCwOT_jVrihMldHxcE5a0cBX2nAAAAAgoNCB4AAAGZjjIl-in2EFsnJsRZ'"
)

# URL
URL_OAUTH = "https://kauth.kakao.com/oauth"
URL_TOKEN = f"{URL_OAUTH}/token"
URL_API_SEND = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
URL_API_LOGOUT = "https://kapi.kakao.com/v1/user/logout"
URL_ICO = f"{func_line.URL_KOYEB_APP}/templates/favicon.ico"
URL_TODAY_KOREA_IMG = f"{func_line.URL_KOYEB_IMG}/{const.APP_TODAY_KOREA}"

# リダイレクトURI
URL_SERVER = func.get_server_url()
REDIRECT_URI = f"{URL_SERVER}/kakao/oauth"

auth_url = (
    f"{URL_OAUTH}/authorize?client_id={KAKAO_API_KEY}&redirect_uri={REDIRECT_URI}"
)
auth_url += "&response_type=code&scope=talk_message&prompt=login"
URL_AUTH = auth_url

# Kakaoメッセージタイプ
OBJECT_TYPE_FEED = "feed"
OBJECT_TYPE_TEXT = "text"
OBJECT_TYPE_LIST = "list"  # TODO: 実装要

# 認証コード：毎回アクセスし、取得が必要であるため、
# リフレッシュトークン方式でアクセストークン発行（有効期限：1か月）
auth_code = ""


# アクセストークン取得（トークン発行、更新）
def get_access_token(refresh_flg: bool = const.FLG_ON) -> str:
    token_url = URL_TOKEN
    client_id = KAKAO_API_KEY

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    if refresh_flg:
        data = {
            "grant_type": "refresh_token",
            "client_id": client_id,
            "refresh_token": KAKAO_API_REFRESH_TOKEN,
            "client_secret": KAKAO_API_SECRET,
        }

    else:
        data = {
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URI,
            "code": auth_code,
            "client_id": client_id,
            "client_secret": KAKAO_API_SECRET,
        }

    result = func_api.get_response_result(
        token_url,
        request_type=const.REQUEST_TYPE_POST,
        headers=headers,
        data=data,
        header_json_flg=const.FLG_OFF,
    )

    if not result:
        return const.SYM_BLANK

    # トークン・タイプ
    token_type = result["token_type"]

    # アクセストークン（有効期限：6時間）
    access_token = result["access_token"]

    token = f"{token_type} {access_token}"

    # 有効期限（秒）
    # expires_in = result["expires_in"]

    # 有効期限（分）
    # expires_min = int(expires_in / 60)
    # func.print_info_msg(const.STR_TOKEN_JA, f"{const.STR_EXPIRE_JA}: {expires_min}分")

    return token


# メッセージ送信
def send_message(
    access_token: str,
    object_type: str = OBJECT_TYPE_FEED,
    title: str = const.SYM_BLANK,
    message: str = const.SYM_BLANK,
    link: str = const.SYM_BLANK,
    link_mo: str = const.SYM_BLANK,
    template_object=const.SYM_BLANK,
):
    url = URL_API_SEND
    headers = {"Authorization": access_token}

    data = {}
    if object_type == const.STR_LOGIN:
        url = URL_AUTH
    elif object_type == const.STR_LOGOUT:
        url = URL_API_LOGOUT
    else:
        template_object = get_template_object(
            object_type, title, message, link, link_mo
        )
        data = {"template_object": template_object}

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
            "text": f"📢 메시지 보내기 테스트 📢\n\n테스트 중입니다.\n발송 시간: {current_time}",
            "link": {
                "web_url": const.URL_NAVER,
                "mobile_web_url": const.URL_NAVER_MO,
            },
            "button_title": "자세히 보기",
        }

    template_object = func.get_dumps_json(template_object)
    return template_object


# トークン取得
def get_token(request):
    token = const.SYM_BLANK
    request_session = request.session
    if request_session:
        token = request_session[STR_KAKAO_API_TOKEN]
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
    get_access_token()
