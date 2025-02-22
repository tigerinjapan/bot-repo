# 説明：API関数

import json

import requests
from PIL import Image, ImageDraw, ImageFont

import apps.utils.constants as const
from apps.utils.function import remove_old_file


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


# JSONデータ読み込み
def get_loads_json(data):
    result = json.loads(data)
    return result


# JSONデータ書き込み
def get_dumps_json(data):
    result = json.dumps(data)
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
    workspace_path = const.DIR_CURR_WORK
    input_path = f"{workspace_path}/{const.STR_INPUT}"
    img_dir_path = f"{input_path}/{const.STR_IMG}"
    img_file_path = f"{img_dir_path}/{img_file_name}.{const.FILE_TYPE_JPEG}"

    img = Image.open(img_file_path).rotate(0)
    draw = ImageDraw.Draw(img)

    font_path = f"{input_path}/{font_type}"
    font = ImageFont.truetype(font=font_path, size=font_size)

    draw.text(xy=xy_size, text=msg, fill="black", font=font, align="left")

    output_path = f"{workspace_path}/{const.STR_OUTPUT}/{const.STR_IMG}"
    remove_old_file(output_path, div)
    file_path = f"{output_path}/{const.DATE_TODAY}_{div}.{const.FILE_TYPE_JPEG}"
    img.save(file_path, optimize=const.FLG_ON)
    return file_path
