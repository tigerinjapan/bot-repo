# 説明：関数一覧

import glob
import json
import os
import random
import re
import socket
import time
from datetime import datetime

import pandas as pd

import apps.utils.constants as const
import apps.utils.message_constants as msg_const


# アプリケーション名取得
def get_app_name(app_path: str, extension_flg: bool = const.FLG_OFF) -> str:
    file_name = os.path.basename(app_path)
    app_name = get_path_split(file_name, extension_flg)
    return app_name


# アプリケーションパス取得
def get_app_path(dir_path: str, file_path: str = const.SYM_BLANK) -> str:
    app_path = os.path.join(const.DIR_CURR_WORK, dir_path, file_path)
    return app_path


# パス存在チェック
def check_path_exists(file_path: str) -> bool:
    check_flg = const.FLG_OFF
    # func[exists]:Check if path exists
    if os.path.exists(file_path):
        check_flg = const.FLG_ON

    return check_flg


# ファイルパス名取得
def get_path_split(file_name: str, extension_flg: bool = const.FLG_OFF) -> str:
    idx = const.NUM_ONE if extension_flg else const.NUM_ZERO
    file_path_name = os.path.splitext(file_name)[idx]
    if extension_flg:
        file_path_name = file_path_name.replace(const.SYM_DOT, const.SYM_BLANK)
    return file_path_name


# 環境変数取得
def get_env_val(var_name: str) -> str:
    env_val = os.environ.get(var_name)
    if env_val:
        env_val = get_decoding_masking_data(env_val)
    else:
        print_error_msg(var_name, msg_const.MSG_ERR_ENV_VAR_NOT_EXIST)
    return env_val


# ローカルIPかチェック
def is_local_env():
    ip_flg = const.FLG_OFF
    host = socket.gethostname()
    ip = socket.gethostbyname(host)

    if host == const.HOST_LOCAL and (const.IP_PRIVATE in ip or const.IP_LOCAL in ip):
        ip_flg = const.FLG_ON
    print_info_msg([const.STR_HOST, host], [const.STR_IP, ip])
    return ip_flg


# ホストIP取得
def get_host_port() -> tuple[str, str]:
    host = const.IP_DEFAULT
    port = const.PORT_DEFAULT

    if is_local_env():
        host = const.IP_LOCAL
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


def convert_str_to_date(str: str, format: str) -> datetime:
    # func[strptime]:Convert String to Date
    date = datetime.strptime(str, format)
    return date


def convert_date_to_str(date: datetime, format: str) -> str:
    # func[strftime]:Convert Date to String
    date_format = date.strftime(format)
    return date_format


def convert_date_format(str: str, old_format: str, new_format: str) -> str:
    # func[strptime]:Convert Date to String
    date = convert_str_to_date(str, old_format)
    date_format = convert_date_to_str(date, new_format)
    return date_format


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
def get_file_path(div: str, file_type: str, file_div: str = const.STR_INPUT) -> str:
    file_path = f"{file_div}/{file_type}/{div}.{file_type}"
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
    data = open_file(file_path)
    return data


# ファイル書込
def write_file(file_path: str, contents):
    open_file(file_path, file_mode=const.FILE_MODE_WRITE, contents=contents)


# ファイルオープン
def open_file(
    file_path: str,
    file_mode: str = const.FILE_MODE_READ,
    contents=const.NONE_CONSTANT,
    file_encode: str = const.CHARSET_UTF_8,
):
    try:
        # func[open]:Open file
        file_open = open(file_path, mode=file_mode, encoding=file_encode)
        if file_mode == const.FILE_MODE_READ:
            if not check_path_exists(file_path):
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
        print_error_msg(file_path, e)
        return const.FLG_OFF
    else:
        if file_mode == const.FILE_MODE_READ:
            return data


# 権限データ取得
def get_auth_data(auth_div: str = const.NONE_CONSTANT):
    json_data = get_json_data(const.STR_AUTH)
    if auth_div:
        auth_data = json_data[auth_div]
    else:
        auth_data = json_data
    return auth_data


# JSONデータ取得
def get_json_data(app_div: str):
    file_path = get_file_path(app_div, const.FILE_TYPE_JSON)
    data = read_file(file_path)
    json_data = object_to_json(data)
    return json_data


# JSONデータ読込
def object_to_json(data):
    # func[json.loads]:Read JSON file
    response_json = json.loads(data)
    return response_json


# DataFrameからJSON出力
def df_to_json(div: str, df):
    # DataFrameをJSONファイルに出力
    file_path = get_file_path(div, const.FILE_TYPE_JSON, const.STR_OUTPUT)

    # データフレームをJSON文字列として取得
    json_data = df.to_json(orient="records", lines=const.FLG_ON)

    # UTF-8エンコーディングでファイルに保存
    write_file(file_path, json_data)


# JSONからDataFrameデータ取得
def get_df_from_json(div: str, file_div: str = const.STR_OUTPUT):
    df = get_df()
    file_path = get_file_path(div, const.FILE_TYPE_JSON, file_div)

    if check_path_exists(file_path):
        # func[read_json]:Read JSON file with Pandas
        df = pd.read_json(file_path)
    else:
        print_info_msg(file_path, msg_const.MSG_ERR_FILE_NOT_EXIST)

    return df


# DataFrame取得
def get_df(
    data_list: list = const.NONE_CONSTANT, columns: list[str] = const.NONE_CONSTANT
):
    if data_list:
        # DataFrame作成
        df = pd.DataFrame(data_list, columns=columns)
        if df.empty:
            print_info_msg(msg_const.MSG_ERR_DATA_NOT_EXIST)
    else:
        # DataFrame初期化
        df = pd.DataFrame()

    return df


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


if __name__ == const.MAIN_FUNCTION:
    print(is_local_env())
