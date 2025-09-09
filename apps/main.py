# 説明: メイン処理

import dotenv
import schedule

import apps.appl as appl
import apps.line as line
import apps.server as server
import apps.utils.constants as const
import apps.utils.function as func

# 環境変数を読み込む
dotenv.load_dotenv()

# ジョブ実行時間を環境変数から取得
HOUR_DAILY_JOB = func.get_env_val("NUM_HOUR_DAILY_JOB", int_flg=const.FLG_ON)
HOUR_DAILY_JOB_2 = func.get_env_val("NUM_HOUR_DAILY_JOB_2", int_flg=const.FLG_ON)
MIN_HOURLY_JOB = func.get_env_val("NUM_MIN_HOURLY_JOB", int_flg=const.FLG_ON)
SEC_NO_SLEEP = func.get_env_val("NUM_SEC_NO_SLEEP", int_flg=const.FLG_ON)


def main():
    # スレッド開始
    server.start_thread()

    # ジョブ実行
    job_scheduler()


def job_scheduler():
    # 毎日指定された時間に実行
    time_daily_job = f"{HOUR_DAILY_JOB:02d}:00"
    time_daily_job_2 = f"{HOUR_DAILY_JOB_2:02d}:00"

    schedule.every().day.at(time_daily_job).do(daily_job)
    schedule.every().day.at(time_daily_job_2).do(daily_job_2)

    # 1時間毎に実行
    schedule.every().hour.at(f":{MIN_HOURLY_JOB:02d}").do(hourly_job)

    pending_cnt = 0

    exec_flg = const.FLG_ON
    while exec_flg:
        # スケジュールされたジョブを確認・実行
        schedule.run_pending()

        # 1秒間スリープする
        func.time_sleep(1)

        pending_cnt += 1

        # スリープ状態にならないよう、ジョブ実行後、10分毎に、サーバーアクセス
        if pending_cnt % SEC_NO_SLEEP == 0:
            every_min_job()
            pending_cnt = 0


# 日次ジョブ
def daily_job():
    line.main(proc_flg=const.FLG_OFF)


# 日次ジョブ
def daily_job_2():
    line.main(data_div=const.NUM_TWO)


# 時次ジョブ
def hourly_job():
    appl.update_news()
    line.get_msg_data_today()


# 随時ジョブ
def every_min_job():
    server.health_check()


# プログラムのエントリーポイント
if __name__ == const.MAIN_FUNCTION:
    # メイン実行
    main()
