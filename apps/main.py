# 説明: メイン処理

import dotenv
import schedule

import apps.line as line
import apps.server as server
import apps.app_exec as sub
import apps.utils.constants as const
import apps.utils.function as func

# 環境変数を読み込む
dotenv.load_dotenv()

# ジョブ実行時間を環境変数から取得
NUM_HOUR_DAILY_JOB = func.get_env_val("NUM_HOUR_DAILY_JOB", decode_flg=const.FLG_OFF).zfill(5)
NUM_MIN_HOURLY_JOB = func.get_env_val("NUM_MIN_HOURLY_JOB", decode_flg=const.FLG_OFF).zfill(2)
NUM_SEC_NO_SLEEP = func.get_env_val(
    "NUM_SEC_NO_SLEEP", decode_flg=const.FLG_OFF, int_flg=const.FLG_ON
)


def main():
    # スレッド開始
    server.start_thread()

    # ジョブ実行
    job_scheduler()


def job_scheduler():
    # 毎日指定された時間に実行
    schedule.every().day.at(NUM_HOUR_DAILY_JOB).do(daily_job)

    # 毎日1時間毎に実行
    for hour in range(24):
        schedule.every().day.at(f"{hour:02d}:{NUM_MIN_HOURLY_JOB}").do(hourly_job)

    pending_cnt = 0

    exec_flg = const.FLG_ON
    while exec_flg:
        # スケジュールされたジョブを確認・実行
        schedule.run_pending()

        # 1秒間スリープする
        func.time_sleep(1)

        pending_cnt += 1

        # スリープ状態にならないよう、ジョブ実行後、10分毎に、サーバーアクセス
        if pending_cnt % NUM_SEC_NO_SLEEP == 0:
            sub.no_sleep()
            pending_cnt = 0


# 時次ジョブ: データ更新
def hourly_job():
    sub.update_news()
    line.get_msg_data_today()


# 日次ジョブ: LINEメッセージ送信
def daily_job():
    line.main(proc_flg=const.FLG_OFF)


# プログラムのエントリーポイント
if __name__ == const.MAIN_FUNCTION:
    # メイン実行
    main()
