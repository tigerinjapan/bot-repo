# 説明：関数一覧

import glob
import json
import os
import random
import re
import socket
import time
from datetime import datetime

import utils.constants as const
import utils.message_constants as msg_const


# アプリケーション名取得
def get_app_name(app_path: str, extension_flg: bool = const.FLG_OFF) -> str:
    file_name = os.path.basename(app_path)
    app_name = get_path_split(file_name, extension_flg)
    return app_name


# ファイルパス名取得
def get_path_split(file_name: str, extension_flg: bool = const.FLG_OFF) -> str:
    idx = const.NUM_ONE if extension_flg else const.NUM_ZERO
    file_path_name = os.path.splitext(file_name)[idx]
    if extension_flg:
        file_path_name = file_path_name.replace(const.SYM_DOT, const.SYM_BLANK)
    return file_path_name


# 現在パス取得
def get_current_dir() -> str:
    current_dir = os.getcwd()
    return current_dir


# 環境変数取得
def get_env_val(var_name: str) -> str:
    env_val = os.environ.get(var_name)
    if env_val:
        env_val = get_decoding_masking_data(env_val)
    else:
        print_error_msg(var_name, msg_const.MSG_ERR_ENV_VAR_NOT_EXIST)
    return env_val


# ローカルIPかチェック
def check_local_ip():
    ip_flg = const.FLG_OFF
    host = socket.gethostname()
    ip = socket.gethostbyname(host)

    if const.IP_PRIVATE in ip:
        ip_flg = const.FLG_ON
    return ip_flg


# ホストIP取得
def get_host_port() -> tuple[str, str]:
    host = const.IP_DEFAULT
    port = const.PORT_DEFAULT

    if check_local_ip():
        host = const.IP_LOCAL_HOST
        port = const.PORT_NUM

    return host, port


# 処理開始メッセージ出力
def print_start(app_div: str):
    print_info_msg(app_div, msg_const.MSG_INFO_PROC_START)


# 処理終了メッセージ出力
def print_end(app_div: str):
    print_info_msg(app_div, msg_const.MSG_INFO_PROC_END)


# 情報メッセージ出力
def print_info_msg(div: str, msg: str = const.SYM_BLANK):
    msg_now = f"[{datetime.now()}]"
    print(msg_now, msg_const.MSG_DIV_INFO, div, msg)


# エラーメッセージ出力
def print_error_msg(div: str, msg: str = const.SYM_BLANK):
    msg_now = f"[{datetime.now()}]"
    print(msg_now, msg_const.MSG_DIV_ERR, div, msg)


# タイムスリップ
def time_sleep(secs: int = 3):
    # func[sleep]:time sleep
    time.sleep(secs)


# 乱数生成
def get_random_int(end_num: int) -> int:
    rand_int = random.randint(1, end_num)
    return rand_int


# 対象文字列がリストに含まれているかチェック
def check_in_list(
    target_str: str, target_list: list[str], check_flg: bool = const.FLG_ON
):
    hit_flg = const.FLG_OFF
    hit_target = const.NONE_CONSTANT
    for target in target_list:
        if target.upper() in target_str.upper():
            hit_flg = const.FLG_ON
            hit_target = target
            break

    if check_flg:
        return hit_flg
    else:
        return hit_target


# ファイルパス取得
def get_file_path(app_div: str, file_type: str, file_div: str = const.STR_INPUT) -> str:
    file_path = f"{file_div}/{app_div}"
    if file_div == const.STR_OUTPUT:
        file_path += f"_{const.DATE_NOW}"
    file_path += f".{file_type}"
    return file_path


# ファイル削除
def remove_old_file(dir_path: str, div: str):
    # func[glob]:Get a list of files that meet the conditions
    file_path_list = glob.glob(f"{dir_path}/{const.DATE_YEAR_MONTH}*_{div}")

    for file_path in file_path_list:
        if const.DATE_TODAY in file_path:
            continue
        else:
            # func[remove]:Delete a file or directory
            os.remove(file_path)


# ファイル読込
def read_file(file_path: str):
    data = open_file(
        file_path, const.FILE_MODE_READ, const.CHARSET_UTF_8, const.NONE_CONSTANT
    )
    return data


# ファイルオープン
def open_file(file_path: str, file_mode: str, file_encode: str, contents):
    try:
        # func[open]:Open file
        file_open = open(file_path, mode=file_mode, encoding=file_encode)
        if file_mode == const.FILE_MODE_READ:
            # func[exists]:Check if path exists
            if not (os.path.exists(file_path)):
                exception_msg = msg_const.MSG_ERR_FILE_NOT_EXIST
                raise Exception(exception_msg)
            # func[read]:Reading file
            data = file_open.read()
        elif file_mode == const.FILE_MODE_WRITE:
            # func[write]:Writing file
            file_open.write(contents)
        # func[close]:Close file
        file_open.close()
    except Exception as e:
        print_error_msg(e, file_path)
        return const.FLG_OFF
    else:
        if file_mode == const.FILE_MODE_READ:
            return data


# 権限データ取得
def get_auth_data(app_div: str = const.NONE_CONSTANT):
    file_path = get_file_path(const.STR_AUTH, const.FILE_TYPE_JSON)
    data = read_file(file_path)
    json_load = object_to_json(data)
    if app_div:
        json_data = json_load[app_div]
    else:
        json_data = json_load
    return json_data


# JSONデータ読込
def object_to_json(data):
    # func[json.loads]:Read JSON file
    response_json = json.loads(data)
    return response_json


# 文字列置換
def get_replace_data(data_str: str) -> str:
    replace_data = data_str
    for target in const.LIST_REPLACE:
        replace_data = replace_data.replace(target, const.SYM_BLANK)
    return replace_data


# マスキングデータ取得
def get_masking_data(target: str):
    result = get_decoding_masking_data(target, encode_flg=const.FLG_ON)
    return result


# マスキングデータ復号
def get_decoding_masking_data(target: str, encode_flg: bool = const.FLG_OFF):
    decoding_info = get_auth_data(const.STR_DECODE)
    masking_list = const.LIST_MASKING
    decoding_list = list(decoding_info.values()) + [str(const.DATE_YEAR)]

    if encode_flg:
        masking_list = decoding_list
        decoding_list = const.LIST_MASKING

    for before_str, after_str in zip(masking_list, decoding_list):
        target = target.replace(before_str, after_str)
    return target


# 文字列の区切り
def re_split(pattern: str, target: str) -> list[str]:
    result = re.split(pattern, target)
    return result


# 全角英数字を半角英数字に変換
def convert_half_char(target: str) -> str:
    full_width_char = const.SYM_BLANK.join(chr(0xFF01 + i) for i in range(94))
    half_width_char = const.SYM_BLANK.join(chr(0x21 + i) for i in range(94))

    full_width_to_half_width = str.maketrans(full_width_char, half_width_char)

    result = target.translate(full_width_to_half_width)
    return result
