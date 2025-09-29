# 説明: LINEメッセージ

import sys

import apps.today_korea as today_korea
import apps.utils.constants as const
import apps.utils.message_constants as msg_const
import apps.utils.function as func
import apps.utils.function_gemini as func_gemini
import apps.utils.function_kakao as func_kakao

# スクリプト名
SCRIPT_NAME = func.get_app_name(__file__)


def main(temp_div: str = func_kakao.OBJECT_TYPE_FEED):
    """
    メインの処理を実行

    引数:
        temp_div (str): feed, text, list
    """

    func.print_start(SCRIPT_NAME)

    if func_kakao.KAKAO_API_KEY:
        # アクセストークン取得
        token = func_kakao.get_access_token()
        if token:
            try:
                img_flg = const.FLG_ON
                if temp_div == func_kakao.OBJECT_TYPE_TEXT:
                    img_flg = const.FLG_OFF

                # 今日のニュース取得
                (message, title, link, link_mo, forecast, outfit) = (
                    today_korea.get_today_info(img_flg)
                )

                if temp_div == func_kakao.OBJECT_TYPE_FEED:
                    file_path = func_gemini.get_today_news_image(
                        message, forecast, outfit[:20], const.APP_TODAY_KOREA
                    )

                    if file_path:
                        msg = func_kakao.URL_TODAY_KOREA_IMG
                        func.print_info_msg(const.STR_IMG, msg)

                        title = "【오늘의 한마디】"
                        message = today_korea.get_phrase()

                    else:
                        temp_div = func_kakao.OBJECT_TYPE_TEXT

                # メッセージ送信
                func_kakao.send_message(token, temp_div, title, message, link, link_mo)

            except Exception as e:
                if e.args[0] != "details":
                    curr_func_nm = sys._getframe().f_code.co_name
                    err_msg = msg_const.MSG_ERR_MSG_SEND
                    func.print_error_msg(SCRIPT_NAME, curr_func_nm, err_msg, e)

    func.print_end(SCRIPT_NAME)


if __name__ == const.MAIN_FUNCTION:
    main()
