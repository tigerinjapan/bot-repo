# 説明：GEMINI関数

import sys

from google import genai

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.message_constants as msg_const

# アプリケーション
app_name = func.get_app_name(__file__)

# GEMINI API情報
GEMINI_MODEL = "gemini-2.0-flash"
GEMINI_API_KEY = func.get_env_val("GEMINI_API_KEY")

# 改行
NEW_LINE = const.SYM_NEW_LINE

# プロパティ
NUM_WRAP_WIDTH = 32


# GEMINI回答取得
def get_gemini_response(contents: str):
    result = []

    curr_def_nm = sys._getframe().f_code.co_name
    response_flg = const.FLG_OFF

    try:
        if GEMINI_API_KEY:
            client = genai.Client(api_key=GEMINI_API_KEY)
            response = client.models.generate_content(
                model=GEMINI_MODEL, contents=contents
            )
            if response:
                response_text = str(response.text)
                result = response_text.split(const.SYM_COMMA)
                response_flg = const.FLG_ON
            else:
                func.print_error_msg(msg_const.MSG_ERR_API_RESPONSE_NONE)
    except ConnectionError as ce:
        func.print_error_msg(curr_def_nm, msg_const.MSG_ERR_API_RESPONSE_NONE)
        func.print_error_msg(f"[ConnectionError] ", str(ce))

    if not response_flg:
        result = ["レスポンス無#1", "レスポンス無#2", "レスポンス無#3"]
    return result


# おすすめコーデ・夕食取得
def get_recommend_outfit_dinner(today_weather: str):
    contents = (
        f"{today_weather}{NEW_LINE}上記の内容を元に、"
        + "気温と季節を考慮し、今日のコーデ・夕食をおすすめしてください。"
    )
    conditions = (
        "※条件1：コーデは、1番目が上着、2番目が中に着るもの"
        + "※条件2：夕食は、1番目が主食、2番目がおかず"
        + "※条件3：コーデ・夕食のそれぞれおすすめしたものを、&で結合"
        + f"※条件4：コーデ・夕食は、コンマ区切り、{NUM_WRAP_WIDTH}バイト未満"
        + "※条件5：解説と他の文言は不要"
    )
    reference = f"※出力例{NEW_LINE}" + "長袖&ダウン,キムパ&キャベツの味噌汁"
    contents += conditions + reference
    recommend_outfit_dinner = get_gemini_response(contents)
    return recommend_outfit_dinner


# ニュース要約取得
def get_news_summary(
    news_list: list[str],
    add_conditions: list[str] = [],
    other_reference: list[str] = [],
    max_count: int = const.MAX_MSG_CNT,
):
    news_item = [str(item) for item in news_list]
    news_item_list = NEW_LINE.join(news_item[:max_count])

    contents = (
        f"{news_item_list}{NEW_LINE}上記のニュース内容を要約してください。{NEW_LINE}"
    )
    conditions = get_news_conditions(add_conditions)
    reference = get_news_reference(other_reference)
    contents += conditions + NEW_LINE + reference

    news_summary = get_gemini_response(contents)
    return news_summary


# ニュース要約条件取得
def get_news_conditions(add_conditions: list[str]) -> str:
    condition_title = ["※条件"]
    condition_list = [
        "記号と絵文字、「。」は、使用しない",
        "英数字は、全て半角に変換",
        f"ニュースは、{const.MAX_MSG_CNT}トピックまで",
        f"ニュース内容と関係ない内容は不要",
        f"1行で、最大{NUM_WRAP_WIDTH}バイト以内",
        "1行ずつ、文章として、完結",
    ]

    if not add_conditions:
        add_conditions = [
            f"各ニュースは、最大{NUM_WRAP_WIDTH * 3}バイト以内",
            "各ニュースの1行目：[ニュースの連番] [キーワード] タイトル",
            "各ニュースの2～3行目：記事",
            "各ニュースの4行目：要約した内容の中で、略語とかIT用語があった場合、その意味を記載",
            "以下出力例のように、解説と他の文言などは不要",
        ]

    condition_list += add_conditions
    conditions = const.SYM_NEW_LINE.join(
        condition_title
        + [f"条件{i+1}：{condition}" for i, condition in enumerate(condition_list)]
    )

    return conditions


# ニュース要約参考取得
def get_news_reference(other_reference: list[str]) -> str:
    reference = [
        "※例",
        f"[1] [Gemini] Geminiの未来{NEW_LINE}議事要約{NEW_LINE}議事要約",
        "※Gemini：Google生成AI",
        f"[2] [DeepSeek] deepSeekのショック{NEW_LINE}議事要約{NEW_LINE}議事要約",
        f"[3] [OpenAI] OpenAIの飛躍{NEW_LINE}議事要約{NEW_LINE}議事要約",
    ]

    if other_reference:
        reference = other_reference

    reference = const.SYM_NEW_LINE.join(reference)
    return reference
