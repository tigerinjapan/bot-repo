"""
ログ管理
"""

from datetime import datetime

import apps.utils.constants as const
import apps.utils.log_dao as log_dao
import apps.utils.log_dto as log_dto
import apps.utils.function as func
import apps.utils.function_api as func_api
import apps.utils.message_constants as msg_const

# スクリプト名
SCRIPT_NAME = func.get_app_name(__file__)

# タイトル
app_title = "ログ管理"

# カラムリスト
col_list = [const.STR_DATE_JA, const.STR_DIV_JA, const.STR_CONTENTS_JA]
col_list_admin = col_list + [const.STR_STATUS_JA]


def get_log_data_list(
    log_div: str,
    col_len: int = const.NUM_THREE,
    backup_flg: bool = const.FLG_OFF,
):
    """
    ログデータリスト取得
    """
    data_list = []
    log_backup_list = []
    backup_data_list = []
    new_log_list = []
    rewrite_log_list = []

    # 重複データ削除
    existed_data_list = []

    try:
        log_path = func.get_file_path(
            log_div,
            file_type=const.FILE_TYPE_LOG,
            file_div=const.STR_OUTPUT,
        )

        log_data_text = func.read_file(log_path)
        if log_data_text:
            log_data_list = log_data_text.split(const.SYM_NEW_LINE)

            if log_div != const.STR_ERROR:
                dummy_log_path = log_path.replace(
                    log_div, f"{log_div}_{const.STR_DUMMY}"
                )
                if backup_flg:
                    target_date = get_last_year_first()
                    log_backup_list = log_dao.get_log_data(log_div, target_date)
                    dummy_data = const.SYM_NEW_LINE.join(log_backup_list)
                    func.write_file(dummy_log_path, dummy_data)
                else:
                    dummy_log_text = func.read_file(dummy_log_path)
                    log_backup_list = dummy_log_text.split(const.SYM_NEW_LINE)

            for log_data in log_data_list:
                if log_data and log_data not in log_backup_list:
                    if log_div == const.STR_ERROR:
                        message = log_data[24:]
                        if message in existed_data_list:
                            continue
                        existed_data_list.append(message)

                    new_log_list.append(log_data)

            if new_log_list:
                log_backup_list.extend(new_log_list)

            for log_data in log_backup_list:
                data = log_data.split(const.SYM_SPACE)[:col_len]
                data_list.append(data)

                if backup_flg and log_data in new_log_list:
                    insert_data = get_insert_data(log_div, log_data, data[0])
                    if insert_data:
                        backup_data_list.append(insert_data)
                    else:
                        rewrite_log_list.append(log_data)

            if backup_data_list:
                backup_data(log_div, backup_data_list, rewrite_log_list, log_path)
            else:
                if not new_log_list:
                    func.print_info_msg(SCRIPT_NAME, msg_const.MSG_INFO_DATA_NOT_EXIST)

    except Exception as e:
        func.print_info_msg(SCRIPT_NAME, e)

    return data_list


def backup_log(log_div: str = const.APP_DASHBOARD):
    """
    ログバックアップ
    """
    div = f"{const.STR_BACKUP} {log_div}"
    func.print_start(div)

    get_log_data_list(log_div, backup_flg=const.FLG_ON)

    func.print_end(div)


def backup_data(
    log_div: str, backup_data_list, rewrite_log_list: list[str], log_path: str
):
    """
    データバックアップ
    """
    try:
        if log_div == const.STR_ERROR:
            api_path = f"/{const.APP_BOARD}/{const.STR_ADD}"
            json_data = {const.STR_DATA: backup_data_list}
            json_data = func.get_dumps_json(json_data)

            # DB登録（掲示板情報）
            result = func_api.post_api_on_server(api_path, json_data)
            if result:
                message = result[const.STR_MESSAGE]

        else:
            # DB登録（ログ）
            log_dao.insert_log_data(backup_data_list)
            message = msg_const.MSG_INFO_PROC_COMPLETED

        if message == msg_const.MSG_INFO_PROC_COMPLETED:
            # ログファイル再作成
            rewrite_log = (
                const.SYM_NEW_LINE.join(rewrite_log_list)
                if rewrite_log_list
                else const.SYM_BLANK
            )
            rewrite_log_data = rewrite_log + const.SYM_NEW_LINE
            func.write_file(log_path, rewrite_log_data)

            msg_div = f"{log_div} {len(backup_data_list)}件 {const.STR_BACKUP_JA}"
            func.print_info_msg(msg_div, msg_const.MSG_INFO_PROC_COMPLETED)

    except Exception as e:
        func.print_info_msg(SCRIPT_NAME, e)


def get_insert_data(log_div: str, log_data: str, log_date: str):
    """
    バックアップ登録データ取得
    """
    insert_data = const.SYM_BLANK

    cutoff_date = func.get_now()
    log_datetime = func.convert_str_to_date(log_date, const.DATE_FORMAT_YYYYMMDD_DASH)

    # 1日以前のログか判定
    if log_datetime < cutoff_date:
        if log_div == const.STR_ERROR:
            idx_app = const.LIST_BOARD_APP.index("Server")
            idx_category = const.LIST_BOARD_CATEGORY.index("Error")
            idx_type = const.LIST_BOARD_TYPE.index("Modify")
            message = log_data.replace("http", const.SYM_BLANK)
            insert_data = [
                idx_app,
                idx_category,
                idx_type,
                message,
                const.AUTH_ADMIN,
            ]
        else:
            log_backup = [log_div, log_data, log_datetime]
            insert_data = log_dto.get_insert_data_for_log(log_backup)

    return insert_data


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
    # get_log_data_list(const.APP_DASHBOARD)
    backup_log(const.APP_DASHBOARD)
