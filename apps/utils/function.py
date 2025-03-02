# 説明：関数一覧

import glob
import json
import os
import random
import re
import socket
import sys
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
    if not env_val:
        env_val = const.SYM_BLANK
        if is_local_env:
            json_data = get_json_data(const.STR_ENV_VAR)
            env_val = json_data[var_name]
        else:
            print_error_msg(var_name, msg_const.MSG_ERR_ENV_VAR_NOT_EXIST)

    if env_val:
        env_val = get_decoding_masking_data(env_val)

    return env_val


# ローカルIPかチェック
def is_local_env() -> bool:
    ip_flg = const.FLG_OFF
    host = socket.gethostname()
    ip = socket.gethostbyname(host)

    if host == const.HOST_LOCAL and (const.IP_PRIVATE in ip or const.IP_LOCAL in ip):
        ip_flg = const.FLG_ON
    print_info_msg(const.STR_HOST, host)
    return ip_flg


# ホストIP取得
def get_host_port() -> tuple[str, int]:
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


# エラーメッセージ出力し、システム終了
def print_msg_exit(div: str, msg: str = const.SYM_BLANK):
    print_error_msg(div, msg)
    sys.exit()


# 文字列を日付型に変換
def convert_str_to_date(str: str, format: str) -> datetime:
    # func[strptime]:Convert String to Date
    date = datetime.strptime(str, format)
    return date


# 日付型を文字列に変換
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
def check_in_list(target_str: str, target_list: list[str]) -> bool:
    hit_flg = const.FLG_OFF
    for target in target_list:
        if target.upper() in target_str.upper():
            hit_flg = const.FLG_ON
            break

    return hit_flg


# ファイルパス取得
def get_file_path(div: str, file_type: str, file_div: str = const.STR_INPUT) -> str:
    file_path = f"{const.DIR_CURR_WORK}/{file_div}/{file_type}/{div}.{file_type}"
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
def read_file(file_path: str, file_encode: str = const.CHARSET_UTF_8) -> str:

    with open(file_path, mode=const.FILE_MODE_READ, encoding=file_encode) as f:
        if not check_path_exists(file_path):
            print_error_msg(file_path, msg_const.MSG_ERR_FILE_NOT_EXIST)

        # func[read]:Reading file
        data = f.read()
        return data


# ファイル書込
def write_file(file_path: str, contents, file_encode: str = const.CHARSET_UTF_8):
    try:
        with open(file_path, mode=const.FILE_MODE_WRITE, encoding=file_encode) as f:
            # func[write]:Writing file
            f.write(contents)

            # func[close]:Close file
            f.close()

    except Exception as e:
        print_error_msg(file_path, str(e))


# JSONデータ読み込み
def get_loads_json(data: str):
    # func[json.loads]:Read JSON file
    result = json.loads(data)
    return result


# JSONデータ書き込み
def get_dumps_json(data):
    json_data = json.dumps(data)
    result = json_data.encode(const.CHARSET_ASCII)
    return result


# JSONデータ取得
def get_json_data(app_div: str):
    file_path = get_file_path(app_div, const.FILE_TYPE_JSON)
    data = read_file(file_path)
    json_data = get_loads_json(data)
    return json_data


# 入力データ取得
def get_input_data(file_div: str, input_div: str):
    json_data = get_json_data(file_div)
    input_data = json_data[input_div]
    if file_div == const.STR_KEYWORD:
        input_data = input_data.split(const.SYM_COMMA)
    return input_data


# DataFrameからJSON出力
def df_to_json(div: str, df):
    # DataFrameをJSONファイルに出力
    file_path = get_file_path(div, const.FILE_TYPE_JSON, const.STR_OUTPUT)

    # データフレームをJSON文字列として取得
    json_data = df.to_json(orient="records", lines=const.FLG_OFF)

    # UTF-8エンコーディングでファイルに保存
    write_file(file_path, json_data)


# JSONからDataFrameデータ取得
def get_df_read_json(file_path: str):
    df = pd.read_json(file_path)
    return df


# JSONからDataFrameデータ取得
def get_df_from_json(div: str, file_div: str = const.STR_OUTPUT):
    # DataFrame初期化
    df = pd.DataFrame()

    file_path = get_file_path(div, const.FILE_TYPE_JSON, file_div)

    if check_path_exists(file_path):
        # func[read_json]:Read JSON file with Pandas
        df = get_df_read_json(file_path)
    else:
        print_error_msg(file_path, msg_const.MSG_ERR_FILE_NOT_EXIST)

    return df, file_path


# DataFrame取得
def get_df(data_list: list, columns: list[str]):
    # DataFrame作成
    df = pd.DataFrame(data_list, columns=columns)
    if df.empty:
        print_info_msg(msg_const.MSG_ERR_DATA_NOT_EXIST)
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
    decoding_info = get_input_data(const.STR_AUTH, const.STR_DECODE)
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
