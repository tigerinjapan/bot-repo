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
JOB_SCHEDULE_TIME = func.get_env_val("JOB_SCHEDULE_TIME")


def main():
    # サーバー起動
    server.run_server()

    # ローカル環境でない場合、ジョブをスケジュールする
    if not func.is_local_env():
        # 毎日指定された時間に実行
        schedule.every().day.at(JOB_SCHEDULE_TIME).do(daily_news)

        # 毎日1時間毎に実行
        for hour in range(24):
            schedule.every().day.at(f"{hour:02d}:55").do(update_news)

        while True:
            # 保留中のジョブを実行
            schedule.run_pending()
            # 1秒間スリープする
            func.time_sleep(1)


# デイリーニュース：LINE APIを呼び出す
def daily_news():
    line_msg_api.main()


# ニュース更新：ウェブページの更新
def update_news():
    server.update_news()


# メイン実行
main()

# プログラムのエントリーポイント
if __name__ == const.MAIN_FUNCTION:
    func.print_test_data(JOB_SCHEDULE_TIME)
