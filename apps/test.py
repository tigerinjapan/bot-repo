# 説明: カフェ
import asyncio

import apps.utils.constants as const
import apps.utils.function as func

# アプリケーション名
app_name = func.get_app_name(__file__)

# タイトル
app_title = "テスト"

# カラムリスト
col_list = [
    const.STR_DIV_JA,
    const.STR_TITLE_JA,
    const.STR_CONTENTS_JA,
]


def main():
    message = "Server is on api test."
    return message


def async_main():
    contents = asyncio.run(async_test())
    return contents


async def async_test():
    func.print_info_msg(const.STR_TEST)


if __name__ == const.MAIN_FUNCTION:
    contents = main()
    func.print_test_data(contents)
