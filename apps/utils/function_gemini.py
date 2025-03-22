# 説明：GEMINI関数

import sys

from google import genai
from google.genai.errors import ServerError

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.message_constants as msg_const

# アプリケーション
app_name = func.get_app_name(__file__)

# GEMINI API情報
GEMINI_MODEL = func.get_env_val("GEMINI_MODEL")
GEMINI_API_KEY = func.get_env_val("GEMINI_API_KEY")

# 改行
NEW_LINE = const.SYM_NEW_LINE

# プロパティ
NUM_WRAP_WIDTH = 32


# GEMINI回答取得
def get_gemini_response(contents: str):
    result = []
    exception_error = const.SYM_BLANK

    try:
        result = get_generate_content(contents)
    except:
        try:
            result = get_generate_content(contents)
        except ConnectionError as ce:
            exception_error = f"ConnectionError, {str(ce)}"
        except ServerError as se:
            exception_error = f"ServerError, {str(se)}"
        except Exception as e:
            exception_error = f"Exception, {str(e)}"

    if exception_error:
        curr_def_nm = sys._getframe().f_code.co_name
        func.print_error_msg(curr_def_nm, msg_const.MSG_ERR_API_RESPONSE_NONE)
        func.print_error_msg(exception_error)
        result = [f"Geminiレスポンスエラー#{i+1}" for i in range(3)]
    return result


# 生成コンテンツ取得
def get_generate_content(contents: str):
    result = []

    if GEMINI_API_KEY:
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(model=GEMINI_MODEL, contents=contents)
        if response:
            response_text = str(response.text)
            result = response_text.split(const.SYM_COMMA)
        else:
            func.print_error_msg(msg_const.MSG_ERR_API_RESPONSE_NONE)

    return result


# おすすめコーデ・夕食取得
def get_recommend_outfit_dinner(today_weather: str):
    contents = (
        f"{today_weather}{NEW_LINE}上記の内容を元に、"
        + "気温と季節を考慮し、今日のコーデ・夕食をおすすめしてください。"
    )
    condition_list = [
        "コーデは、1番目が上着、2番目が中に着るもの",
        "夕食は、1番目が主食、2番目がおかず",
        "コーデ・夕食のそれぞれおすすめしたものを、&で結合",
        f"コーデ・夕食は、コンマ区切り、{NUM_WRAP_WIDTH}バイト未満",
        "文章の終わりに絵文字を使用。言葉の代わりには使用しない",
        "絵文字は、環境依存せず、全てのデバイスに適用されるものにする",
        "解説と他の文言は不要",
    ]
    conditions = get_prompt_conditions(condition_list)
    reference = f"※出力例{NEW_LINE}" + "長袖&ダウン,キムパ&キャベツの味噌汁"
    contents += conditions + reference
    recommend_outfit_dinner = get_gemini_response(contents)
    return recommend_outfit_dinner


# ニュース要約取得
def get_news_summary(
    news_list: list[str],
    keyword: str = const.SYM_BLANK,
    max_count: int = const.MIN_DISPLAY_CNT,
):
    news_item = [str(item) for item in news_list]
    news_item_list = NEW_LINE.join(news_item[:max_count])

    contents = (
        f"{news_item_list}{NEW_LINE}上記のニュース内容を要約してください。{NEW_LINE}"
    )

    if keyword:
        add_condition_list = get_add_condition_list()
        other_reference = get_other_reference()
    else:
        add_condition_list = []
        other_reference = []

    conditions = get_news_conditions(add_condition_list)
    reference = get_news_reference(other_reference)
    contents += conditions + NEW_LINE + reference

    news_summary = get_gemini_response(contents)
    return news_summary


# ニュース要約条件取得
def get_news_conditions(add_condition_list: list[str]) -> str:
    condition_list = [
        "記号と絵文字、「。」は、使用しない",
        "英数字は、全て半角に変換",
        f"ニュースは、{const.MIN_DISPLAY_CNT}トピックまで",
        f"ニュース内容と関係ない内容は不要",
        f"1行で、最大{NUM_WRAP_WIDTH}バイト以内",
        "1行ずつ、文章として、完結",
    ]

    if not add_condition_list:
        add_condition_list = [
            f"各ニュースは、最大{NUM_WRAP_WIDTH * 3}バイト以内",
            "各ニュースの1行目：[ニュースの連番] [キーワード] タイトル",
            "各ニュースの2～3行目：記事",
            "各ニュースの4行目：要約した内容の中で、略語とかIT用語があった場合、その意味を記載",
            "以下出力例のように、解説と他の文言などは不要",
        ]

    conditions = get_prompt_conditions(condition_list, add_condition_list)
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


# 追加条件取得
def get_add_condition_list():
    add_condition_list = [
        "韓国語を勉強している初級レベルの人が記事を学習用で使用する目的",
        "【会話】記事の内容を元に韓国人同士が会話する内容",
        "【会話】会話の中で、記事が何の内容かを全て把握したい",
        f"【会話】会話の中で、検索したキーワードを一度は使用",
        f"【会話】会話の中で、説明する韓国語熟語は、<b>と</b>に囲む",
        "【会話】20文字以内",
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
    return add_condition_list


# 追加参考取得
def get_other_reference():
    other_reference = [
        "※例",
        "유리：<b>오빠들</b>이 <b>음악프로</b> 1등했데.",
        "창빈：<b>대단하다.</b> 정말 축해.",
        "유리：다음 노래도 1위 했음 좋겠다.",
        "창빈：그래.",
        "유리：다음 달에는 월드투어도 한데.",
        "창빈：일본에서 콘서트 하는거 보고싶다.",
        NEW_LINE * 2,
        "[1] 오빠들",
        "お兄ちゃんたち。",
        "[2] 음악프로",
        "音楽番組",
        "[3] 대단하다",
        "凄い",
        "[4] 그래",
        "そうね。そうだね。",
        "[5] 보고싶다",
        "見たい",
    ]
    return other_reference


# プロンプト条件取得
def get_prompt_conditions(
    condition_list: list[str], add_condition_list: list[str] = []
) -> str:
    condition_title = ["※条件"]
    condition_list_all = condition_list + add_condition_list
    prompt_conditions = const.SYM_NEW_LINE.join(
        condition_title
        + [f"条件{i+1}：{condition}" for i, condition in enumerate(condition_list_all)]
    )
    return prompt_conditions
