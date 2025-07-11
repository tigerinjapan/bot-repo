# 説明: ニュース情報

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_beautiful_soup as func_bs
import apps.utils.function_gemini as func_gemini

# アプリケーション名
app_name = func.get_app_name(__file__)

# タイトル
app_title = "今日の" + const.STR_NEWS_JA

# カラムリスト
col_list = [const.STR_DIV_JA, app_title]

# 改行
NEW_LINE = const.SYM_NEW_LINE

# 区分
DIV_NEWS = "{}" + const.STR_NEWS_JA
DIV_NIKKEI_NEWS = DIV_NEWS.format(const.STR_NIKKEI_JA)
DIV_KOREA_NEWS = DIV_NEWS.format(const.STR_KOREA_JA)
DIV_ENT_NEWS = DIV_NEWS.format(const.STR_ENT_JA)
DIV_KPOP_NEWS = DIV_NEWS.format(const.STR_KPOP)
DIV_AI_NEWS = DIV_NEWS.format(const.STR_AI)
DIV_AI_NEWS_LIST = [DIV_AI_NEWS]
DIV_NEWS_LIST = [
    DIV_NIKKEI_NEWS,
    DIV_AI_NEWS,
    DIV_KOREA_NEWS,
    DIV_ENT_NEWS,
    DIV_KPOP_NEWS,
]

ITEM_NEWS_LIST = [
    const.STR_NIKKEI_JA,
    const.STR_AI,
    const.STR_KOREA_JA,
    const.STR_ENT_JA,
    const.STR_KPOP,
]

DIV_WEEKLY_RANKING = "{}週間" + const.STR_RANKING_JA
DIV_KPOP_RANKING = DIV_WEEKLY_RANKING.format(const.STR_KPOP)

# キーワードリスト
LIST_KEYWORD_AI = func.get_input_data(const.STR_KEYWORD, const.STR_AI)


# アイテムリスト取得
def get_item_list():
    item_list = []

    for div, item_div in zip(DIV_NEWS_LIST, ITEM_NEWS_LIST):
        news_list = get_news_list(div, list_flg=const.FLG_ON)
        if news_list:
            print_news_list = news_list[:1]
            for news in print_news_list:
                news = news.insert(0, item_div)
            item_list += print_news_list

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
    div: str,
    list_flg: bool = const.FLG_OFF,
    url_flg: bool = const.FLG_OFF,
    ai_flg: bool = const.FLG_OFF,
):

    news_list = []

    elem_list = get_elem_list(div)

    if not elem_list:
        return news_list

    if div == DIV_KOREA_NEWS:
        for idx, a in enumerate(elem_list):
            if not a or idx % 2 == 0:
                continue

            a_title = a.get(const.ATTR_TITLE)
            if a_title and func.check_in_list(a_title, ["芸能", "旅行"]):
                news_text_list = func.re_split("[…,]", func.get_replace_data(a_title))
                news_text = NEW_LINE.join(news_text_list)

                a_href = a.get(const.ATTR_HREF)
                url_news = f"{const.URL_KONEST}/contents/{a_href}"

                news_contents = func.get_a_tag(url_news, news_text)

                if list_flg:
                    news_contents = [news_contents]

                news_list.append(news_contents)

    elif div in [DIV_NIKKEI_NEWS, DIV_ENT_NEWS, DIV_KPOP_NEWS]:
        for a in elem_list:
            if not a:
                continue

            a_href = a.get(const.ATTR_HREF)
            url = const.URL_WOWKOREA
            if div == DIV_NIKKEI_NEWS:
                url = const.URL_NIKKEI

            url_news = f"{url}{a_href}"

            a_text = a.text
            if a_text:
                news_text_list = func.re_split("[…,、]", func.get_replace_data(a_text))
                news_text = NEW_LINE.join(news_text_list)

                news_contents = func.get_a_tag(url_news, news_text)

                if url_flg:
                    news_title = f"[{const.STR_NIKKEI_JA}] {news_text}"[
                        : const.MAX_TEMP_MSG
                    ]
                    return news_title, url_news

                if list_flg:
                    news_contents = [news_contents]

                news_list.append(news_contents)

    elif div == DIV_AI_NEWS:
        for a in elem_list:
            if not a:
                continue

            a_href = a.get(const.ATTR_HREF)
            a_text = a.text

            if func.check_in_list(a_text, LIST_KEYWORD_AI):
                news_text = func.get_replace_data(a_text).replace(
                    const.SYM_SPACE, const.SYM_BLANK
                )
                news_contents = func.get_a_tag(a_href, news_text)

                if url_flg:
                    news_title = f"[{const.STR_AI}] {news_text}"[: const.MAX_TEMP_MSG]
                    return news_title, a_href

                if ai_flg:
                    p_list = get_elem_list(div, a_href)
                    if p_list:
                        news_contents_list = [p.text for p in p_list[:-2] if p]
                        news_contents = NEW_LINE.join(news_contents_list)

                if list_flg:
                    news_contents = [news_contents]

                news_list.append(news_contents)

    if ai_flg:
        news_summary = func_gemini.get_news_summary(news_list)[0]
        news_list = [news_summary]

    if not list_flg:
        news_list = NEW_LINE.join(news_list)

    return news_list


# 要素リスト取得
def get_elem_list(div: str, url: str = const.SYM_BLANK):
    attr_div = const.ATTR_CLASS
    attr_val = const.SYM_BLANK
    tag = const.TAG_A

    if div == DIV_NIKKEI_NEWS:
        url = f"{const.URL_NIKKEI}/access/"
        attr_val = "m-miM32_itemTitleText"

    elif div == DIV_AI_NEWS:
        attr_div = const.ATTR_ID

        if url:
            attr_val = "cmsBody"
            tag = const.TAG_P
        else:
            url = f"{const.URL_ITMEDIA}/ranking/"
            attr_val = "rank-all"

    elif div == DIV_KOREA_NEWS:
        url = f"{const.URL_KONEST}/contents/news_top.html"
        attr_val = "mArticleKonest"

    elif div in [DIV_ENT_NEWS, DIV_KPOP_NEWS]:
        url_param = "ranking/day/"
        if div == DIV_KPOP_NEWS:
            url_param = "news/kpop/"

        url = f"{const.URL_WOWKOREA}/{url_param}"
        attr_val = "card-title h6 h5-sm h3-lg mb-1"

    elif div == DIV_KPOP_RANKING:
        attr_val = "image-wrapper"
        tag = const.TAG_SPAN + '"'

    if const.URL_NIKKEI in url or const.URL_WOWKOREA in url:
        elem_list_org = func_bs.get_elem_from_url(
            url, attr_val=attr_val, list_flg=const.FLG_ON
        )
        if elem_list_org:
            if div == DIV_KPOP_RANKING:
                elem_list = [elem.contents[2] for elem in elem_list_org]
            else:
                elem_list = [
                    func_bs.find_elem_by_attr(elem, tag=tag) for elem in elem_list_org
                ]
        else:
            elem_list = []

    else:
        elem = func_bs.get_elem_from_url(url, attr_div=attr_div, attr_val=attr_val)
        elem_list = func_bs.find_elem_by_attr(elem, tag=tag, list_flg=const.FLG_ON)

    return elem_list


if __name__ == const.MAIN_FUNCTION:
    item_list = get_item_list()
    func.print_test_data(item_list)
