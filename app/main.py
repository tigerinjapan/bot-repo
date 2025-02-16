# 説明：メイン処理

import dotenv
import function as func
import schedule
from line_api import main as line_api
from server import server_thread

dotenv.load_dotenv()

# ジョブ実行時間
JOB_SCHEDULE_TIME = func.get_env_val("JOB_SCHEDULE_TIME")


def main():
    # Koyeb用 サーバー立ち上げ
    server_thread()

    # 条件：毎日指定時間で、実行
    schedule.every().day.at(JOB_SCHEDULE_TIME).do(job)

    while True:
        # 指定時間で、実行
        schedule.run_pending()
        func.time_sleep(1)


def job():
    line_api()


main()
