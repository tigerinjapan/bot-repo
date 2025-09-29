# 説明: LINEメッセージAPI

import sys

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_api as func_api
import apps.utils.function_line as func_line

# スクリプト名
SCRIPT_NAME = func.get_app_name(__file__)

# URL
URL_TOKEN = "https://kauth.kakao.com/oauth/token"
URL_API_SEND = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
URI_REDIRECT = "http://localhost:5000/"
URL_ICO = f"{func_line.URL_KOYEB_APP}/templates/favicon.ico"
URL_TODAY_KOREA_IMG = f"{func_line.URL_KOYEB_IMG}/{const.APP_TODAY_KOREA}"

# Kakaoメッセージタイプ
OBJECT_TYPE_FEED = "feed"
OBJECT_TYPE_TEXT = "text"
OBJECT_TYPE_LIST = "list"  # TODO: 実装要

# Kakao API情報
STR_KAKAO_API = "Kakao API"
KAKAO_API_KEY = func.get_env_val("KAKAO_API_KEY")
KAKAO_API_SECRET = func.get_env_val("KAKAO_API_SECRET")

# 認証コード：毎回アクセスし、取得が必要であるため、
# リフレッシュトークン方式でアクセストークン発行（有効期限：1か月）
# auth_code_url = f"https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={KAKAO_API_KEY}&redirect_uri=http://localhost:5000/kakao/oauth"
auth_code = ""


# アクセストークン取得
def get_access_token(refresh_flg: bool = const.FLG_ON) -> str:
    token_url = URL_TOKEN
    client_id = KAKAO_API_KEY

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    if refresh_flg:
        data = {
            "grant_type": "refresh_token",
            "client_id": client_id,
            "refresh_token": "'usBRFwjCwOT_jVrihMldHxcE5a0cBX2nAAAAAgoNCB4AAAGZjjIl-in2EFsnJsRZ'",
            "client_secret": KAKAO_API_SECRET,
        }

    else:
        data = {
            "grant_type": "authorization_code",
            "redirect_uri": URI_REDIRECT,
            "code": auth_code,
            "client_id": client_id,
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
    temp_div: str = OBJECT_TYPE_FEED,
    title: str = const.SYM_BLANK,
    message: str = const.SYM_BLANK,
    link: str = const.SYM_BLANK,
    link_mo: str = const.SYM_BLANK,
):
    url = URL_API_SEND
    headers = {"Authorization": access_token}

    template_object = get_template_object(temp_div, title, message, link, link_mo)
    data = {"template_object": template_object}

    result = func_api.get_response_result(
        url,
        request_type=const.REQUEST_TYPE_POST,
        headers=headers,
        data=data,
        header_json_flg=const.FLG_OFF,
    )
    if result:
        curr_func_nm = sys._getframe().f_code.co_name
        func.print_error_msg(
            SCRIPT_NAME, curr_func_nm, STR_KAKAO_API, result["details"]
        )


# テンプレート取得
def get_template_object(
    temp_div: str = OBJECT_TYPE_FEED,
    title: str = const.SYM_BLANK,
    message: str = const.SYM_BLANK,
    link: str = const.SYM_BLANK,
    link_mo: str = const.SYM_BLANK,
    img_url: str = URL_TODAY_KOREA_IMG,
):
    if temp_div == OBJECT_TYPE_FEED:
        template_object = {
            "object_type": temp_div,
            "content": {
                "title": title,
                "description": message,
                "image_url": img_url,
                "image_width": 480,
                "image_height": 480,
                "link": {"web_url": link, "mobile_web_url": link_mo},
            },
        }

    elif temp_div == OBJECT_TYPE_TEXT:
        template_object = {
            "object_type": temp_div,
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


if __name__ == const.MAIN_FUNCTION:
    get_access_token()
