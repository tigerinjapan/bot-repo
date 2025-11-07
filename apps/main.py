"""
メイン処理
"""

import dotenv
import schedule

import apps.appl as appl
import apps.dashboard as dashboard
import apps.kakao as kakao
import apps.line as line
import apps.server as server
import apps.utils.constants as const
import apps.utils.function as func

# 環境変数を読み込む
dotenv.load_dotenv()

# ジョブ実行時間を環境変数から取得
TIME_WEEKLY_JOB = func.get_env_val("TIME_WEEKLY_JOB", div=const.STR_ENV_VAR)
TIME_DAILY_JOB = func.get_env_val("TIME_DAILY_JOB", div=const.STR_ENV_VAR)
TIME_DAILY_JOB_2 = func.get_env_val("TIME_DAILY_JOB_2", div=const.STR_ENV_VAR)
TIME_DAILY_JOB_3 = func.get_env_val("TIME_DAILY_JOB_3", div=const.STR_ENV_VAR)
MIN_HOURLY_JOB = func.get_env_val("MIN_HOURLY_JOB", div=const.STR_ENV_VAR)
SEC_NO_SLEEP = func.get_env_val("SEC_NO_SLEEP", div=const.STR_ENV_VAR)


def main():
    """
    メイン処理
    """
    # スレッド開始
    server.start_thread()

    # ジョブ実行
    job_scheduler()


def job_scheduler():
    """
    ジョブ実行
    """
    if func.is_local_env():
        func.is_network()
    else:
        # 毎週指定された時間に実行（例：09:00）
        schedule.every().monday.at(TIME_WEEKLY_JOB).do(weekly_job)

        # 毎日指定された時間に実行（例：07:00）
        schedule.every().day.at(TIME_DAILY_JOB).do(daily_job)
        schedule.every().day.at(TIME_DAILY_JOB_2).do(daily_job_2)
        schedule.every().day.at(TIME_DAILY_JOB_3).do(daily_job_3)

    # 1時間毎に実行（例：:30）
    schedule.every().hour.at(MIN_HOURLY_JOB).do(hourly_job)

    pending_cnt = 0

    exec_flg = const.FLG_ON
    while exec_flg:
        # スケジュールされたジョブを確認・実行
        schedule.run_pending()

        # 1秒間スリープする
        func.time_sleep(1)

        pending_cnt += 1

        # スリープ状態にならないよう、ジョブ実行後、10分毎に、サーバーアクセス
        if pending_cnt % int(SEC_NO_SLEEP) == 0:
            every_min_job()
            pending_cnt = 0


def weekly_job():
    """
    週次ジョブ
    """
    if func.get_now(const.DATE_WEEKDAY) == 0:
        line.sub(div=const.STR_NISA)


def daily_job():
    """
    日次ジョブ
    """
    line.main()
    dashboard.backup_log()


def daily_job_2():
    """
    日次ジョブ
    """
    line.main(data_div=const.NUM_TWO)
    line.sub(div=const.APP_MLB)
    kakao.main(div=const.APP_LCC)


def daily_job_3():
    """
    日次ジョブ
    """
    kakao.main()


def hourly_job():
    """
    時次ジョブ
    """
    appl.update_news(const.APP_TODAY_KOREA)
    appl.update_news()
    appl.update_news(const.APP_NUMBER)
    dashboard.update_data()
    dashboard.backup_log(const.STR_ERROR)


def every_min_job():
    # 随時ジョブ
    server.health_check()


if __name__ == const.MAIN_FUNCTION:
    main()
