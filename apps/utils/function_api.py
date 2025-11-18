"""
API関数
"""

import requests
import sys
from PIL import Image, ImageDraw, ImageFont

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.message_constants as msg_const

# スクリプト名
SCRIPT_NAME = func.get_app_name(__file__)

# URL
URL_SERVER = func.get_server_url()

# プロパティ
IMG_NO = func.get_env_val("LINE_IMG_DIV", div=const.STR_ENV_VAR)


def get_response_result(
    url: str,
    request_type: str = const.REQUEST_TYPE_GET,
    headers={},
    data={},
    header_json_flg: bool = const.FLG_ON,
    log_flg: bool = const.FLG_ON,
):
    """
    リクエスト結果取得
    """
    result = except_ = msg = const.NONE_CONSTANT
    curr_func_nm = sys._getframe().f_code.co_name

    if log_flg:
        div = f"{const.STR_API} {curr_func_nm}"
        func.print_debug_msg(div, url)

    if header_json_flg:
        api_headers = const.API_HEADERS_JSON
    else:
        api_headers = const.API_HEADERS_UTF8
    headers.update(api_headers)

    try:
        if request_type == const.REQUEST_TYPE_GET:
            response = requests.get(url, headers=headers)

        elif request_type == const.REQUEST_TYPE_POST:
            response = requests.post(url, headers=headers, data=data)

        res_status = response.status_code
        res_text = response.text
        if res_status in const.STATUS_CODE_NORMAL:
            result = func.get_loads_json(res_text)
        else:
            err_msg = f"{res_status} {res_text}"
            func.print_error_msg(SCRIPT_NAME, curr_func_nm, err_msg)
            if not response:
                err_msg = f"{url} {msg_const.MSG_ERR_API_RESPONSE_NONE}"
                func.print_error_msg(SCRIPT_NAME, curr_func_nm, err_msg)

    except requests.exceptions.ConnectionError as ce:
        msg = f"{msg_const.MSG_ERR_SERVER_NOT_WORKING} {url}"
        except_ = ce

    except KeyError as ke:
        msg = msg_const.MSG_ERR_DATA_NOT_EXIST
        except_ = ke

    if except_:
        func.print_error_msg(SCRIPT_NAME, curr_func_nm, msg, except_)

    return result


def get_json_data_on_app(app_name: str, token_flg: bool = const.FLG_OFF):
    """
    JSONデータ取得
    """
    url = f"{URL_SERVER}/{const.FILE_TYPE_JSON}/{app_name}"
    if token_flg:
        url += f"?token=token_{func.get_now(const.DATE_TODAY)}"
    result = get_response_result(url, log_flg=const.FLG_OFF)
    return result


def post_api_on_server(path: str, json_data):
    """
    API送信
    """
    url = f"{URL_SERVER}{path}"
    result = get_response_result(
        url, request_type=const.REQUEST_TYPE_POST, data=json_data
    )
    return result


def create_msg_img(div: str, msg: str, forecast: str = const.SYM_BLANK) -> str:
    """
    画像に文字列挿入
    """
    if forecast:
        if "雨" in forecast:
            img_div = "rainy"
        elif "雪" in forecast:
            img_div = "snowy"
        elif "曇" in forecast:
            img_div = "cloudy"
        else:
            img_div = "sunny"
    else:
        img_div = const.APP_NEWS

    # 任意の数値取得
    img_seq = str(func.get_random_int(const.MAX_RANDOM_IMG, const.NUM_ONE))
    img_no = str(IMG_NO) + img_seq.zfill(2)

    img_file_base = f"{img_div}_{img_no}"

    font_type = const.FONT_TYPE_UZURA
    font_size = 11
    xy_size = (45, 90)
    if div == const.APP_TODAY:
        xy_size = (60, 200)
        if IMG_NO == const.NUM_ONE:
            font_size = 16
            xy_size = (20, 140)

    file_path = insert_msg_to_img(
        div, img_file_base, font_type, font_size, xy_size, msg
    )

    img_file_name = func.get_app_name(file_path)
    return img_file_name


def insert_msg_to_img(
    div: str,
    img_file_name: str,
    font_type: str,
    font_size: int,
    xy_size: tuple[int, int],
    msg: str,
) -> str:
    """
    メッセージ画像生成
    """
    img_file_path = func.get_file_path(img_file_name, const.FILE_TYPE_JPEG)

    img = Image.open(img_file_path).rotate(0)
    draw = ImageDraw.Draw(img)

    font_path = func.get_file_path(font_type, const.FILE_TYPE_TTC)
    font = ImageFont.truetype(font=font_path, size=font_size)

    draw.text(xy=xy_size, text=msg, fill="black", font=font, align="left")

    file_path = func.get_file_path(div, const.FILE_TYPE_JPEG, const.STR_OUTPUT)
    img.save(file_path, optimize=const.FLG_ON)
    return file_path


def get_target_data(
    data, search_value: str, target_key: str, search_key: str = const.STR_DIV_JA
):
    """
    リストの中で、一つ値をキーに、対象データ取得
    """
    target_info = const.SYM_BLANK

    # リストの要素（辞書）を一つずつ確認
    for item in data:
        if item.get(search_key) == search_value:
            target_info = item.get(target_key)
            break
    return target_info


if __name__ == const.MAIN_FUNCTION:
    result = get_json_data_on_app(const.APP_TODAY)
    func.print_test_data(result, type_flg=const.FLG_ON)
