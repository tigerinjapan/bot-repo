"""
HTML定数
"""

HTML_KAKAO_BUTTON = """ <a href="/kakao{}" class="button{}">{}</a> """

HTML_KAKAO_AUTH = f""" {HTML_KAKAO_BUTTON.format("/auth", "", "카카오 인증")} """
HTML_KAKAO_LOGIN = f""" {HTML_KAKAO_BUTTON.format("/login", "","서버 로그인")} """
HTML_KAKAO_LOGOUT = (
    f""" {HTML_KAKAO_BUTTON.format("/logout", " logout","서버 로그아웃")} """
)
HTML_KAKAO_AUTH_SUCCESS = (
    f""" {HTML_KAKAO_BUTTON.format("/logout", " logout","카카오 인증완료")} """
)
HTML_KAKAO_SEND_TEST = (
    f""" {HTML_KAKAO_BUTTON.format("/send-test", "", "테스트 메시지 보내기")} """
)

HTML_KAKAO_GO_HOME = f""" {HTML_KAKAO_BUTTON.format("", "", "홈으로 이동")} """
HTML_KAKAO_GO_MAIN = (
    f""" {HTML_KAKAO_BUTTON.format("/main", "", "메인 페이지로 이동")} """
)

HTML_KAKAO_UNLINK = (
    f""" {HTML_KAKAO_BUTTON.format("/unlink", " unlink", "앱 연결 해제")} """
)
HTML_KAKAO_LIST = """ <a href="/kakao/list" target="_blank" rel="noopener noreferrer" class="button">링크 리스트</a> """

HTML_KAKAO_STYLE = """ <style>
body {
	font-family: Arial, sans-serif;
	margin: 40px;
	line-height: 1.6;
}

.success {
	color: green;
}

.warning {
	color: orange;
}

.error {
	color: red;
}

pre {
	background: #f4f4f4;
	padding: 10px;
	overflow: auto;
}

h1 {
	color: #222;
}

.button {
	display: inline-block;
	background-color: #FEE500;
	color: #000;
	padding: 10px 20px;
	text-decoration: none;
	border-radius: 4px;
	font-weight: bold;
	margin-right: 10px;
}

.button-group {
	margin-top: 20px;
}

.logout {
	background-color: #f1f1f1;
	color: #666;
}

.unlink {
    background-color: #ff9999;
    color: #990000;
}

</style>
"""


# HTMLテキスト取得
def get_html_context(title: str, body: str, style: str = HTML_KAKAO_STYLE) -> str:
    html_context = f"""
<!DOCTYPE html>
<html lang="ja">

<head>
    <title>{title}</title>
    <meta http-equiv="Content-Type" content="text/html" charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href="/templates/favicon.ico" type="image/x-icon">
    {style}
</head>
<body>
    {body}
</body>

</html>
    """

    return html_context
