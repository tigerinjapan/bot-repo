# 説明: ダッシュボード

import numpy as np
import pandas as pd
from fastapi import Request
from user_agents import parse

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.message_constants as msg_const

# スクリプト名
SCRIPT_NAME = func.get_app_name(__file__)
app_div = SCRIPT_NAME

# カラム
COL_LIST_DASHBOARD = [
    const.STR_DATE,
    const.STR_TIME,
    const.STR_LEVEL,
    const.STR_APP,
    const.STR_CATEGORY,
    const.STR_COUNTRY,
    const.STR_DEVICE,
    const.STR_OS,
    const.STR_BROWSER,
]


# ダッシュボードデータ取得
def get_dashboard_json():
    func.print_start(SCRIPT_NAME)

    log_path = func.get_file_path(
        app_div, file_type=const.FILE_TYPE_LOG, file_div=const.STR_OUTPUT
    )
    log_data_text = func.read_file(log_path)
    log_data_list = log_data_text.split(const.SYM_NEW_LINE)
    data_list = []
    for log_data in log_data_list:
        data = log_data.split(const.SYM_SPACE)
        if len(data) == len(COL_LIST_DASHBOARD):
            data_list.append(data)

    df = func.get_df(data_list, COL_LIST_DASHBOARD)
    df[const.STR_DATE] = pd.to_datetime(df[const.STR_DATE]).dt.strftime(
        const.DATE_FORMAT_MMDD
    )
    df[const.STR_COUNTRY] = np.where(
        df[const.STR_COUNTRY] == const.COUNTRY_CD_JP,
        const.STR_JAPAN_JA,
        const.STR_KOREA_JA,
    )

    daily_access = df[const.STR_DATE].value_counts().sort_index()
    total_access = daily_access.sum()
    category_counts = df[const.STR_CATEGORY].value_counts()
    country_counts = df[const.STR_COUNTRY].value_counts()
    device_counts = df[const.STR_DEVICE].value_counts()
    os_counts = df[const.STR_OS].value_counts()
    browser_counts = df[const.STR_BROWSER].value_counts()

    # JSON形式のデータを作成
    json_data = {
        "label": "日",
        "users": {
            "total": f"{total_access:,}",
            "labels": daily_access.index.tolist(),
            "data": daily_access.values.tolist(),
        },
        const.STR_CATEGORY: {
            "labels": category_counts.index.tolist(),
            "data": category_counts.values.tolist(),
        },
        const.STR_COUNTRY: calculate_percentage_to_100(country_counts),
        const.STR_DEVICE: calculate_percentage_to_100(device_counts),
        const.STR_OS: calculate_percentage_to_100(os_counts),
        const.STR_BROWSER: calculate_percentage_to_100(browser_counts),
    }
    json_data = {"day": json_data}

    dummy_data = func.get_json_data(const.STR_DUMMY, const.STR_OUTPUT)
    json_data.update(dummy_data)

    file_path = func.get_file_path(
        app_div, file_type=const.FILE_TYPE_JSON, file_div=const.STR_OUTPUT
    )

    # 結果をJSON形式で表示
    func.write_file(file_path, json_data)

    func.print_end(SCRIPT_NAME)


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
            if diff > 0:
                # 100未満の場合、大きい項目に1を加算
                percentages_int[item_to_adjust] += 1
            elif diff < 0:
                # 100を超過する場合、大きい項目から1を減算（ほぼ起こらないが念のため）
                percentages_int[item_to_adjust] -= 1

    # 結果をJSON形式に変換
    result = [{"name": name, "value": value} for name, value in percentages_int.items()]
    return result


# ダッシュボードデータ出力
def write_dashboard_log(request: Request, app_name: str):
    # ユーザーエージェントの文字列を取得
    user_agent_str = request.headers.get("user-agent")

    if user_agent_str:
        app_category = get_app_category(app_name)

        country_cd = get_user_country_cd(request)

        # 解析
        user_agent = parse(user_agent_str)

        ua_div = const.UA_DIV_MO
        if user_agent.is_pc:
            ua_div = const.UA_DIV_PC
        elif user_agent.is_tablet:
            ua_div = const.UA_DIV_TABLET

        ua_os = user_agent.os.family
        ua_browser = user_agent.browser.family

        msg_list = [app_category, country_cd, ua_div, ua_os, ua_browser]
        msg = const.SYM_SPACE.join(msg_list)
        func.print_msg(app_name, msg, app_div)
    else:
        message = msg_const.MSG_ERR_USER_AGENT_NOT_FOUND_EN
        func.print_error_msg(app_name, message)


# カテゴリ名取得
def get_app_category(app_name: str) -> str:
    app_category = "unknown"

    # カテゴリ名とアプリリストを同時に処理する
    for category, apps in zip(const.LIST_CATEGORY, const.LIST_APP_CATEGORY):
        for app in apps:
            if app == app_name:
                app_category = category
                break

    return app_category


# IPアドレスより、国コード取得
def get_user_country_cd(request: Request) -> str:

    # サーバーに直接アクセスの場合
    client_ip = request.client.host

    # クラウドサービスなどを経由している場合
    forwarded_for = request.headers.get("x-forwarded-for")

    if forwarded_for:
        ip_address = forwarded_for.split(",")[0].strip()
    else:
        ip_address = client_ip

    country = get_country_cd_from_csv(ip_address)
    return country


# CSVより、国コード取得
def get_country_cd_from_csv(ip_address: str) -> str:
    country_cd = const.COUNTRY_CD_JP
    file_path = func.get_file_path(const.STR_IP, const.FILE_TYPE_CSV)
    data = func.get_dict_from_csv(file_path, ip_address)
    if data:
        country_cd = data[0]
    return country_cd


if __name__ == const.MAIN_FUNCTION:
    get_dashboard_json()
