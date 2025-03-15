# 説明：カフェ
import asyncio
from playwright.sync_api import sync_playwright

import apps.utils.constants as const
import apps.utils.function as func

# アプリケーション名
app_name = func.get_app_name(__file__)

# タイトル
app_title = "おしゃれカフェ"

# カラムリスト
col_list = [
    const.STR_DIV_JA,
    const.STR_TITLE_JA,
    const.STR_CONTENTS_JA,
]


def main():
    contents = sync_main()
    return contents


def sync_main():
    # Playwrightのインスタンスを取得
    playwright = sync_playwright().start()
    try:
        # ブラウザの起動
        browser = playwright.chromium.launch()

        # 新しいページを作成
        page = browser.new_page()

        # ページにアクセス
        url = const.URL_GOOGLE
        page.goto(url)

        # ページタイトルを出力
        title = page.title()
    finally:
        # ブラウザとPlaywrightのインスタンスを閉じる
        browser.close()
        playwright.stop()

        return title


# async def async_main():
#     # Playwrightのインスタンスを取得
#     playwright = await async_playwright().start()
#     try:
#         # ブラウザの起動
#         browser = await playwright.chromium.launch()

#         # 新しいページを作成
#         page = await browser.new_page()

#         # ページにアクセス
#         url = const.URL_GOOGLE
#         await page.goto(url)

#         # ページタイトルを出力
#         title = await page.title()
#     finally:
#         # ブラウザとPlaywrightのインスタンスを閉じる
#         await browser.close()
#         await playwright.stop()

#         return title


if __name__ == const.MAIN_FUNCTION:
    contents = main()
    func.print_test_data(contents)
