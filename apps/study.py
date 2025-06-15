# 説明: ニュース韓国語

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_beautiful_soup as func_bs
import apps.utils.function_gemini as func_gemini

# アプリケーション名
app_name = func.get_app_name(__file__)

# タイトル
app_title = const.STR_NEWS_JA + const.STR_KOREAN_JA

# カラムリスト
col_list = ["会話", const.STR_KOREAN_JA]

# キーワードリスト
LIST_KEYWORD = func.get_input_data(const.STR_KEYWORD, app_name)

# 改行
NEW_LINE = const.SYM_NEW_LINE

# URL
url_search_param = "/search.naver?where=news&query={}&service_area=1&sort=1"


# データリスト取得
def get_item_list(keyword_list: list[str] = []) -> list[str]:
    item_list = []

    if not keyword_list:
        keyword_list = LIST_KEYWORD

    # retry_cnt = const.MAX_RETRY_CNT # TODO 3回だと、時間かかるため、別方法検討要
    retry_cnt = 1
    for attempt in range(retry_cnt):
        for keyword in keyword_list:
            news_summary = get_naver_news_summary(keyword)
            if not news_summary or len(news_summary) != 3:
                continue

            conversation = news_summary[1]
            korean = news_summary[2]

            if "[1]" in korean:
                study_item = [conversation, korean]
                item_list.append(study_item)

        if item_list:
            break

    return item_list


# NAVERニュース取得
def get_naver_news_summary(keyword: str) -> list[str]:
    news_summary = []

    url_param = url_search_param.format(keyword)
    url = f"{const.URL_NAVER_SEARCH}{url_param}"
    a_elem_list = func_bs.get_elem_from_url(
        url,
        attr_div=const.ATTR_CLASS,
        attr_val="sds-comps-vertical-layout sds-comps-full-layout fds-news-item-list-tab",
    ).find_all(const.TAG_DIV)

    news_list = []
    if a_elem_list:
        for a_elem in a_elem_list:
            time_elem = func_bs.find_elem_by_attr(
                a_elem,
                attr_div=const.ATTR_CLASS,
                attr_val="sds-comps-text sds-comps-text-type-body2 sds-comps-text-weight-sm sds-comps-profile-info-subtext",
            )

            if not time_elem:
                continue
            time_text = time_elem.text

            if func.check_in_list(time_text, ["분 전", "시간 전"]):
                contents_elem_list = func_bs.find_elem_by_attr(
                    a_elem,
                    attr_div=const.ATTR_CLASS,
                    attr_val="sds-comps-text sds-comps-text-ellipsis sds-comps-text-ellipsis-1 sds-comps-text-type-headline1",
                    list_flg=const.FLG_ON,
                )

                for contents_elem in contents_elem_list:
                    contents_text = contents_elem.text
                    if keyword in contents_text:
                        contents_body_text = func_bs.find_elem_by_attr(
                            a_elem,
                            attr_div=const.ATTR_CLASS,
                            attr_val="sds-comps-text sds-comps-text-ellipsis sds-comps-text-ellipsis-3 sds-comps-text-type-body1",
                        ).text
                        contents_text += contents_body_text
                        news_list.append(contents_text)

    if news_list:
        news_summary = func_gemini.get_news_summary(news_list, keyword)

    return news_summary


# 今日の韓国語
def get_today_korean():
    url = f"{const.URL_KONEST}/contents/todays_korean_list.html"
    attr_val = "size12 blackg"
    a_elem = func_bs.get_elem_from_url(url, attr_val=attr_val).find(const.TAG_A)
    today_korean = f"[韓国語] {a_elem[const.ATTR_TITLE]}"[:const.MAX_TEMP_MSG]
    url_korean = f"{const.URL_KONEST}" + a_elem[const.ATTR_HREF]
    return today_korean, url_korean


if __name__ == const.MAIN_FUNCTION:
    item_list = get_item_list()
    func.print_test_data(item_list)
