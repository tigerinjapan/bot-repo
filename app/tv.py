# 説明：TV番組検索

import utils.constants as const
import utils.function as func
import utils.function_beautiful_soup as func_bs

# アプリケーション名
app_name = func.get_app_name(__file__)

# タイトル
app_title = "韓国TV番組"

# URL
URL_TV = "https://www.tvkingdom.jp"

# カラムリスト
COL_LIST = ["放送時間", "番組名", "チャンネル"]

# 検索キーワード
KEYWORD_KOREA = "韓国"

# URL
URL_PARAM = (
    "schedulesBySearch.action?stationPlatformId=1"
    + "&condition.keyword={}&submit=%E6%A4%9C%E7%B4%A2"
)


# データリスト取得
def get_data_list(keyword: str = KEYWORD_KOREA) -> list[tuple[list[str], list[str]]]:
    data_list = []
    tv_info_list = get_tv_info_list(keyword)
    data_info = [COL_LIST, tv_info_list]
    data_list.append(data_info)
    return data_list


# TV番組情報取得
def get_tv_info_list(keyword) -> list[str]:
    tv_info_list = []

    url = f"{URL_TV}/{URL_PARAM}".format(keyword)
    soup = func_bs.get_elem_from_url(
        url, const.TAG_FORM, const.STR_NAME, "form_multi_iepg"
    )
    title_list = func_bs.find_elem_by_attr(
        soup, tag=const.TAG_H2, list_flg=const.FLG_ON
    )
    program_list = func_bs.find_elem_by_attr(
        soup,
        attr_div=const.ATTR_CLASS,
        attr_val="utileListProperty",
        list_flg=const.FLG_ON,
    )

    for title, program in zip(title_list, program_list):
        title = func.convert_half_char(title.text)
        tv_info_txt = (
            func.convert_half_char(program.text)
            .replace(const.SYM_SPACE, const.SYM_BLANK)
            .split("\r\n")
        )
        time = tv_info_txt[1]
        min = time.split("分")[0].split("(")[-1]
        hour = time.split(")")[1].split(":")[0]
        if 20 <= int(min) and 8 <= int(hour):
            channel = tv_info_txt[2]
            tv_info = [time, title, channel]
            tv_info_list.append(tv_info)

    return tv_info_list


if __name__ == const.MAIN_FUNCTION:
    data_list = get_data_list()
    print(data_list[0][1])
