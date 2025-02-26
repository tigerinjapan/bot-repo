# 説明：ニュース情報

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_beautiful_soup as func_bs
import apps.utils.function_gemini as func_gemini

# アプリケーション名
app_name = func.get_app_name(__file__)

# URL
URL_KONEST = "https://www.konest.com"
URL_KSTYLE = "https://kstyle.com"
URL_WOWKOREA = "https://www.wowkorea.jp"
URL_NIKKEI = "https://www.nikkei.com"
URL_ITMEDIA = "https://www.itmedia.co.jp"

# 改行
NEW_LINE = const.SYM_NEW_LINE

# 定数（日本語）
STR_KOREA_JA = "韓国"
STR_ENT_JA = "エンタメ"
STR_NIKKEI_JA = "日経"
STR_AI = "AI"

DIV_NEWS = const.STR_TODAY_JA + "{}" + const.STR_NEWS_JA
DIV_KOREA_NEWS = DIV_NEWS.format(STR_KOREA_JA)
DIV_ENT_NEWS = DIV_NEWS.format(STR_ENT_JA)
DIV_KPOP_RANKING = "週間KPOPランキング"
DIV_KPOP_NEWS = "KPOP" + const.STR_NEWS_JA
DIV_NIKKEI_NEWS = DIV_NEWS.format(STR_NIKKEI_JA)
DIV_AI_NEWS = DIV_NEWS.format(STR_AI)
DIV_AI_NEWS_LIST = [DIV_AI_NEWS]
DIV_NEWS_LIST = [DIV_NIKKEI_NEWS] + DIV_AI_NEWS_LIST
DIV_KOREA_NEWS_LIST = [DIV_KOREA_NEWS, DIV_ENT_NEWS, DIV_KPOP_NEWS]

LIST_KEYWORD_AI = ["AI", "OpenAI", "ChatGPT", "Gemini"]

# タイトル
app_title = DIV_NEWS.format(const.SYM_BLANK)


# データリスト取得
def get_data_list(
    div_list: list[str] = DIV_NEWS_LIST,
) -> list[tuple[list[str], list[str]]]:
    data_list = []

    for div in div_list:
        item_list = get_item_list(div)
        col_list = [div, const.STR_LINK_JA]
        data_info = [col_list, item_list]
        data_list.append(data_info)
    return data_list


# アイテムリスト取得
def get_item_list(div:str):
    item_list = get_news_list(div, list_flg=const.FLG_ON)[: const.MAX_DISPLAY_CNT]
    return item_list


# ニュースメッセージリスト取得
def get_news_msg_list(div_list: list[str]):
    news_msg_list = []
    for div in div_list:
        news_list = get_news_list(div, ai_flg=const.FLG_ON)
        news_msg_list.append(news_list)
    return news_msg_list


# ニュース情報取得
def get_news_list(
    div: str, list_flg: bool = const.FLG_OFF, ai_flg: bool = const.FLG_OFF
) -> list[str]:

    news_list = []

    elem_list = get_elem_list(div)

    if div == DIV_KOREA_NEWS:
        for idx, a in enumerate(elem_list):
            if idx % 2 == 0:
                continue

            a_href = a.get(const.ATTR_HREF)
            url_news = f"{URL_KONEST}/contents/{a_href}"
            a_title = a.get(const.ATTR_TITLE)

            if a_title and func.check_in_list(a_title, ["芸能", "文化", "旅行"]):
                news_contents = a_title
                if ai_flg:
                    news_contents = func_bs.get_elem_from_url(
                        url_news, attr_val="size14"
                    )

                if list_flg:
                    news_contents = [news_contents, url_news]

                news_list.append(news_contents)

    elif div in [DIV_NIKKEI_NEWS, DIV_ENT_NEWS, DIV_KPOP_NEWS]:
        for a in elem_list:
            a_href = a.get(const.ATTR_HREF)
            url = URL_NIKKEI
            if div == DIV_ENT_NEWS:
                url = URL_KSTYLE
            elif div == DIV_KPOP_NEWS:
                url = URL_WOWKOREA

            url_news = f"{url}{a_href}"
            a_text = func.get_replace_data(a.text)
            news_text_list = func.re_split("[…,]", a_text)
            news_contents = NEW_LINE.join(news_text_list)

            if list_flg:
                news_contents = [news_contents, url_news]
            news_list.append(news_contents)

    elif div == DIV_AI_NEWS:
        for a in elem_list:
            a_href = a.get(const.ATTR_HREF)
            a_text = a.text

            if func.check_in_list(a_text, LIST_KEYWORD_AI):
                news_contents = a_text
                if ai_flg:
                    p_list = get_elem_list(div, a_href)
                    news_contents_list = [p.text for p in p_list[:-2]]
                    news_contents = NEW_LINE.join(news_contents_list)

                if list_flg:
                    news_contents = [news_contents, a_href]

                news_list.append(news_contents)

    if ai_flg:
        news_summary = func_gemini.get_news_summary(news_list)
        news_list = [news_summary]

    if not list_flg:
        news_list = NEW_LINE.join(news_list)

    return news_list


# 要素リスト取得
def get_elem_list(div: str, url: str = const.NONE_CONSTANT):
    attr_div = const.ATTR_CLASS
    tag = const.TAG_A

    if div == DIV_NIKKEI_NEWS:
        url = f"{URL_NIKKEI}/access/"
        attr_val = "m-miM32_itemTitleText"

    elif div == DIV_AI_NEWS:
        attr_div = const.ATTR_ID

        if url:
            attr_val = "cmsBody"
            tag = const.TAG_P
        else:
            url = f"{URL_ITMEDIA}/ranking/"
            attr_val = "rank-all"

    elif div == DIV_KOREA_NEWS:
        url = f"{URL_KONEST}/contents/news_top.html"
        attr_val = "mArticleKonest"

    elif div in [DIV_ENT_NEWS, DIV_KPOP_NEWS]:
        url_param = "ranking/day/"
        if div == DIV_KPOP_NEWS:
            url_param = "news/kpop/"

        url = f"{URL_WOWKOREA}/{url_param}"
        attr_val = "card-title h6 h5-sm h3-lg mb-1"

    elif div == DIV_KPOP_RANKING:
        attr_val = "image-wrapper"
        tag = const.TAG_SPAN + '"'

    if URL_NIKKEI in url or URL_WOWKOREA in url:
        elem_list = func_bs.get_elem_from_url(
            url, attr_val=attr_val, list_flg=const.FLG_ON
        )
        elem_list = [func_bs.find_elem_by_attr(elem, tag=tag) for elem in elem_list]

    else:
        elem = func_bs.get_elem_from_url(url, attr_div=attr_div, attr_val=attr_val)
        elem_list = func_bs.find_elem_by_attr(elem, tag=tag, list_flg=const.FLG_ON)

    return elem_list


if __name__ == const.MAIN_FUNCTION:
    data_list = get_data_list()
    print(data_list[0][1])
