# 説明：Playwright関数

import apps.utils.constants as const
import apps.utils.function as func
from playwright.sync_api import sync_playwright

# アプリケーション
app_name = "Playwright"


def main(app_div: str = const.STR_TEST):
    # 処理開始
    func.print_start(app_name)
    playwright = sync_playwright().start()

    # パフォーマンス向上のためにブラウザオプションを設定
    browser = playwright.chromium.launch(
        headless=const.FLG_ON,  # ヘッドレスモードで動作（UIを表示しない）
        args=[
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage",
        ],
    )
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},  # 視覚領域の設定
        java_script_enabled=True,  # JavaScriptを有効化
        bypass_csp=True,  # CSP（コンテンツセキュリティポリシー）を無視
    )

    page = context.new_page()

    # コンテンツ取得
    contents = get_contents_by_locator(app_div, page)

    # リソースを明示的に解放
    page.close()
    context.close()
    browser.close()

    playwright.stop()

    # 処理終了
    func.print_end(app_name)

    return contents


# コンテンツ取得
def get_contents_by_locator(app_div: str, page):
    url = const.URL_GOOGLE
    # if (app_div == const.STR_TEST):

    # ページへ移動
    page.goto(url, wait_until="domcontentloaded")  # 高速読み込み

    # 結果ページのタイトルを表示
    title = page.title()
    func.print_info_msg(const.STR_TITLE_JA, title)

    contents = [title]
    return contents


# 要素を取得
def get_elem_by_locator(
    page,
    attr_val: str,
    attr_name: str = const.SYM_BLANK,
    list_flg: bool = const.FLG_OFF,
):
    if attr_name == const.ATTR_ID:
        attr_val = "#" + attr_val
    elif attr_name == const.ATTR_CLASS:
        attr_val = "." + attr_val

    elem = page.locator(attr_name)

    if list_flg:
        func.print_info_msg("要素の数：", elem.count())
    return elem


# 指定した要素にテキストを入力
def input_elem_by_locator(page, attr_name: str, attr_val: str, input_text: str):
    elem = get_elem_by_locator(page, attr_name, attr_val)
    elem.fill(input_text)


# 要素をクリック
def click_elem_by_locator(page, attr_name: str, attr_val: str, timeout: int = 1000):
    elem = get_elem_by_locator(page, attr_name, attr_val)
    page.wait_for_timeout(timeout)  # 要素が有効になるまで待機
    elem.click()


# 要素のテキストコンテンツを取得
def get_text_by_elem(elem):
    elem_text = elem.text_content()
    return elem_text


# 要素の属性値を取得
def get_attr_by_elem(elem, attr_name: str):
    elem_attr = elem.get_attribute(attr_name)
    return elem_attr


# スクリーンショット保存
def save_page_screenshot(page, div: str):
    file_path = func.get_file_path(div, const.FILE_TYPE_PNG, const.STR_OUTPUT)
    page.screenshot(path=file_path)


if __name__ == const.MAIN_FUNCTION:
    main()
