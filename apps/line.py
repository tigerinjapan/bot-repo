"""
LINEメッセージ
"""

import sys

import apps.event as event
import apps.lcc as lcc
import apps.mlb as mlb
import apps.news as news
import apps.study as study
import apps.today as today
import apps.tv as tv
import apps.utils.constants as const
import apps.utils.message_constants as msg_const
import apps.utils.function as func
import apps.utils.function_api as func_api
import apps.utils.function_beautiful_soup as func_bs
import apps.utils.function_gemini as func_gemini
import apps.utils.function_line as func_line

# スクリプト名
SCRIPT_NAME = func.get_app_name(__file__)

# URL
URL_TODAY_IMG = f"{func_api.URL_KOYEB_IMG}/{const.APP_TODAY}"
URL_NISA = f"{const.URL_SMBC_FUND}/{const.FUND_NO_SP_500}/"
URL_EX = f"{const.URL_GOOGLE}/finance/quote/JPY-KRW"


# 改行
NEW_LINE = const.SYM_NEW_LINE


def main(
    data_div: int = const.NUM_ONE,
    proc_flg: bool = const.FLG_ON,
    auto_flg: bool = const.FLG_ON,
):
    """
    メイン処理実行

    引数:
        data_div (int): 1:通常、2:テンプレート、3:フレックス
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
                        msg_list = [[const.MSG_TYPE_IMG, URL_TODAY_IMG]]

                    # メッセージ取得
                    messages = func_line.get_line_messages(msg_list)

                else:
                    # テンプレートメッセージ取得
                    messages = get_template_msg(data_div)

                # メッセージ送信
                func_line.send_line_msg(token, messages)

            except Exception as e:
                curr_func_nm = sys._getframe().f_code.co_name
                err_msg = msg_const.MSG_ERR_MSG_SEND
                func.print_error_msg(SCRIPT_NAME, curr_func_nm, err_msg, e)

                # LINE通知
                msg = f"[{err_msg}]\n{e[:100]}"
                sub(SCRIPT_NAME, msg)

    func.print_end(SCRIPT_NAME)


def sub(div: str, data_list: list[str] = []):
    """
    メッセージ送信
    """
    msg_json_list = []
    msg_list = []
    msg_data = const.SYM_BLANK
    data_list = []

    date_today = func.get_now(const.DATE_TODAY, const.DATE_FORMAT_YYYYMMDD_SLASH)

    if div == const.STR_NISA:
        # フレックスメッセージ取得
        alt_text = f"[{date_today}] {div}"
        msg_json_list = get_flex_msg(alt_text)

    else:
        if div == const.APP_MLB:
            msg_data = mlb.get_mlb_game_data(all_flg=const.FLG_ON)

        else:
            if div == const.STR_AI_NEWS:
                news_list = news.get_news_list(news.DIV_AI_NEWS, url_flg=const.FLG_ON)
                data_list = [
                    f"{news_data[0]}{NEW_LINE}{news_data[1]}"
                    for news_data in news_list[:3]
                ]

            if data_list:
                msg_data = NEW_LINE.join(data_list)

        if msg_data:
            msg_list.append(msg_data)
            msg_data_list = get_msg_data_list(
                div, const.MSG_TYPE_TXT, msg_list, date_today
            )
            msg_json_list = func_line.get_line_messages([msg_data_list])

    if msg_json_list:
        func_line.send_msg_for_admin(msg_json_list)


def get_msg_list(auto_flg: bool = const.FLG_ON) -> list[list[str]]:
    """
    メッセージリスト取得
    """
    msg_list = []
    if auto_flg:
        msg_div = const.APP_TODAY
        msg_type = const.MSG_TYPE_IMG
        msg_data = URL_TODAY_IMG
        date_today = today.get_today_image()

    else:
        msg_div = const.STR_NOTIFY
        msg_type = const.MSG_TYPE_TXT
        msg_data = func.get_input_data(const.STR_MESSAGE, msg_div)
        date_today = const.SYM_BLANK

    msg_data_list = get_msg_data_list(msg_div, msg_type, msg_data, date_today)
    msg_list.append(msg_data_list)
    return msg_list


def get_template_msg(data_div: int = const.NUM_TWO):
    """
    テンプレートメッセージ取得
    """
    messages = []

    if data_div == const.NUM_TWO:
        temp_text = event.get_item_list()
        forecast, temp_title, temp_msg_list = get_temp_msg_list()
        img_file_name = func_api.get_img_file_div(forecast)
        img_url = f"{func_api.URL_KOYEB_IMG}/{img_file_name}"
    else:
        img_url, temp_title, temp_text = get_temp_img()
        temp_msg_list = get_temp_msg_list_2()

    alt_text = today.get_today_phrase()
    actions = get_template_actions(temp_msg_list)
    template_msg = func_line.get_template_msg_json(
        alt_text, img_url, temp_title, temp_text, actions
    )
    messages.append(template_msg)
    return messages


def get_template_actions(temp_msg_list: list):
    """
    テンプレートアクション取得
    """
    actions = []
    if temp_msg_list:
        for temp_msg in temp_msg_list:
            label = temp_msg[0]
            url = temp_msg[1]
            label = label[: const.MAX_TEMP_MSG]
            action = {"type": "uri", "label": label, "uri": url}
            actions.append(action)
    return actions


def get_temp_msg_list():
    """
    メッセージデータ取得
    """
    temp_msg_list = []

    url_list = [today.URL_WEATHER, URL_NISA, URL_EX]
    today_info = func_api.get_json_data_on_app(const.APP_TODAY)
    if today_info:
        date = today_info[0][const.APP_NEWS]
        temp_title = date.split(const.SYM_SPACE)[0]

        weather = today_info[1][const.APP_NEWS]
        forecast = weather.split("・")[0]

        data_list = [list(info.values()) for info in today_info[1:4]]
        for data, url in zip(data_list, url_list):
            div = data[0]
            lbl = data[1]
            split_str = " = "
            if split_str in lbl:
                lbl_list = lbl.split(split_str)
                div = lbl_list[0]
                lbl = lbl_list[1]

            label = f"[{func.upper_str(div)}] {lbl}"
            temp_msg = [label, url]
            temp_msg_list.append(temp_msg)
        return forecast, temp_title, temp_msg_list


def get_temp_msg_list_2():
    """
    メッセージデータ取得
    """
    temp_msg_list = []

    app_list = [tv, lcc, study]
    for app in app_list:
        try:
            # テンプレートメッセージ取得
            div, lbl, url = app.get_temp_msg()
            label = f"[{func.upper_str(div)}] {lbl}"
        except:
            continue

        if label:
            temp_msg = [label, url]
            temp_msg_list.append(temp_msg)

    return temp_msg_list


def get_temp_img(section: str = const.STR_WORLD):
    """
    イメージ取得
    """
    img_url = headline = const.SYM_BLANK

    title = f"CNN {func.upper_str(section)}"
    url = f"https://edition.cnn.com/{section}"
    class_ = "container__item--type-media-image"
    soup = func_bs.get_elem_from_url(url, attr_val=class_)
    if soup:
        img_elem = func_bs.find_elem_by_class(soup, "image__hide-placeholder")
        img_url = img_elem.get("data-url").replace("?c=original", const.SYM_BLANK)
        headline_elem = func_bs.find_elem_by_class(soup, "container__headline-text")
        headline_text = headline_elem.text
        response = func_gemini.get_gemini_response(
            title, headline_text, msg_flg=const.FLG_ON
        )
        if response:
            headline = response[0]
        else:
            headline = f"{headline_text[57:]}..."
    return img_url, title, headline


def get_flex_msg(alt_text: str = const.SYM_BLANK):
    """
    フレックスメッセージ取得
    """
    messages = []
    if not alt_text:
        alt_text = today.get_today_phrase()
    data_list = get_flex_data_list()
    flex_msg = func_line.get_flex_msg_json(alt_text, data_list)
    messages.append(flex_msg)
    return messages


def get_flex_data_list():
    """
    フレックスメッセージ・データ取得
    """
    header_list = ["Check#1", "Check#2", "Check#3"]
    fund_goal_list = [30000, 50000, 50000]

    rate_list = []
    body_list = []
    for fund_no, fund_goal in zip(const.LIST_FUND_NO, fund_goal_list):
        fund_name, point = today.get_today_nisa(fund_no, msg_flg=const.FLG_OFF)

        target_list = [const.SYM_COMMA, const.STR_JPY_JA]
        point_str = func.get_replace_data(point, target_list)
        rate = (int(point_str) / fund_goal) * 100
        rate_str = f"{int(rate)}%"
        body_text = f"{fund_name}{NEW_LINE}{point}"

        rate_list.append(rate_str)
        body_list.append(body_text)

    data_list = [header_list, rate_list, body_list]
    return data_list


def get_msg_data_list(
    msg_div: str,
    msg_type: str,
    msg_data: list[str] | str,
    date_today: str = const.SYM_BLANK,
) -> list[str]:
    """
    メッセージデータリスト取得
    """
    if msg_type == const.MSG_TYPE_IMG:
        msg = msg_data
    else:
        title = get_title(msg_div, msg_type, date_today)
        msg = title + NEW_LINE + NEW_LINE.join(msg_data)

    msg_data_list = [msg_type, msg]
    return msg_data_list


def get_title(
    div: str, msg_type: str = const.SYM_BLANK, date_today: str = const.SYM_BLANK
) -> str:
    """
    タイトル取得
    """
    title_div = func.upper_str(div)

    if msg_type == const.MSG_TYPE_TXT:
        total_length = len(const.DIV_MARK)
        title_txt = get_title_mark(title_div, const.MARK_PATTERN_1, total_length)
        if date_today:
            date_text = get_title_mark(date_today, const.MARK_PATTERN_1, total_length)
            title_txt = date_text + NEW_LINE + title_txt

        title_list = [const.DIV_MARK, title_txt, const.DIV_MARK]
        title = NEW_LINE.join(title_list)

    elif msg_type == const.MSG_TYPE_IMG:
        if div == const.APP_TODAY and date_today:
            title_div = date_today

        title_img = get_title_mark(title_div, const.MARK_PATTERN_2)
        title = title_img

    else:
        title = title_div

    return title


def get_title_mark(
    target_str: str, div_mark_pattern: str, total_length: int = const.NUM_ZERO
) -> str:
    """
    タイトルマーク取得

    指定された文字列を任意の長さの中央に配置し、任意のパターンで左右を埋める
    """
    left_mark = right_mark = div_mark_pattern
    if total_length != const.NUM_ZERO:
        # 1. 挿入部分の長さ (target_str + 左右の必須スペース)
        insert_len = len(target_str) + 2

        # 2. 左右のマーク部分の合計長を計算
        mark_total_len = total_length - insert_len

        # 3. 左右のマークの長さを計算 (左右で長さが違う場合は、右側を長くする)
        left_mark_len = mark_total_len // 2
        right_mark_len = mark_total_len - left_mark_len

        # 4. マーク文字列の作成ロジック
        #    パターンを繰り返し、必要な長さの分だけ切り取る
        def create_mark(length, pattern):
            if length <= 0:
                return const.SYM_BLANK

            # パターンを繰り返し繋げ、必要な長さで切り取る
            repeat_count = (length + len(pattern) - 1) // len(pattern)
            full_mark = pattern * repeat_count
            return full_mark[:length]

        # 5. 左右のマーク取得
        left_mark = create_mark(left_mark_len, div_mark_pattern)
        right_mark = create_mark(right_mark_len, div_mark_pattern)

    # 6. 全体を結合して、完成
    # (左マーク)(スペース1)(target_str)(スペース1)(追加スペース)(右マーク)
    result = f"{left_mark} {target_str} {right_mark}"
    return result


def sub_test():
    """
    [テスト] メッセージ送信
    """
    data_list = [
        "[70] ありがとうございますありがとうございますありがとうございますありがとうございます",
        "[71] ABCDEEGHIJABCDEEGHIJABCDEEGHIJABCDEEGHIJ",
        "[72] 안녕하세요감사합니다안녕하세요감사합니다안녕하세요감사합니다안녕하세요감사합니다",
        "[73] １２３４５６７８９０１２３４５６７８９０１２３４５６７８９０１２３４５６７８９０",
    ]
    sub(const.STR_TEST, data_list)


if __name__ == const.MAIN_FUNCTION:
    # main()
    # main(proc_flg=const.FLG_OFF)
    main(data_div=const.NUM_TWO)
    # main(data_div=const.NUM_THREE)
    # main(auto_flg=const.FLG_OFF)
    # sub(const.STR_AI_NEWS)
