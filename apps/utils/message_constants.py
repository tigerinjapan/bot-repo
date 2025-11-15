"""
メッセージ一覧
"""

# インフォメーションメッセージ
MSG_INFO_PROC_START = "処理を開始します。"
MSG_INFO_PROC_END = "処理を終了します。"
MSG_INFO_PROC_COMPLETED = "処理を完了しました。"
MSG_INFO_LOGIN = "ログインしました。"
MSG_INFO_LOGOUT = "ログアウトしました。"
MSG_INFO_SERVER_START = "サーバーを起動します。"
MSG_INFO_SERVER_RESTART = "サーバーを再起動します。"
MSG_INFO_SERVER_KEEP_WORKING = "サーバーは正常に稼働しています。"
MSG_INFO_SERVER_SLEEP = "サーバーがスリープ状態です。"
MSG_INFO_SESSION_EXPIRED = "セッション期限が切れました。再ログインしてください。"
MSG_INFO_AUTH_SUCCESS = "認証が完了しました。"
MSG_INFO_TOKEN_ISSUED_SUCCESS = "トークンの発行が完了しました。"
MSG_INFO_TOKEN_UPDATE_SUCCESS = "トークンの更新が完了しました。"
MSG_INFO_DATA_NOT_EXIST = "更新データが存在しません。"

# エラーメッセージ
MSG_ERR_USER_NOT_EXIST = "[ログイン] IDを再確認してください。"
MSG_ERR_PASSWORD_INCORRECT = "[ログイン] パスワードを再確認してください。"
MSG_ERR_CONNECTION_FAILED = "[接続] 接続情報を確認してください。"
MSG_ERR_TOKEN_NOT_EXIST = "[認証] トークンが存在しません。"
MSG_ERR_TOKEN_EXPIRED = "[認証] トークンの有効期限が切れました。"
MSG_ERR_INVALID_TOKEN = "[認証] トークンが無効です。"
MSG_ERR_INVALID_API_KEY = "[認証] APIキーが無効です。"
MSG_ERR_API_REQUEST_CONNECT = "[API] 対象URLへ接続できません。"
MSG_ERR_API_RESPONSE_NONE = "[API] レスポンス結果がありません。"
MSG_ERR_API_SUPPORT_ENDED = "[API] サポートが終了しました。"
MSG_ERR_ENV_VAR_NOT_EXIST = "[環境変数] 環境変数が存在しません。"
MSG_ERR_SERVER_NOT_WORKING = "[サーバー] サーバーが正常に稼働していません。"
MSG_ERR_SERVER_PROC_FAILED = "[サーバー] 処理に失敗しました。"
MSG_ERR_MSG_SEND = "[メッセージ] メッセージ送信中に、エラーが発生しました。"
MSG_ERR_DB_PROC_FAILED = "[DB] 処理に失敗しました。"
MSG_ERR_DATA_NOT_EXIST = "[データ] 対象データが存在しません。"
MSG_ERR_FILE_NOT_EXIST = "[ファイル] 対象パスにファイルが存在しません。"
MSG_ERR_NO_SUCH_ELEMENT = "[要素] 対象の画面要素が存在しません。"

# [英語] メッセージ
MSG_INFO_LOGIN_EN = "Login successful."
MSG_INFO_LOGOUT_EN = "Logout successful."
MSG_ERR_INCORRECT_ACCESS_EN = "Incorrect user id or password."
MSG_ERR_USER_AGENT_NOT_FOUND_EN = "User-Agent header not found."

# HTTPステータスメッセージ
HTTP_STATUS_MESSAGES = {
    # 成功 (2xx)
    200: "リクエストは正常に処理されました。",
    201: "新しいリソースが作成されました。",
    204: "リクエストは正常終了しましたが、コンテンツはありません。",
    # リダイレクト (3xx)
    301: "このページは、新しいURLへ移動しました。",
    302: "このページは、一時的に別の場所へ移動しています。",
    304: "コンテンツは更新されていません。",
    # クライアントエラー (4xx)
    400: "リクエストが正しくありません。入力内容をご確認ください。",
    401: "このページへのアクセスには、認証が必要です。",
    403: "権限がなく、アクセスが拒否されました。",
    404: "お探しのページは見つかりませんでした。",
    408: "リクエストがタイムアウトしました。",
    429: "短時間に多くのリクエストが送信されました。",
    # サーバーエラー (5xx)
    500: "サーバーで予期せぬエラーが発生しました。",
    502: "無効なレスポンスがサーバーから返されました。",
    503: "サービスが一時的に利用できません。",
    504: "ゲートウェイがタイムアウトしました。",
}
