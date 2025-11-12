"""
ログ管理
"""

from datetime import datetime

import apps.utils.constants as const
import apps.utils.log_dao as log_dao
import apps.utils.log_dto as log_dto
import apps.utils.function as func
import apps.utils.message_constants as msg_const

# スクリプト名
SCRIPT_NAME = func.get_app_name(__file__)

# タイトル
app_title = "ログ管理"

# カラムリスト
col_list = [const.STR_DATE_JA, const.STR_DIV_JA, const.STR_CONTENTS_JA]
col_list_admin = col_list + [const.STR_STATUS_JA]


def backup_log(log_div: str = const.APP_DASHBOARD):
    """
    ログバックアップ
    """
    div = f"{const.STR_BACKUP} {log_div}"
    func.print_start(div)

    get_log_data_list(log_div, backup_flg=const.FLG_ON)

    func.print_end(div)


def get_log_data_list(
    log_div: str, col_len: int = const.NUM_THREE, backup_flg: bool = const.FLG_OFF
):
    """
    ログデータリスト取得
    """
    data_list = []
    backup_data_list = []
    new_log_list = []

    try:
        log_path = func.get_file_path(
            log_div,
            file_type=const.FILE_TYPE_LOG,
            file_div=const.STR_OUTPUT,
        )

        log_data_text = func.read_file(log_path)
        if log_data_text:
            log_data_list = log_data_text.split(const.SYM_NEW_LINE)

            target_date = get_last_year_first()
            log_backup_list = log_dao.get_log_data(log_div, target_date)

            for log_data in log_data_list:
                if log_data and log_data not in log_backup_list:
                    new_log_list.append(log_data)

            if new_log_list:
                log_backup_list.extend(new_log_list)

            for log_data in log_backup_list:
                data = log_data.split(const.SYM_SPACE)[:col_len]
                data_list.append(data)

                if backup_flg and log_data in new_log_list:
                    log_date = data[0]
                    cutoff_date = func.get_calc_date(-1)
                    log_datetime = func.convert_str_to_date(
                        log_date, const.DATE_FORMAT_YYYYMMDD_DASH
                    )
                    # 1日以前のログか判定
                    if log_datetime <= cutoff_date:
                        log_backup = [log_div, log_data, log_datetime]
                        json_data = log_dto.get_insert_data_for_log(log_backup)
                        backup_data_list.append(json_data)

            if backup_data_list:
                # DB登録
                log_dao.insert_log_data(backup_data_list)

                # ログファイル：本日分以外削除
                backup_log_data = (
                    const.SYM_NEW_LINE.join(new_log_list) + const.SYM_NEW_LINE
                )
                func.write_file(log_path, backup_log_data)

                msg_div = f"{len(backup_data_list)}件, {const.STR_BACKUP_JA}"
                func.print_info_msg(msg_div, msg_const.MSG_INFO_PROC_COMPLETED)

            else:
                if not new_log_list:
                    func.print_info_msg(SCRIPT_NAME, msg_const.MSG_INFO_DATA_NOT_EXIST)

    except Exception as e:
        func.print_info_msg(SCRIPT_NAME, e)

    return data_list


# TODO: エラー対応すると、log_divをdummyへ更新？
def get_df_data(log_div: str = const.STR_ERROR, user_div: str = const.AUTH_DEV):
    """
    DataFrameのデータ取得
    """
    data_list = []

    # JSONデータ取得
    target_date = get_last_year_first()
    log_data_list = log_dao.get_log_data(log_div, target_date)

    for log_data in log_data_list:
        log_data_split = log_data.split(const.SYM_SPACE)
        date = log_data_split[0]
        div = get_log_category(log_data_split[3])
        message = const.SYM_SPACE.join(log_data_split[3:])
        data = [date, div, message]
        data_list.append(data)

    # DataFrame変換
    df = func.get_df(data_list, col_list)

    user_auth = func.get_auth_num(user_div)
    if user_auth == const.NUM_AUTH_ADMIN:
        df[const.STR_STATUS_JA] = func.get_dialog_button(
            func.convert_upper_lower(log_div),
            df[const.STR_DIV_JA],
            "▶️",
        )
        df.columns = col_list_admin

    return df


def get_log_category(log_data: str) -> str:
    """
    ログカテゴリ取得
    """
    log_category = const.SYM_BLANK
    func_name = log_data.replace("[", const.SYM_BLANK).replace("]", const.SYM_BLANK)

    for category in const.LIST_LOG_CATEGORY:
        if category in func_name:
            log_category = category
            break

    if not log_category:
        log_category = const.STR_ETC
        if const.STR_RESPONSE in func_name or const.STR_REQUEST in func_name:
            log_category = const.STR_API
        elif const.STR_MONGO in func_name:
            log_category = const.STR_DB
        else:
            app_category_list = [
                item for sub_list in const.LIST_APP_CATEGORY for item in sub_list
            ]
            for app_category in app_category_list:
                if app_category in func_name:
                    log_category = const.STR_APP
                    break

    return log_category


def get_last_year_first() -> datetime:
    """
    去年の1月1日取得
    """
    # 1. 今年の年度を取得
    this_year = func.get_now(const.DATE_YEAR)

    # 2. 今年から1を引いて、去年の年を計算
    last_year = this_year - 1

    # 3. 去年の1月1日のdate型を作成
    last_year_first = datetime(last_year, 1, 1)
    return last_year_first


if __name__ == const.MAIN_FUNCTION:
    get_log_data_list(const.APP_DASHBOARD)
