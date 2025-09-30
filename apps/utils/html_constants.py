# 説明: HTMLの定数

HTML_KAKAO_LOGIN = """ <a href="/kakao/login" class="button">카카오 로그인</a> """
HTML_KAKAO_LOGOUT = """ <a href="/kakao/logout" class="button logout">로그아웃</a> """
HTML_KAKAO_SEND_TEST = (
    """ <a href="/kakao/send-test" class="button">테스트 메시지 보내기</a> """
)
HTML_KAKAO_GO_HOME = """ <a href="/kakao" class="button">홈으로 이동</a> """
HTML_KAKAO_UNLINK = (
    """ <a href="/kakao/unlink" class="button unlink">앱 연결 해제</a> """
)
HTML_KAKAO_TODAY = """ <a href="/kakao/today" class="button">오늘의 생활정보</a> """

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
