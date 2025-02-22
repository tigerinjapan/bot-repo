# 説明：メイン処理

import os
import sys

import dotenv
import schedule

print("[sys.path] ", sys.path)  # TODO テスト後削除
print("[os.getcwd()] ", os.getcwd())  # TODO テスト後削除

import utils.function_selenium as func_sele

print(func_sele.test_access_webdriver())

import apps.utils.function as func
from apps.line_api import main as line_api
from apps.server import start_thread

dotenv.load_dotenv()

# ジョブ実行時間
JOB_SCHEDULE_TIME = func.get_env_val("JOB_SCHEDULE_TIME")


def main():
    # サーバー立ち上げ
    start_thread()

    if not func.check_local_ip():
        # 条件：毎日指定時間で、実行
        schedule.every().day.at(JOB_SCHEDULE_TIME).do(job)

        while True:
            # 指定時間で、実行
            schedule.run_pending()
            func.time_sleep(1)


def job():
    line_api()


main()
