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
    object_type: str = func_kakao.OBJECT_TYPE_FEED,
    div: str = const.APP_TODAY,
    list_flg: bool = const.FLG_OFF,
):
    """
    メインの処理を実行

    引数:
        object_type (str): feed, text, list, test
        div (str): today, lcc
        list_flg (bool): 一括送信フラグ # TODO: [pending] チャネル登録必要
    """
    curr_func_nm = sys._getframe().f_code.co_name

    func.print_start(SCRIPT_NAME)

    if func_kakao.KAKAO_API_KEY:
        # アクセストークン取得
        token = func_kakao.get_access_token()
        if token:
            try:
                if div == const.APP_TODAY:
                    # 今日のニュース取得
                    message, file_path = today_korea.get_today_info(object_type)
                    title = today_korea.TITLE_LINK
                    link = today_korea.URL_LINK
                    link_mo = today_korea.URL_LINK_MO

                    img_file_path = func_kakao.URL_TODAY_KOREA_IMG
                    if file_path:
                        func.print_debug_msg(const.STR_IMG, img_file_path)

                        title = "【오늘의 한마디】"
                        message = today_korea.get_phrase()

                    else:
                        func.print_debug_msg(
                            img_file_path, msg_const.MSG_ERR_SERVER_PROC_FAILED
                        )
                        object_type = func_kakao.OBJECT_TYPE_TEXT

                    receiver_uuids = []
                    if list_flg:
                        receiver_uuids = func_kakao.get_receiver_uuids(token)

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

                else:
                    lbl = data = const.SYM_BLANK
                    if div == const.APP_LCC:
                        lbl, data = lcc.get_temp_msg(data_flg=const.FLG_ON)
                    elif div == const.APP_NEWS:
                        lbl = div
                        data = today_korea.get_it_news()

                    if lbl and data:
                        # メッセージ送信
                        func_kakao.send_kakao_msg(token, title=lbl, message=data)

            except Exception as e:
                if e.args[0] != "details":
                    err_msg = msg_const.MSG_ERR_MSG_SEND
                    func.print_error_msg(SCRIPT_NAME, curr_func_nm, err_msg, e)

        else:
            msg = msg_const.MSG_ERR_TOKEN_NOT_EXIST
            func.print_error_msg(SCRIPT_NAME, curr_func_nm, msg)

    func.print_end(SCRIPT_NAME)


if __name__ == const.MAIN_FUNCTION:
    main()
