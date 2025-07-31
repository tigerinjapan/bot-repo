# 説明: LINEメッセージ

import apps.lcc as lcc
import apps.mlb as mlb
import apps.news as news
import apps.study as study
import apps.today as today
import apps.tv as tv
import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_api as func_api
import apps.utils.function_gemini as func_gemini
import apps.utils.function_line as func_line

# アプリケーション
app_name = func.get_app_name(__file__)

# URL
URL_LINE_API = "https://api.line.me"
URL_KOYEB_APP = "https://" + func.get_env_val("URL_KOYEB")
URL_TODAY_IMG = f"{URL_KOYEB_APP}/{const.STR_IMG}/{const.APP_TODAY}"

# 改行
NEW_LINE = const.SYM_NEW_LINE

# メッセージタイプ
MSG_TYPE_TXT = "text"
MSG_TYPE_IMG = "image"
MSG_TYPE_TMP = "template"

# ファイル区分
FILE_DIV_AI_NEWS = "ai_news"

# タイトル
DIV_MARK = "*----*----*----*----*----*"
DIV_MARK_TXT = "*-- {} --*"
DIV_MARK_IMG = "=== {} ==="

# 曜日
WEEKLY_DIV_FRI = "Fri"


def main(
    auto_flg: bool = const.FLG_ON,
    data_flg: bool = const.FLG_ON,
    proc_flg: bool = const.FLG_ON,
):
    """
    メインの処理を実行

    引数:
        auto_flg (bool): 自動処理を有効にするフラグ
        data_flg (bool): データ処理を有効にするフラグ。False: テンプレート送信
        proc_flg (bool): 処理実行を有効にするフラグ
    """

    func.print_start(app_name)

    if func_line.LINE_CHANNEL_ID:
        # チャネル・アクセストークン取得
        token = func_line.get_channel_access_token()

        if token:
            if data_flg:
                if proc_flg:
                    msg_list = get_msg_list(auto_flg)

                else:
                    msg_list = [[MSG_TYPE_IMG, URL_TODAY_IMG]]

                # メッセージ取得
                messages = func_line.get_line_messages(msg_list)

            else:
                template_msg = get_template_msg()
                messages = func_line.get_send_messages(template_msg)

            # メッセージ送信
            func_line.send_message(token, messages)

    func.print_end(app_name)


# メッセージリスト取得
def get_msg_list(auto_flg: bool = const.FLG_ON) -> list[list[str]]:
    if auto_flg:
        msg_data_list, date_today = get_msg_data_today()
        if WEEKLY_DIV_FRI in date_today:
            ai_news_msg = news.get_news_msg_list(news.DIV_AI_NEWS_LIST)
            msg_data_list = get_msg_data_list(
                FILE_DIV_AI_NEWS, MSG_TYPE_TXT, ai_news_msg, date_today
            )
            msg_list.append(msg_data_list)

    else:
        msg_div = const.STR_NOTIFY
        msg_data = func.get_input_data(const.STR_MESSAGE, msg_div)
        msg_data_list = get_msg_data_list(msg_div, MSG_TYPE_TXT, msg_data)

    msg_list = [msg_data_list]
    return msg_list


# メッセージデータ取得
def get_msg_data_today() -> tuple[list[str], str]:
    today_info = func_api.get_result_on_app(const.APP_TODAY)
    if today_info:
        date_today = today_info[0][today.app_title]
        forecast = today_info[1][today.app_title].split("・")[0]
        today_outfit = today_info[2][today.app_title]

        data_list = [list(info.values()) for info in today_info[1:]]
        msg_data = [f"[{data[0]}] {data[1]}" for data in data_list]

        msg_data_list = get_msg_data_list(
            const.APP_TODAY, MSG_TYPE_IMG, msg_data, date_today, forecast, today_outfit
        )
        return msg_data_list, date_today


# テンプレートメッセージ取得
def get_template_msg():
    alt_text = "今日も一日お疲れ様でした。"

    template_title = "【今日の一言】"

    file_path = func.get_file_path(const.STR_PHRASE, const.FILE_TYPE_CSV)
    dict_data = func.get_dict_from_csv(file_path)
    random_int = str(func.get_random_int(const.MAX_PHRASE_CSV))
    key = random_int.zfill(3)
    phrase = dict_data.get(key)[1]
    template_text = phrase

    actions = get_template_actions()

    template_msg = func_line.get_template_msg_json(
        alt_text, template_title, template_text, actions
    )
    return template_msg


# テンプレートアクション取得
def get_template_actions():
    # news_lbl, news_url = news.get_news_list(news.DIV_NIKKEI_NEWS, url_flg=const.FLG_ON)
    ai_lbl, ai_url = news.get_news_list(news.DIV_AI_NEWS, url_flg=const.FLG_ON)
    mlb_lbl, mlb_url = mlb.get_last_game_info()
    lcc_lbl, lcc_url = lcc.get_lcc_info_list(list_flg=const.FLG_OFF)
    korean_lbl, korean_url = study.get_today_korean()
    # tv_lbl, tv_url = tv.get_tv_info_today()

    label_list = [ai_lbl, mlb_lbl, lcc_lbl, korean_lbl]
    url_list = [ai_url, mlb_url, lcc_url, korean_url]

    actions = []
    for label, url in zip(label_list, url_list):
        if label:
            action = {"type": "uri", "label": label, "uri": url}
            actions.append(action)
    return actions


# メッセージ取得
def get_msg_data_list(
    msg_div: str,
    msg_type: str,
    msg_data: list[str],
    date_today: str = const.SYM_BLANK,
    forecast: str = const.SYM_BLANK,
    today_outfit: str = const.SYM_BLANK,
) -> list[str]:
    text_title = get_title(msg_div, msg_type, date_today)
    text_msg = text_title + const.SYM_NEW_LINE + NEW_LINE.join(msg_data)

    if msg_type == MSG_TYPE_IMG:
        if msg_div == const.APP_TODAY:
            file_path = func_gemini.get_today_news_image(
                text_msg, forecast, today_outfit
            )
            if not file_path:
                func_api.create_msg_img(msg_div, text_msg, forecast)

        text_msg = URL_TODAY_IMG
        func.print_info_msg(MSG_TYPE_IMG, text_msg)

    msg_data_list = [msg_type, text_msg]
    return msg_data_list


# タイトル取得
def get_title(
    div: str, msg_type: str = const.SYM_BLANK, date_today: str = const.SYM_BLANK
) -> str:
    title_div = div.upper()

    if div == const.APP_NEWS:
        title_div = news.DIV_NEWS.format(const.SYM_BLANK)
    elif div == FILE_DIV_AI_NEWS:
        title_div = news.DIV_AI_NEWS
    else:
        if date_today:
            title_div = date_today

    title_txt = DIV_MARK_TXT.format(title_div)
    title_img = DIV_MARK_IMG.format(title_div)

    if msg_type == MSG_TYPE_TXT:
        title_list = [DIV_MARK, title_txt, DIV_MARK]
        title = NEW_LINE.join(title_list)
    elif msg_type == MSG_TYPE_IMG:
        title = title_img
    else:
        title = title_div

    return title


if __name__ == const.MAIN_FUNCTION:
    get_msg_data_today()
    # get_template_actions()
    # main(auto_flg=const.FLG_OFF)
    # main(data_flg=const.FLG_OFF)
    # main(proc_flg=const.FLG_OFF)
