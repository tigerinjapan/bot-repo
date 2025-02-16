# 説明：関数一覧

import glob
import json
import os
import random
import socket
import textwrap
import time
from datetime import datetime

import constants as const
import message_constants as msg_const


# アプリケーション名取得
def get_app_nm(app_path: str) -> str:
    app_nm = os.path.basename(app_path)
    return app_nm


# 現在パス取得
def get_current_dir() -> str:
    current_dir = os.getcwd()
    return current_dir


# 環境変数取得
def get_env_val(var_name: str, div: str = const.STR_LINE) -> str:
    env_val = os.environ.get(var_name)
    if not env_val:
        print_error_msg(var_name, msg_const.MSG_ERR_ENV_VAR_NOT_EXIST)

        if check_local_ip():
            auth_data = get_auth_data(div)

            if const.STR_ID in var_name.lower():
                key = const.STR_ID
            elif const.STR_TIME in var_name.lower():
                key = const.STR_TIME
            else:
                key = const.STR_KEY

            env_val = auth_data[key]

    env_val = get_decoding_masking_data(env_val)
    return env_val


# ローカルIPかチェック
def check_local_ip():
    ip_flg = const.FLG_OFF
    host = socket.gethostname()
    ip = socket.gethostbyname(host)

    if const.IP_PRIVATE in ip:
        ip_flg = const.FLG_ON
    return ip_flg


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


# 文字列折り返し
def get_wrap_text(target_str: str, wrap_width: int) -> str:
    wrap_text_list = textwrap.wrap(target_str, wrap_width)
    wrap_text = const.SYM_NEW_LINE.join(wrap_text_list)
    return wrap_text


# マスキングデータ復号
def get_decoding_masking_data(target: str):
    decoding_info = get_auth_data(const.STR_USER)
    masking_list = const.LIST_MASKING
    decoding_list = list(decoding_info.values()) + [str(const.DATE_YEAR)]

    for masking_str, decode_str in zip(masking_list, decoding_list):
        target = target.replace(masking_str, decode_str)
    return target
