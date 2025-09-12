# 説明: API関数

import requests
from PIL import Image, ImageDraw, ImageFont

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.message_constants as msg_const

# URL
URL_KOYEB_APP = "https://" + func.get_env_val("URL_KOYEB")

# プロパティ
IMG_NO = func.get_env_val("LINE_IMG_DIV", int_flg=const.FLG_ON)
NUM_IMG_MAX_SEQ = 4
FONT_TYPE_UZURA = "uzura"


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

    try:
        if request_type == const.REQUEST_TYPE_GET:
            response = requests.get(url, headers=headers)

        elif request_type == const.REQUEST_TYPE_POST:
            response = requests.post(url, headers=headers, data=data)

    except requests.exceptions.ConnectionError as ce:
        func.print_error_msg(url, msg_const.MSG_ERR_API_REQUEST_CONNECT)
        return result

    res_status = response.status_code
    res_text = response.text
    if res_status in const.STATUS_CODE_NORMAL:
        result = func.get_loads_json(res_text)

    else:
        func.print_error_msg(res_status, res_text)
        if not response:
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


# 画像に文字列挿入
def create_msg_img(div: str, msg: str, forecast: str) -> str:

    if div == const.APP_TODAY:
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
    img_seq = str(func.get_random_int(NUM_IMG_MAX_SEQ, const.NUM_ONE))
    img_no = str(IMG_NO) + img_seq.zfill(2)

    img_file_base = f"{img_div}_{img_no}"

    font_type = FONT_TYPE_UZURA
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


# メッセージ画像生成
def insert_msg_to_img(
    div: str,
    img_file_name: str,
    font_type: str,
    font_size: int,
    xy_size: tuple[int, int],
    msg: str,
) -> str:
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
