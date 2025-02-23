# 説明：メイン処理

import dotenv
import schedule

import apps.utils.constants as const
import apps.utils.function as func
from apps.line_api import main as line_api
from apps.server import start_thread

dotenv.load_dotenv()

# ジョブ実行時間
JOB_SCHEDULE_TIME = func.get_env_val("JOB_SCHEDULE_TIME")


def main():
    # サーバー立ち上げ
    start_thread()

    if not func.is_local_env():
        # 条件：毎日指定時間で、実行
        schedule.every().day.at(JOB_SCHEDULE_TIME).do(job)

        while True:
            # 指定時間で、実行
            schedule.run_pending()
            func.time_sleep(1)


# ジョブ
def job():
    line_api()


# メイン実行
main()

# プログラムのエントリーポイント
if __name__ == const.MAIN_FUNCTION:
    print(JOB_SCHEDULE_TIME)
