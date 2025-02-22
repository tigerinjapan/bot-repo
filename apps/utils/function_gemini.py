# 説明：GEMINI関数

from google import genai

import apps.utils.constants as const
import apps.utils.function as func

# アプリケーション
app_name = func.get_app_name(__file__)

# GEMINI API情報
GEMINI_MODEL = "gemini-2.0-flash-exp"
GEMINI_API_KEY = func.get_env_val("GEMINI_API_KEY")

# 改行
NEW_LINE = const.SYM_NEW_LINE

# プロパティ
NUM_WRAP_WIDTH = 32
NUM_NEWS_CNT = 3


# GEMINI回答取得
def get_gemini_response(contents: str):
    if GEMINI_API_KEY:
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(model=GEMINI_MODEL, contents=contents)
        result = response.text.split(const.SYM_COMMA)
    else:
        if "天気" in contents:
            result = ["素敵なファッション", "美味しい食事"]
        else:
            result = ["ニュース要約#1", "ニュース要約#2", "ニュース要約#3"]
    return result


# おすすめコーデ・夕食取得
def get_recommend_outfit_dinner(today_weather: str):
    contents = f"{today_weather}{NEW_LINE}上記の内容を元に、気温と季節を考慮し、今日のコーデ・夕食をおすすめしてください。"
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
def get_news_summary(news_list: list[str]):
    news_list = NEW_LINE.join(news_list[:NUM_NEWS_CNT])
    contents = f"{news_list}{NEW_LINE}上記のニュース内容を要約してください。"
    conditions = (
        "※条件1：記号と絵文字、「。」は、使用しない"
        + "※条件2：英数字は、全て半角に変換"
        + f"※条件3：ニュースは、{NUM_NEWS_CNT}トピックまで"
        + f"※条件4：ニュース内容と関係ない内容は不要"
        + f"※条件5：1行で、最大{NUM_WRAP_WIDTH}バイト以内"
        + "※条件6：1行ずつ、文章として、完結"
        + f"※条件7：各ニュースは、最大{NUM_WRAP_WIDTH * 3}バイト以内"
        + "※条件8：各ニュースの1行目：[ニュースの連番] [キーワード] タイトル"
        + "※条件9：各ニュースの2～3行目：記事"
        + "※条件10：各ニュースの4行目：要約した内容の中で、略語とかIT用語があった場合、その意味を記載"
        + "※条件11：以下出力例のように、解説と他の文言などは不要"
    )
    reference = (
        f"※例{NEW_LINE}"
        + f"[1] [Gemini] Geminiの未来{NEW_LINE}議事要約{NEW_LINE}議事要約{NEW_LINE}※Gemini：Google生成AI{NEW_LINE}"
        + f"[2] [deepSeek] deepSeekのショック{NEW_LINE}議事要約{NEW_LINE}議事要約{NEW_LINE}"
    )
    contents += conditions + reference

    news_summary = get_gemini_response(contents)[0]
    return news_summary
