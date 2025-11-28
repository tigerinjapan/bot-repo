"""
KakaoメッセージAPI
"""

import sys

import apps.lcc as lcc
import apps.today_korea as today_korea
import apps.utils.constants as const
import apps.utils.message_constants as msg_const
import apps.utils.function as func
import apps.utils.function_kakao as func_kakao

# スクリプト名
SCRIPT_NAME = func.get_app_name(__file__)


def main(
    div: str = const.APP_TODAY,
    object_type=func_kakao.OBJECT_TYPE_TEXT,
    list_flg: bool = const.FLG_OFF,
):
    """
    メインの処理を実行

    引数:
        div (str): today, ai_news, lcc, test
        object_type (str): feed, list, text
        list_flg (bool): 一括送信フラグ # TODO: [pending] チャネル登録必要
    """
    curr_func_nm = sys._getframe().f_code.co_name

    func.print_start(SCRIPT_NAME)

    if func_kakao.KAKAO_API_KEY:
        # アクセストークン取得
        token = func_kakao.get_access_token()
        if token:
            try:

                receiver_uuids = []
                if list_flg:
                    receiver_uuids = func_kakao.get_receiver_uuids(token)

                title = div

                if div == const.APP_TODAY:
                    # 今日のニュース取得
                    message, file_path = today_korea.get_today_info()
                    if file_path:
                        object_type = func_kakao.OBJECT_TYPE_FEED
                        title = "【오늘의 한마디】"
                        message = today_korea.get_phrase()
                    else:
                        title = today_korea.TITLE_LINK

                    link = today_korea.URL_LINK
                    link_mo = today_korea.URL_LINK_MO

                elif div == const.APP_LCC:
                    title, message = lcc.get_temp_msg(data_flg=const.FLG_ON)
                    link = link_mo = const.URL_LCC

                elif div == const.STR_AI_NEWS:
                    object_type = func_kakao.OBJECT_TYPE_LIST
                    message = today_korea.get_it_news_list()
                    link = link_mo = today_korea.URL_ET_NEWS

                else:
                    message = div

                if title and message:
                    # メッセージ送信
                    func_kakao.send_kakao_msg(
                        token,
                        object_type,
                        title,
                        message,
                        link,
                        link_mo,
                        receiver_uuids,
                    )

            except Exception as e:
                if e.args[0] != "details":
                    err_msg = msg_const.MSG_ERR_MSG_SEND
                    func.print_error_msg(SCRIPT_NAME, curr_func_nm, err_msg, e)

        else:
            msg = msg_const.MSG_ERR_TOKEN_NOT_EXIST
            func.print_error_msg(SCRIPT_NAME, curr_func_nm, msg)

    func.print_end(SCRIPT_NAME)


if __name__ == const.MAIN_FUNCTION:
    div = const.APP_TODAY
    # div = const.APP_LCC
    # div = const.APP_NEWS
    main(div)
