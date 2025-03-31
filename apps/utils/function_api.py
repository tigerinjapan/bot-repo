# 説明: API関数

import requests
from PIL import Image, ImageDraw, ImageFont

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.message_constants as msg_const

# URL
URL_KOYEB_APP = "https://" + func.get_env_val("URL_KOYEB")


# リクエスト送信
def get_response_result(
    url: str,
    request_type: str = const.REQUEST_TYPE_GET,
    headers={},
    data={},
    header_json_flg: bool = const.FLG_ON,
):
    result = const.NONE_CONSTANT

    if header_json_flg:
        headers.update(const.HEADERS_JSON)

    if request_type == const.REQUEST_TYPE_GET:
        response = requests.get(url, headers=headers)

    elif request_type == const.REQUEST_TYPE_POST:
        response = requests.post(url, headers=headers, data=data)

    if response:
        res_status = response.status_code
        res_text = response.text
        if res_status not in const.STATUS_CODE_NORMAL:
            func.print_error_msg(res_status, res_text)
        else:
            result = func.get_loads_json(res_text)
    else:
        func.print_error_msg(const.STR_API, msg_const.MSG_ERR_API_RESPONSE_NONE)

    return result


# API結果取得
def get_result_on_app(app_name: str):
    base_url = URL_KOYEB_APP
    if func.is_local_env():
        base_url = func.get_local_url()
    url = f"{base_url}/{const.FILE_TYPE_JSON}/{app_name}?token=token_{const.DATE_TODAY}"
    result = get_response_result(url)
    return result


# メッセージ画像生成
def insert_msg_to_img(
    div: str,
    img_file_name: str,
    font_type: str,
    font_size: int,
    xy_size: tuple[int, int],
    msg: str,
):
    img_file_path = func.get_file_path(img_file_name, const.FILE_TYPE_JPEG)

    img = Image.open(img_file_path).rotate(0)
    draw = ImageDraw.Draw(img)

    font_path = func.get_file_path(font_type, const.FILE_TYPE_TTC)
    font = ImageFont.truetype(font=font_path, size=font_size)

    draw.text(xy=xy_size, text=msg, fill="black", font=font, align="left")

    file_path = func.get_file_path(div, const.FILE_TYPE_JPEG, const.STR_OUTPUT)
    img.save(file_path, optimize=const.FLG_ON)
    return file_path


if __name__ == const.MAIN_FUNCTION:
    result = get_result_on_app(const.APP_TODAY)
    func.print_test_data(result, type_flg=const.FLG_ON)
