# 説明：メイン処理

import dotenv
import schedule

import apps.line_msg_api as line_msg_api
import apps.server as server
import apps.utils.constants as const
import apps.utils.function as func

# 環境変数を読み込む
dotenv.load_dotenv()

# ジョブ実行時間を環境変数から取得
NUM_HOUR_DAILY_JOB = func.get_env_val("NUM_HOUR_DAILY_JOB")
NUM_MIN_HOURLY_JOB = func.get_env_val("NUM_MIN_HOURLY_JOB")


def main():
    # スレッド開始
    server.start_thread()

    # ジョブ実行
    job_scheduler()


def job_scheduler():
    # ローカル環境でない場合、ジョブをスケジュールする
    if not func.is_local_env():
        # 毎日5分間毎に実行
        schedule.every(5).minutes.do(min_job)

        # 毎日指定された時間に実行
        schedule.every().day.at(f"{NUM_HOUR_DAILY_JOB:02d}:00").do(daily_job)

        # 毎日1時間毎に実行
        for hour in range(24):
            schedule.every().day.at(f"{hour:02d}:{NUM_MIN_HOURLY_JOB}").do(hourly_job)

        while True:
            # スケジュールされたジョブを確認・実行
            schedule.run_pending()
            # 1秒間スリープする
            func.time_sleep(1)


# 分次ジョブ：スリープしない
def min_job():
    server.no_sleep()


# 日次ジョブ：LINEメッセージ送信
def daily_job():
    line_msg_api.main()


# 時次ジョブ：ウェブページの更新
def hourly_job():
    server.update_news()


# メイン実行
main()

# プログラムのエントリーポイント
if __name__ == const.MAIN_FUNCTION:
    if func.is_local_env():
        func.print_test_data(NUM_HOUR_DAILY_JOB, const.FLG_ON)
