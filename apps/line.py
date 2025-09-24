# 説明: LINEメッセージ

import sys

import apps.lcc as lcc
import apps.news as news
import apps.study as study
import apps.today as today
import apps.tv as tv
import apps.utils.constants as const
import apps.utils.message_constants as msg_const
import apps.utils.function as func
import apps.utils.function_api as func_api
import apps.utils.function_gemini as func_gemini
import apps.utils.function_line as func_line

# スクリプト名
SCRIPT_NAME = func.get_app_name(__file__)

# 改行
NEW_LINE = const.SYM_NEW_LINE

# メッセージタイプ
MSG_TYPE_TXT = "text"
MSG_TYPE_IMG = "image"

# ファイル区分
FILE_DIV_AI_NEWS = "ai_news"

# タイトル
DIV_MARK = "*----*----*----*----*----*"
DIV_MARK_TXT = "*-- {} --*"
# DIV_MARK_IMG = "=== {} ==="
DIV_MARK_IMG = "■ {} ■"

# 曜日
WEEKLY_DIV_FRI = "Fri"


def main(
    data_div: int = const.NUM_ONE,
    proc_flg: bool = const.FLG_ON,
    auto_flg: bool = const.FLG_ON,
):
    """
    メインの処理を実行

    引数:
        data_div  (int): 1:通常、2:テンプレート、3:フレックス
        proc_flg (bool): 処理実行を有効にするフラグ
        auto_flg (bool): 自動処理を有効にするフラグ
    """

    func.print_start(SCRIPT_NAME)

    if func_line.LINE_CHANNEL_ID:
        # チャネル・アクセストークン取得
        token = func_line.get_channel_access_token()

        if token:
            try:
                if data_div == const.NUM_ONE:
                    if proc_flg:
                        msg_list = get_msg_list(auto_flg)

                    else:
                        msg_list = [[MSG_TYPE_IMG, func_line.URL_TODAY_IMG]]

                    # メッセージ取得
                    messages = func_line.get_line_messages(msg_list)

                else:
                    if data_div == const.NUM_TWO:
                        # テンプレートメッセージ取得
                        messages = get_template_msg()
                    else:
                        # フレックスメッセージ取得
                        messages = get_flex_msg()

                # メッセージ送信
                func_line.send_message(token, messages)

            except Exception as e:
                curr_func_nm = sys._getframe().f_code.co_name
                err_msg = msg_const.MSG_INFO_SERVER_KEEP_WORKING
                func.print_error_msg(SCRIPT_NAME, curr_func_nm, err_msg, e)

                if not func.is_local_env():
                    msg = f"[{err_msg}]\n{e[:100]}"
                    func_line.send_text_msg(msg)

    func.print_end(SCRIPT_NAME)


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
    messages = []

    alt_text = "今日も一日お疲れ様でした。"
    template_title = "【今日の一言】"
    template_text = today.get_today_phrase()
    actions = get_template_actions()

    template_msg = func_line.get_template_msg_json(
        alt_text, template_title, template_text, actions
    )

    messages.append(template_msg)
    return messages


# テンプレートアクション取得
def get_template_actions():
    actions = []
    temp_item_list = [news, tv, lcc, study]

    for item in temp_item_list:
        try:
            # テンプレートメッセージ取得
            label, url = item.get_temp_msg()
        except:
            continue

        if label:
            label = label[: const.MAX_TEMP_MSG]
            action = {"type": "uri", "label": label, "uri": url}
            actions.append(action)
    return actions


# フレックスメッセージ取得
def get_flex_msg():
    messages = []
    alt_text = today.get_today_phrase()
    data_list = get_flex_data_list()
    flex_msg = func_line.get_flex_msg_json(alt_text, data_list)
    messages.append(flex_msg)
    return messages


# フレックスメッセージ・データ取得
def get_flex_data_list():
    header_list = ["Check#1", "Check#2", "Check#3"]
    fund_goal_list = [30000, 50000, 50000]

    rate_list = []
    body_list = []
    for fund_no, fund_goal in zip(const.LIST_FUND_NO, fund_goal_list):
        fund_name, point = today.get_today_nisa(fund_no, msg_flg=const.FLG_OFF)
        int_point = int(
            point.replace(const.SYM_COMMA, const.SYM_BLANK).replace(
                const.STR_JPY_JA, const.SYM_BLANK
            )
        )
        rate = (int_point / fund_goal) * 100
        str_rate = f"{int(rate)}%"
        body_text = f"{fund_name}{const.SYM_NEW_LINE}{point}"
        rate_list.append(str_rate)
        body_list.append(body_text)

    data_list = [header_list, rate_list, body_list]
    return data_list


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

        text_msg = func_line.URL_TODAY_IMG
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

    if msg_type == MSG_TYPE_TXT:
        title_txt = DIV_MARK_TXT.format(title_div)
        title_list = [DIV_MARK, title_txt, DIV_MARK]
        title = NEW_LINE.join(title_list)
    elif msg_type == MSG_TYPE_IMG:
        title_img = DIV_MARK_IMG.format(title_div)
        title = title_img
    else:
        title = title_div

    return title


if __name__ == const.MAIN_FUNCTION:
    get_msg_data_today()
    # get_template_actions()
    # get_flex_data_list()
    # main(proc_flg=const.FLG_OFF)
    # main(data_div=const.NUM_TWO)
    # main(data_div=const.NUM_THREE)
    # main(auto_flg=const.FLG_OFF)
