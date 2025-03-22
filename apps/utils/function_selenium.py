# 説明：Selenium関数

import sys

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.message_constants as msg_const


# ドライバーの取得
def get_webdriver():
    # ローカル環境判定
    local_flg = const.FLG_ON if func.is_local_env() else const.FLG_OFF

    # ChromeDriverサービス設定
    if local_flg:
        service = Service()
    else:
        executable_path = "/usr/bin/chromedriver"
        service = Service(executable_path=executable_path)

    # Message: tab crashed  (Session info: chrome=133.0.6943.126)

    # ブラウザオプション設定
    options = webdriver.ChromeOptions()

    # オプション：ブラウザの表示
    browser_display_options = [
        "--start-maximized",  # ウィンドウ最大化
        "--window-size=1920x1080",  # ウィンドウサイズ指定
        # "--blink-settings=imagesEnabled=false",  # 画像ロード無効化
    ]

    if local_flg:
        option_add_arg = "--incognito"  # シークレットモード
    else:
        option_add_arg = "--headless"  # ヘッドレスモードで実行
    browser_display_options.append(option_add_arg)

    # オプション：セキュリティ
    security_options = [
        "--no-sandbox",  # サンドボックス無効化
    ]

    if local_flg:
        security_options += [
            "--disable-notifications",  # 通知無効化
            "--disable-popup-blocking",  # ポップアップブロック無効化
            "--no-sandbox",  # サンドボックス無効化
            "--disable-extensions",  # 拡張機能無効化
            "--ignore-certificate-errors",  # 証明書エラー無視
            "--ignore-ssl-errors",  # SSLエラー無視
        ]

    # オプション：パフォーマンス
    performance_options = [
        "--disable-gpu",  # GPU無効化
    ]

    if local_flg:
        performance_options += [
            "--disable-dev-shm-usage",  # 開発共有メモリ無効化
            "--disable-accelerated-2d-canvas",  # ハードウェアアクセラ無効化
        ]

    # オプション：自動化とログ
    automation_and_log_options = [
        "--disable-blink-features=AutomationControlled",  # 自動化フラグ無効化
        "--log-level=3",  # ログ出力抑制
    ]

    # オプション：その他
    other_options = [
        # "--disable-javascript",  # JavaScript無効化
        "--user-agent=MyCustomUserAgent",  # ユーザーエージェント設定
        const.UA_OPT_PC,  # ユーザーエージェント設定
    ]

    options_list = browser_display_options
    options_list += security_options
    options_list += performance_options

    if local_flg:
        options_list += automation_and_log_options
        options_list += other_options

    # 各カテゴリーのオプションを追加
    for option in options_list:
        options.add_argument(option)

    # Chromeのバイナリパスを指定
    # if not local_flg:
    #     options.binary_location = "/usr/bin/chromium"

    download_path = func.get_app_path(const.STR_OUTPUT)
    prefs = {"download.default_directory": download_path}
    options.add_experimental_option("prefs", prefs)

    # ドライバー初期化
    try:
        driver = webdriver.Chrome(service=service, options=options)

    except WebDriverException as wde:
        curr_def_nm = sys._getframe().f_code.co_name
        func.print_error_msg(curr_def_nm, msg_const.MSG_ERR_CONNECTION_FAILED)
        func.print_error_msg("[WebDriverException] ", str(wde))
        driver = const.NONE_CONSTANT

    return driver


# 要素が特定の条件を満たすまで待機
def wait_for_element(driver, by, value, timeout=30):
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))


# 暗黙的に指定した秒数だけ待機
def implicit_wait(driver, time_sec=10):
    driver.implicitly_wait(time_sec)


# 要素をクリック
def click_element(driver, by, value):
    element = find_element(driver, by, value)
    if element:
        element.click()


# 要素に入力
def write_element(driver, by, value, input_value):
    element = find_element(driver, by, value)
    if element:
        element.clear()
        element.send_keys(input_value)


# 要素を検索
def find_element(driver, by: str, value: str, timeout: int = 3):
    element = const.NONE_CONSTANT
    exception_div = const.NONE_CONSTANT

    try:
        implicit_wait(driver, timeout)
        element = driver.find_element(by, value)
    except AttributeError as ae:
        exception_div = ae
    except Exception as e:
        exception_div = e

    if exception_div:
        curr_def_nm = sys._getframe().f_code.co_name
        func.print_error_msg(value, msg_const.MSG_ERR_NO_SUCH_ELEMENT)
        func.print_error_msg(f"[{curr_def_nm}] ", str(exception_div))

    return element


# 要素のテキストを取得
def get_element_text(driver, by, value):
    element = find_element(driver, by, value)
    elem_text = element.text if element else const.SYM_BLANK
    return elem_text


# 接続テスト
def test_webdriver():
    driver = get_webdriver()
    try:
        if driver:
            driver.get(const.URL_GOOGLE)
            func.print_info_msg(driver.title)
            func.time_sleep()
            driver.quit()
        else:
            func.print_error_msg("Chrome Driver", msg_const.MSG_ERR_FILE_NOT_EXIST)

    except WebDriverException as wde:
        curr_def_nm = sys._getframe().f_code.co_name
        func.print_error_msg(curr_def_nm, msg_const.MSG_ERR_CONNECTION_FAILED)
        func.print_error_msg("[test_webdriver:WebDriverException] ", str(wde))
        driver = const.NONE_CONSTANT


if __name__ == const.MAIN_FUNCTION:
    test_webdriver()
