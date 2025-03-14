# 説明：ニュース韓国語

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.function_beautiful_soup as func_bs
import apps.utils.function_gemini as func_gemini

# アプリケーション名
app_name = func.get_app_name(__file__)

# 定数
STR_KOREAN_JA = "韓国語"

# タイトル
app_title = const.STR_NEWS_JA + STR_KOREAN_JA

# カラムリスト
col_list = ["会話", STR_KOREAN_JA]

# キーワードリスト
LIST_KEYWORD = func.get_input_data(const.STR_KEYWORD, app_name)

# 改行
NEW_LINE = const.SYM_NEW_LINE

# URL
URL_NAVER_SEARCH = "https://search.naver.com"
url_search_param = "/search.naver?where=news&query={}&service_area=1&sort=1"


# データリスト取得
def get_item_list(keyword_list: list[str] = []) -> list[str]:
    item_list = []

    if not keyword_list:
        keyword_list = LIST_KEYWORD

    for attempt in range(const.MAX_RETRY_CNT):
        for keyword in keyword_list:
            news_summary = get_naver_news_summary(keyword)
            if not news_summary:
                continue

            study_info = news_summary[0].split(NEW_LINE * 2)
            try:
                korean = study_info[1]
            except:
                continue

            if korean and "[1]" in korean and len(study_info) == 2:
                item_list.append(study_info)

        if item_list:
            break

    return item_list


# NAVERニュース取得
def get_naver_news_summary(keyword: str) -> list[str]:
    news_summary = []

    url_param = url_search_param.format(keyword)
    url = f"{URL_NAVER_SEARCH}{url_param}"
    a_elem_list = func_bs.get_elem_from_url(
        url, attr_val="news_area", list_flg=const.FLG_ON
    )[: const.MAX_DISPLAY_CNT]  # type: ignore

    naver_news = []
    if a_elem_list:
        for a_elem in a_elem_list:
            time_elem = func_bs.find_elem_by_attr(
                a_elem, const.TAG_SPAN, attr_div=const.ATTR_CLASS, attr_val="info"
            )
            time_text = time_elem.text  # type: ignore
            if func.check_in_list(time_text, ["분 전", "시간 전"]):
                contents_elem = func_bs.find_elem_by_attr(
                    a_elem,
                    attr_div=const.ATTR_CLASS,
                    attr_val="api_txt_lines dsc_txt_wrap",
                )
                contents_text = contents_elem.text  # type: ignore
                naver_news.append(contents_text)

    if naver_news:
        add_conditions = [
            "韓国語を勉強している初級レベルの人が記事を学習用で使用する目的",
            "【会話】記事の内容を元に韓国人の女性同士が会話するような内容",
            "【会話】会話の中で、記事が何の内容かを全て把握したい",
            f"【会話】会話の中で、「{keyword}」というキーワードを一度は使用",
            f"【会話】会話の中で、「{keyword}」と説明する韓国語熟語は、<b>と</b>に囲む",
            "【会話】文章の終わりに絵文字を使用。言葉の代わりには使用しない",
            "【会話】絵文字は、環境依存せず、全てのデバイスに適用されるものにする",
            "【熟語】会話の途中にある熟語で、日常でよく使う表現5個をピックアップし、説明",
            "【熟語】韓国語熟語は、純ハングル語、韓国式略語、韓国式英語の優先順位",
            "【熟語】日本語で直訳すると、同じ意味の韓国語は、対象外",
            "【熟語】韓国語熟語の説明は、日本語と同じ表現を使い、20文字以内",
            "【熟語】韓国語熟語の説明は、日本語以外の言語は、不要",
            "使用しない：**、コンマ",
            "小数点、4桁以上などの数値の内容は、不要",
            "日本語、韓国語、英語以外の言語は、不要",
            "알겠습니다. 요약해 드리겠습니다. などの内容は、不要",
            "以下例のように、レイアウトを構成する",
        ]

        other_reference = [
            "※例",
            "유리：이번에 우리 오빠들이 <b>음악</b>프로그램 1위를 했데.",
            "창빈：대단하다. 정말 축해.",
            "유리：다음 노래도 1위 했음 좋겠다.",
            "창빈：그래.",
            "유리：다음 달에는 월드투어도 한다네.",
            "창빈：미국이나 일본에서 콘서트 하는거 보고싶다.",
            NEW_LINE * 2,
            "[1] 오빠들：お兄ちゃんたち。",
            "[2] 프로그램：番組、プログラム",
            "[3] 대단하다：凄い",
            "[4] 그래：そうね。そうだね。",
            "[5] 보고싶다：見たい",
        ]
        news_summary = func_gemini.get_news_summary(
            naver_news, add_conditions, other_reference, 1
        )

    return news_summary


if __name__ == const.MAIN_FUNCTION:
    item_list = get_item_list()
    func.print_test_data(item_list)
