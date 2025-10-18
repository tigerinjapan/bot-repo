# 説明: 関数一覧

import csv
import glob
import json
import os
import random
import re
import socket
import sys
import time
import urllib

from datetime import datetime, timedelta
import logging
from pprint import pprint
from translate import Translator

import pandas as pd

import apps.utils.constants as const
import apps.utils.message_constants as msg_const


# 現在時刻の取得
def get_now(div: int = const.DATE_NOW):
    now = datetime.now()
    if div == const.DATE_TODAY:
        now = now.strftime(const.DATE_FORMAT_YYYYMMDD)
    elif div == const.DATE_YEAR:
        now = now.year
    elif div == const.DATE_HOUR:
        now = now.hour
    elif div == const.DATE_WEEKDAY:
        now = now.weekday()
    return now


# 対象時刻より、計算された時刻の取得
def get_calc_date(val: int, div: int = const.DATE_DAY, calc_date: datetime = get_now()):
    if div == const.DATE_DAY:
        calc_date += timedelta(days=val)
    elif div == const.DATE_HOUR:
        calc_date += timedelta(hours=val)
    elif div == const.DATE_MIN:
        calc_date += timedelta(minutes=val)

    return calc_date


# ファイルパス名取得
def get_path_split(file_name: str, extension_flg: bool = const.FLG_OFF) -> str:
    idx = const.NUM_ONE if extension_flg else const.NUM_ZERO
    file_path_name = os.path.splitext(file_name)[idx]
    if extension_flg:
        file_path_name = file_path_name.replace(const.SYM_DOT, const.SYM_BLANK)
    return file_path_name


# アプリケーション名取得
def get_app_name(app_path: str, extension_flg: bool = const.FLG_OFF) -> str:
    file_name = os.path.basename(app_path)
    app_name = get_path_split(file_name, extension_flg)
    return app_name


# スクリプト名
SCRIPT_NAME = get_app_name(__file__)


# アプリケーションパス取得
def get_app_path(dir_path: str, file_path: str = const.SYM_BLANK) -> str:
    app_path = os.path.join(os.getcwd(), dir_path, file_path)
    return app_path


# パス存在チェック
def check_path_exists(file_path: str) -> bool:
    check_flg = const.FLG_OFF
    # func[exists]:Check if path exists
    if os.path.exists(file_path):
        check_flg = const.FLG_ON

    return check_flg


# 環境変数取得
def get_env_val(var_name: str, div: str = const.STR_SECRET_KEY) -> str:
    env_val = os.environ.get(var_name)
    if not env_val:
        env_val = const.SYM_BLANK
        if is_local_env():
            json_data = get_json_data(div)
            env_val = json_data[var_name]

    if env_val:
        if div == const.STR_SECRET_KEY:
            env_val = get_decoding_masking_data(env_val)
    else:
        curr_func_nm = sys._getframe().f_code.co_name
        print_error_msg(
            SCRIPT_NAME,
            curr_func_nm,
            var_name,
            msg_const.MSG_ERR_ENV_VAR_NOT_EXIST,
            sys_exit=const.FLG_ON,
        )

    return env_val


# ネットワーク接続チェック
def is_network() -> bool:
    network_flg = const.FLG_OFF
    curr_func_nm = sys._getframe().f_code.co_name

    try:
        response = urllib.request.urlopen(const.URL_GOOGLE)
        network_flg = const.FLG_ON
        # print_debug_msg(curr_func_nm, response)
    except Exception as e:
        print_error_msg(SCRIPT_NAME, curr_func_nm, const.STR_REQUEST, str(e))
    return network_flg


# サーバーURL取得
def get_server_url() -> str:
    server_url = "https://" + get_env_val("URL_KOYEB")
    if is_local_env():
        server_url = get_local_url()
    return server_url


# ローカルIPかチェック
def is_local_env() -> bool:
    local_flg = const.FLG_OFF

    try:
        host = socket.gethostname()
        ip = socket.gethostbyname(host)

        if host == const.HOST_LOCAL and (
            const.IP_PRIVATE in ip or const.IP_LOCAL in ip
        ):
            local_flg = const.FLG_ON

    except socket.gaierror as sge:
        curr_func_nm = sys._getframe().f_code.co_name
        print_error_msg(SCRIPT_NAME, curr_func_nm, const.STR_IP, str(sge))

    return local_flg


# ホストIP取得
def get_host_port() -> tuple[str, int]:
    host = const.IP_DEFAULT
    port = const.PORT_DEFAULT

    if is_local_env():
        host = const.IP_LOCAL
        port = const.PORT_NUM

    return host, port


# ローカルURL取得
def get_local_url() -> str:
    host, port = get_host_port()
    local_url = f"http://{host}:{port}"
    return local_url


# 休日チェック
def is_holiday(weekend_flg: bool = const.FLG_ON) -> bool:
    holiday_flg = const.FLG_OFF

    holiday_data = get_input_data(const.STR_HOLIDAY)
    holiday_list = [holiday[const.STR_DATE] for holiday in holiday_data]

    if get_now(const.DATE_TODAY) in holiday_list:
        holiday_flg = const.FLG_ON

    if weekend_flg:
        if get_now(const.DATE_WEEKDAY) >= 5:
            holiday_flg = const.FLG_ON

    return holiday_flg


# 開始メッセージ出力
def print_start(div: str, msg: str = msg_const.MSG_INFO_PROC_START):
    print_info_msg(div, msg)


# 終了メッセージ出力
def print_end(div: str, msg: str = msg_const.MSG_INFO_PROC_END):
    print_info_msg(div, msg)


# 情報メッセージ出力
def print_info_msg(div: str, msg: str):
    print_msg(div, msg)


# デバックメッセージ出力
def print_debug_msg(div: str, msg: str):
    print_msg(div, msg, const.STR_DEBUG)


# メッセージ出力
def print_msg(div: str, msg: str, log_div: str = const.STR_INFO):
    log_msg = f"{div} {msg}"
    write_log(log_msg, log_div)


# エラーメッセージ出力
def print_error_msg(
    script_name: str,
    func_name: str,
    div: str,
    exception=const.NONE_CONSTANT,
    sys_exit: bool = const.FLG_OFF,
):
    log_msg = f"[{script_name}.{func_name}] {div}"

    if exception:
        except_msg = f" {str(exception)}"
        log_msg += except_msg

        if const.MAX_TEXT_LENGTH < len(log_msg):
            log_msg = f"{log_msg[:const.MAX_TEXT_LENGTH]}..."

    write_log(log_msg)

    if sys_exit:
        sys.exit()


# ログ出力
def write_log(log_msg: str, log_div: str = const.STR_ERROR):
    log_level = logging.ERROR
    if log_div == const.STR_INFO:
        log_level = logging.INFO
    elif log_div == const.STR_DEBUG:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logger = logging.getLogger(log_div)
    logger.setLevel(log_level)
    logger.propagate = const.FLG_OFF

    # log_format = "%(asctime)s %(name)s:%(lineno)s %(funcName)s [%(levelname)s]: %(message)s"
    log_format = "%(asctime)s [%(levelname)s] %(message)s"
    formatter = logging.Formatter(log_format)

    # コンソール出力設定
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(formatter)

    # ファイル出力設定
    log_path = get_file_path(
        log_div, file_type=const.FILE_TYPE_LOG, file_div=const.STR_OUTPUT
    )
    file_handler = logging.FileHandler(log_path, encoding=const.CHARSET_UTF_8)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    if not is_local_env():
        logger.addHandler(file_handler)

    msg = get_replace_data(log_msg, const.LIST_LOG_MASKING, const.LOG_MASKING)

    if log_level == logging.DEBUG:
        logger.debug(msg)
    elif log_level == logging.ERROR:
        logger.error(msg)
    else:
        logger.info(msg)

    # 登録されているハンドラーをリストで取得
    handlers = logger.handlers[:]

    # ハンドラーを一つずつ削除
    for handler in handlers:
        logger.removeHandler(handler)


# 文字列を日付型に変換
def convert_str_to_date(str: str, format: str = const.DATE_FORMAT_ISO) -> datetime:
    if format == const.DATE_FORMAT_ISO:
        date = datetime.fromisoformat(str)
    else:
        # func[strptime]:Convert String to Date
        date = datetime.strptime(str, format)
    return date


# 日付型を文字列に変換
def convert_date_to_str(date: datetime, format: str) -> str:
    # func[strftime]:Convert Date to String
    date_format = date.strftime(format)
    return date_format


# 日付フォーマット変換
def convert_date_format(
    str: str, new_format: str, old_format: str = const.DATE_FORMAT_ISO
) -> str:
    date = convert_str_to_date(str, old_format)
    date_format = convert_date_to_str(date, new_format)
    return date_format


# タイムスリップ
def time_sleep(secs: int = 3):
    # func[sleep]:time sleep
    time.sleep(secs)


# 乱数生成
def get_random_int(end_num: int, start_num: int = const.NUM_ZERO) -> int:
    if start_num == const.NUM_ZERO:
        rand_int = random.randrange(end_num)
    else:
        rand_int = random.randint(start_num, end_num)
    return rand_int


# 乱数生成
def get_random_choice(number_list: list[int]) -> int:
    rand_int = random.choice(number_list)
    return rand_int


# 対象文字列がリストの文字列を含まれているかチェック
def check_in_list(target_str: str, target_list: list[str]) -> bool:
    hit_flg = const.FLG_OFF
    for target in target_list:
        if target.upper() in target_str.upper():
            hit_flg = const.FLG_ON
            break

    return hit_flg


# ファイルパス取得
def get_file_path(div: str, file_type: str, file_div: str = const.STR_INPUT) -> str:
    file_path = f"{os.getcwd()}/{file_div}/{file_type}/{div}.{file_type}"
    return file_path


# ファイル名リスト取得
def get_file_name_list(
    file_type: str, file_div: str = const.STR_INPUT, extension_flg: bool = const.FLG_OFF
):
    folder_path = f"{os.getcwd()}/{file_div}/{file_type}"

    # os.listdir()でフォルダ内のすべての項目名を取得
    items = os.listdir(folder_path)

    # 項目がファイルであるか確認し、ファイル名のみをリストに追加
    file_name_list = []
    for item in items:
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            file_name_list.append(item)

    if not extension_flg:
        file_name_list = [
            file_name.split(const.SYM_DOT)[0] for file_name in file_name_list
        ]

    return file_name_list


# ファイル削除
def remove_old_file(dir_path: str, div: str):
    # func[glob]:Get a list of files that meet the conditions
    file_path_list = glob.glob(f"{dir_path}/{get_now(const.DATE_YEAR)}*_{div}")

    for file_path in file_path_list:
        if get_now(const.DATE_TODAY) in file_path:
            continue
        else:
            # func[remove]:Delete a file or directory
            os.remove(file_path)


# ファイル読込
def read_file(file_path: str, file_encode: str = const.CHARSET_UTF_8) -> str:

    try:
        with open(file_path, mode=const.FILE_MODE_READ, encoding=file_encode) as f:
            # func[read]:Reading file
            data = f.read()

    except Exception as e:
        curr_func_nm = sys._getframe().f_code.co_name
        print_error_msg(
            SCRIPT_NAME, curr_func_nm, msg_const.MSG_ERR_FILE_NOT_EXIST, str(e)
        )
        data = const.NONE_CONSTANT

    return data


# ファイル書込
def write_file(file_path: str, data, file_encode: str = const.CHARSET_UTF_8):
    file_ext = get_path_split(file_path, extension_flg=const.FLG_ON)

    try:
        with open(file_path, mode=const.FILE_MODE_WRITE, encoding=file_encode) as f:
            if is_local_env() and file_ext == const.FILE_TYPE_JSON:
                json.dump(data, f, ensure_ascii=const.FLG_OFF, indent=4)
            else:
                # func[write]:Writing file
                f.write(data)

            # func[close]:Close file
            f.close()

    except Exception as e:
        curr_func_nm = sys._getframe().f_code.co_name
        print_error_msg(SCRIPT_NAME, curr_func_nm, file_path, str(e))


# CSVファイルを読み込み
def get_dict_from_csv(file_path: str, search_key: str = const.SYM_BLANK):
    # データを格納する辞書
    data_dict = {}

    with open(file_path, newline="", encoding=const.CHARSET_UTF_8) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if search_key:
                for row_data in row:
                    search_value = row_data.strip()
                    if search_key == search_value:
                        return row

            else:
                # 1番目の値をキーとして使用
                key = row[0]
                # 全体の行を値として格納
                data_dict[key] = row

        return data_dict


# JSONデータ読み込み
def get_loads_json(data: str):
    # func[json.loads]:Read JSON file
    result = json.loads(data)
    return result


# JSONデータ書き込み
def get_dumps_json(data, indent: int = 2, ensure_ascii: bool = const.FLG_OFF):
    json_data = json.dumps(data, indent=indent, ensure_ascii=ensure_ascii)
    if ensure_ascii:
        result = json_data.encode(const.CHARSET_ASCII)
    else:
        result = json_data
    return result


# JSONデータ取得
def get_json_data(div: str, file_div: str = const.STR_INPUT):
    file_path = get_file_path(div, const.FILE_TYPE_JSON, file_div)
    json_data = read_file(file_path)
    if json_data:
        json_data = get_loads_json(json_data)
    return json_data


# 入力データ取得
def get_input_data(div: str, input_div: str = const.STR_ITEM):
    json_data = get_json_data(div)
    input_data = json_data[input_div]
    if div == const.STR_KEYWORD:
        input_data = input_data.split(const.SYM_COMMA)
    return input_data


# DataFrame初期化
def init_df():
    df = pd.DataFrame()
    return df


# DataFrameからJSON出力
def df_to_json(
    div: str, df, file_div: str = const.STR_OUTPUT, dict_flg: bool = const.FLG_OFF
):
    # DataFrameをJSONファイルに出力
    file_path = get_file_path(div, const.FILE_TYPE_JSON, file_div)

    if dict_flg or is_local_env():
        # DataFrameをリスト形式の辞書に変換
        data = df.to_dict(orient="records")
    else:
        data = df.to_json(orient="records", lines=const.FLG_OFF)

    # JSONファイルに書き込む
    write_file(file_path, data)


# JSONからDataFrameデータ取得
def get_df_read_json(file_path: str):
    df = pd.read_json(file_path)
    return df


# CSVからDataFrameデータ取得
def get_df_read_csv(file_path: str):
    df = pd.read_csv(file_path)
    return df


# JSONからDataFrameデータ取得
def get_df_from_json(div: str, file_div: str = const.STR_OUTPUT):
    df, file_path = get_df_from_file_path(div, file_div, file_type=const.FILE_TYPE_JSON)
    return df, file_path


# CSVからDataFrameデータ取得
def get_df_from_csv(div: str, file_div=const.STR_INPUT):
    df, file_path = get_df_from_file_path(div, file_div, file_type=const.FILE_TYPE_CSV)
    return df, file_path


# JSONからDataFrameデータ取得
def get_df_from_file_path(div: str, file_div, file_type):
    # DataFrame初期化
    df = init_df()

    file_path = get_file_path(div, file_type, file_div)

    if check_path_exists(file_path):
        if file_type == const.FILE_TYPE_JSON:
            # func[read_json]:Read JSON file with Pandas
            df = get_df_read_json(file_path)

        elif file_type == const.FILE_TYPE_CSV:
            if div == const.STR_ZIP_CODE:
                # func[read_csv]:Read CSV file with Pandas
                df = pd.read_csv(file_path, dtype={div: str})
            else:
                df = get_df_read_csv(file_path)
    else:
        curr_func_nm = sys._getframe().f_code.co_name
        print_error_msg(
            SCRIPT_NAME, curr_func_nm, file_path, msg_const.MSG_ERR_FILE_NOT_EXIST
        )

    return df, file_path


# DataFrame取得
def get_df(data, columns: list[str] = const.NONE_CONSTANT):
    # DataFrame作成
    df = pd.DataFrame(data, columns=columns)
    return df


# リンクタグ取得
def get_a_tag(url: str, text: str, alert_flg: bool = const.FLG_OFF):
    a_attr = '" target="_blank" rel="noopener noreferrer">'
    if alert_flg:
        a_attr = '" onclick="' + f"alert('{msg_const.MSG_INFO_PROC_COMPLETED}');" + '">'

    result = '<a href="' + url + a_attr + text + "</a>"
    return result


# ボタンタグ取得
def get_dialog_button(title: str, contents: str, text: str):
    result = (
        '<button id="btn'
        + title
        + '" class="spot-link" onclick="'
        + "openDialog('"
        + title
        + "', '"
        + contents
        + "')"
        + '">'
        + text
        + "</button>"
    )
    return result


# イメージ文字列取得
def get_img_tag(
    img_path: str, file_name: str = const.SYM_BLANK, text: str = const.SYM_BLANK
):
    result = '<img src="' + img_path + file_name + text + '"</img>'
    return result


# リストの重複削除
def remove_duplicates(val_list):
    is_1d = all(not isinstance(i, list) for i in val_list)

    if is_1d:
        unique_list = list(dict.fromkeys(val_list))
    else:
        # 各サブリストをタプルに変換してセットに追加
        unique_set = {tuple(sub_list) for sub_list in val_list}
        # セットをリストに戻す
        unique_list = [list(tup) for tup in unique_set]
    return unique_list


# 文字列置換
def get_replace_data(
    data_str: str,
    target_list: list[str] = const.LIST_REPLACE,
    replace_str: str = const.SYM_BLANK,
) -> str:
    replace_data = convert_half_char(data_str)
    for target in target_list:
        replace_data = replace_data.replace(target, replace_str)
    return replace_data


# マスキングデータ取得
def get_masking_data(target: str):
    result = get_decoding_masking_data(target, encode_flg=const.FLG_ON)
    return result


# マスキングデータ復号
def get_decoding_masking_data(target: str, encode_flg: bool = const.FLG_OFF):
    decoding_info = get_input_data(const.STR_AUTH, const.STR_DECODE)
    masking_list = const.LIST_MASKING
    decoding_list = list(decoding_info.values()) + [str(get_now(const.DATE_YEAR))]

    if encode_flg:
        masking_list = decoding_list
        decoding_list = const.LIST_MASKING

    for before_str, after_str in zip(masking_list, decoding_list):
        target = target.replace(before_str, after_str)
    return target


# [正規表現] 文字列の検索
def re_search(pattern: str, target: str) -> str:
    result = const.SYM_BLANK

    # 文字列内でパターンを検索
    match = re.search(pattern, target)
    if match:
        # マッチした文字列を返却
        result = match.group(0)

    return result


# [正規表現] 文字列の区切り
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


# 文字列変換
def convert_upper_lower(before_str: str, div: str = const.STR_UPPER) -> str:
    after_str = before_str
    if div == const.STR_UPPER:
        after_str = before_str.upper()
    elif div == const.STR_LOWER:
        after_str = before_str.lower()
    elif div == const.STR_CAPITALIZE:
        after_str = before_str.capitalize()

    return after_str


# 翻訳文の取得
def get_translated_text(
    target_text: str, from_lang: str = const.LANG_CD_JA, to_lang: str = const.LANG_CD_EN
) -> str:
    # デフォルト：日本語から英語への翻訳
    translator = Translator(from_lang=from_lang, to_lang=to_lang)

    # 翻訳
    translated_text = translator.translate(target_text)
    return translated_text


# テストデータ出力
def print_test_data(data, type_flg: bool = const.FLG_OFF):
    if type_flg:
        type_name = type(data).__name__
        print_info_msg(const.STR_TYPE_JA, type_name)
    pprint(data)


if __name__ == const.MAIN_FUNCTION:
    print(is_holiday())
