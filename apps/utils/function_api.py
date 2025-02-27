# 説明：API関数

import requests
from PIL import Image, ImageDraw, ImageFont

import apps.utils.constants as const
from apps.utils.function import get_file_path


# リクエスト送信
def get_response_result(
    url: str,
    request_type: str = const.REQUEST_TYPE_GET,
    headers=const.NONE_CONSTANT,
    data=const.NONE_CONSTANT,
):
    response = const.NONE_CONSTANT

    if request_type == const.REQUEST_TYPE_GET:
        response = requests.get(url, headers=headers)

    elif request_type == const.REQUEST_TYPE_POST:
        response = requests.post(url, headers=headers, data=data)

    return response


# メッセージ画像生成
def insert_msg_to_img(
    div: str,
    img_file_name: str,
    font_type: str,
    font_size: int,
    xy_size: tuple[int, int],
    msg: str,
):
    img_file_path = get_file_path(img_file_name, const.FILE_TYPE_JPEG)

    img = Image.open(img_file_path).rotate(0)
    draw = ImageDraw.Draw(img)

    font_path = get_file_path(font_type, const.FILE_TYPE_TTC)
    font = ImageFont.truetype(font=font_path, size=font_size)

    draw.text(xy=xy_size, text=msg, fill="black", font=font, align="left")

    file_path = get_file_path(div, const.FILE_TYPE_JPEG, const.STR_OUTPUT)
    img.save(file_path, optimize=const.FLG_ON)
    return file_path
