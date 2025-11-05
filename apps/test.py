"""
テストページ
"""

import asyncio

import apps.utils.constants as const
import apps.utils.function as func

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
    func.print_debug_msg(const.STR_TEST, "非同期処理テスト")


if __name__ == const.MAIN_FUNCTION:
    contents = main()
    func.print_test_data(contents)
