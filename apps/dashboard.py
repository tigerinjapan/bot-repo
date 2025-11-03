# 説明: ダッシュボード

import pandas as pd
from dateutil.relativedelta import relativedelta
from fastapi import Request
from user_agents import parse

import apps.utils.constants as const
import apps.utils.log_dao as log_dao
import apps.utils.log_dto as log_dto
import apps.utils.function as func
import apps.utils.function_api as func_api
import apps.utils.message_constants as msg_const

# スクリプト名
SCRIPT_NAME = func.get_app_name(__file__)

# カラム
COL_LIST_DASHBOARD = [
    const.STR_DATE,
    const.STR_TIME,
    const.STR_LEVEL,
    const.STR_APP,
    const.STR_CATEGORY,
    const.STR_DEVICE,
    const.STR_OS,
    const.STR_BROWSER,
]

# リスト
LIST_DATE = [const.STR_DAY, const.STR_MONTH, const.STR_YEAR]

# デフォルト値
DEFAULT_VALUE = "Unknown"


# データ更新
def update_data():
    func.print_start(SCRIPT_NAME)

    data_list = get_data_list(const.APP_DASHBOARD)
    if data_list:
        df = func.get_df(data_list, COL_LIST_DASHBOARD)
        dummy_data = func.get_json_data(const.APP_DASHBOARD, const.STR_OUTPUT)

        json_data = {}
        for date_div in LIST_DATE:
            dashboard_json = get_dashboard_json(df, date_div)

            if date_div == const.STR_DAY:
                dummy_json = dummy_data[date_div]
                if dashboard_json == dummy_json:
                    break

            json_data[date_div] = dashboard_json

        if json_data:
            file_path = func.get_file_path(
                SCRIPT_NAME, file_type=const.FILE_TYPE_JSON, file_div=const.STR_OUTPUT
            )
            func.write_file(file_path, json_data)
        else:
            func.print_info_msg(SCRIPT_NAME, msg_const.MSG_INFO_DATA_NOT_EXIST)

    else:
        func.print_info_msg(SCRIPT_NAME, msg_const.MSG_ERR_DATA_NOT_EXIST)

    func.print_end(SCRIPT_NAME)


# データリスト取得
def get_data_list(log_div: str, backup_flg: bool = const.FLG_OFF):
    data_list = []
    backup_log_list = []

    try:
        log_path = func.get_file_path(
            log_div,
            file_type=const.FILE_TYPE_LOG,
            file_div=const.STR_OUTPUT,
        )

        log_data_text = func.read_file(log_path)
        if log_data_text:
            log_data_list = log_data_text.split(const.SYM_NEW_LINE)

            if not backup_flg:
                target_date = get_target_date(const.STR_YEAR)[0]
                log_backup_list = log_dao.get_log_data_list(log_div, target_date)
                log_data_list.extend(log_backup_list)

            for log_data in log_data_list:
                data = log_data.split(const.SYM_SPACE)
                if log_div == const.APP_DASHBOARD:
                    data = data[: len(COL_LIST_DASHBOARD)]

                if not data[0]:
                    continue

                if backup_flg:
                    cutoff_date = func.get_calc_date(-1)
                    log_datetime = func.convert_str_to_date(
                        data[0], const.DATE_FORMAT_YYYYMMDD_DASH
                    )
                    # 1日以前のログか判定
                    if log_datetime <= cutoff_date:
                        log_backup = [log_div, log_data, log_datetime]
                        json_data = log_dto.get_insert_data_for_log(log_backup)
                        backup_log_list.append(json_data)
                    else:
                        data_list.append(log_data)

                else:
                    data_list.append(data)

            if backup_flg and backup_log_list:
                # DB登録
                log_dao.insert_log_data(backup_log_list)

                # ログファイル：本日分以外削除
                log_data = const.SYM_NEW_LINE.join(data_list) + const.SYM_NEW_LINE
                func.write_file(log_path, log_data)

        if not data_list:
            func.print_info_msg(SCRIPT_NAME, msg_const.MSG_ERR_DATA_NOT_EXIST)

    except Exception as e:
        func.print_info_msg(SCRIPT_NAME, e)

    return data_list


# ログバックアップ
def backup_log(log_div: str = const.APP_DASHBOARD):
    div = f"{const.STR_BACKUP} {log_div}"
    func.print_start(div)

    get_data_list(log_div, backup_flg=const.FLG_ON)

    func.print_end(div)


# ダッシュボードデータ取得
def get_dashboard_json(df_all, date_div: str):
    target_date, date_format = get_target_date(date_div)

    df_all[const.STR_DATE] = pd.to_datetime(df_all[const.STR_DATE])
    df = df_all[target_date <= df_all[const.STR_DATE]]

    df[const.STR_DATE] = df[const.STR_DATE].dt.strftime(date_format)

    term_access = df[const.STR_DATE].value_counts().sort_index()
    total_access = term_access.sum()
    category_counts = df[const.STR_CATEGORY].value_counts()
    app_counts = df[const.STR_APP].value_counts()
    device_counts = df[const.STR_DEVICE].value_counts()
    os_counts = df[const.STR_OS].value_counts()
    browser_counts = df[const.STR_BROWSER].value_counts()

    # JSON形式のデータを作成
    dashboard_json = {
        "label": date_div,
        "users": {
            "total": f"{total_access:,}",
            "labels": term_access.index.tolist(),
            "data": term_access.values.tolist(),
        },
        const.STR_CATEGORY: {
            "labels": category_counts.index.tolist(),
            "data": category_counts.values.tolist(),
        },
        const.STR_APP: calculate_percentage_to_100(app_counts),
        const.STR_DEVICE: calculate_percentage_to_100(device_counts),
        const.STR_OS: calculate_percentage_to_100(os_counts),
        const.STR_BROWSER: calculate_percentage_to_100(browser_counts),
    }

    return dashboard_json


# 処理対象日取得
def get_target_date(date_div: str):
    target_date = func.get_now()
    date_format = const.DATE_FORMAT_YYYYMMDD

    if date_div == const.STR_DAY:
        # 7日前のデータ
        target_date = func.get_calc_date(-const.NUM_TARGET_DAYS)
        date_format = const.DATE_FORMAT_MMDD_SLASH

    else:
        today = pd.to_datetime(func.get_now())
        if date_div == const.STR_MONTH:
            # 今月1日取得
            this_month_start = today.replace(day=1)

            # 先月1日取得
            last_month_start = this_month_start - relativedelta(months=1)
            target_date = last_month_start
            date_format = const.DATE_FORMAT_YYYYMM_SLASH

        elif date_div == const.STR_YEAR:
            # 今年1月1日取得
            this_year_start = today.replace(month=1, day=1)

            # 去年1月1日取得
            last_year_start = this_year_start - relativedelta(years=1)
            target_date = last_year_start
            date_format = const.DATE_FORMAT_YYYY

    return target_date, date_format


# デバイスとOSの割合（パーセンテージ）計算
def calculate_percentage_to_100(counts):
    total = counts.sum()

    # まず割合を計算し、小数点以下を切り捨てて整数に変換
    # 0.5の丸め誤差を防ぐため、最初に割合を計算
    percentages_float = (counts / total) * 100
    percentages_int = percentages_float.astype(int)

    # 合計が100になるように調整（端数を一番大きい項目に加算）
    current_sum = percentages_int.sum()
    diff = 100 - current_sum  # 100との差を計算

    # 端数を加算する対象を見つける（元の割合が一番大きい項目）
    # 元の割合（小数点以下を含む）でソートして、上位から差分を配分する

    # 調整の必要がある場合のみ実行
    if diff != 0:
        # 小数点以下の値が多い順（元の値が大きい順）に並べ替える
        sorted_indices = percentages_float.sort_values(ascending=False).index

        # 差分（diff）を大きい順に1ずつ配分する
        for i in range(abs(diff)):
            item_to_adjust = sorted_indices[i % len(sorted_indices)]
            if 0 < diff:
                # 100未満の場合、大きい項目に1を加算
                percentages_int[item_to_adjust] += 1
            elif diff < 0:
                # 100を超過する場合、大きい項目から1を減算（ほぼ起こらないが念のため）
                percentages_int[item_to_adjust] -= 1

    # 結果をJSON形式に変換
    result = [
        {"name": name, "value": value}
        for name, value in percentages_int.items()
        if value > 0
    ]
    return result


# ラベルリスト取得
def get_date_label_list(date_div: str):
    date_list = []
    today = func.get_now()
    if date_div == const.STR_DAY:
        for i in range(const.NUM_TARGET_DAYS):
            target_date = func.get_calc_date(-i)
            formatted_date = f"{target_date.month}/{target_date.day}"
            date_list.append(formatted_date)
    else:
        target_date, date_format = get_target_date(date_div)
        last_date = func.convert_date_to_str(target_date, date_format)
        this_date = func.convert_date_to_str(today, date_format)
        date_list = [last_date, this_date]

    date_list.sort()
    return date_list


# ダッシュボードデータ出力
def write_dashboard_log(request: Request, app_name: str):
    # ユーザーエージェントの文字列を取得
    user_agent_str = request.headers.get("user-agent")

    if user_agent_str:
        app_category = get_app_category(app_name)

        # 解析
        user_agent = parse(user_agent_str)

        ua_div = DEFAULT_VALUE
        if user_agent.is_mobile:
            ua_div = const.UA_DIV_MO
        elif user_agent.is_pc:
            ua_div = const.UA_DIV_PC
        elif user_agent.is_tablet:
            ua_div = const.UA_DIV_TABLET

        ua_os = user_agent.os.family
        ua_browser = user_agent.browser.family

        msg_list = [app_category, ua_div, ua_os, ua_browser]
        msg = const.SYM_SPACE.join(msg_list)
        func.print_msg(app_name, msg, SCRIPT_NAME)
    else:
        message = msg_const.MSG_ERR_USER_AGENT_NOT_FOUND_EN
        func.print_error_msg(app_name, message)


# カテゴリ名取得
def get_app_category(app_name: str) -> str:
    app_category = DEFAULT_VALUE

    # カテゴリ名とアプリリストを同時に処理する
    for category, apps in zip(const.LIST_CATEGORY, const.LIST_APP_CATEGORY):
        for app in apps:
            if app == app_name:
                app_category = category
                break

    return app_category


# IP情報取得
def get_ip_info(ip_address: str):
    url = f"{const.URL_IP_INFO}/{ip_address}/json"
    ip_info = func_api.get_response_result(url)
    return ip_info


if __name__ == const.MAIN_FUNCTION:
    update_data()
    backup_log()
