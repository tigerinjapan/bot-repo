# 説明: GEMINI関数

import sys

from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

from google import genai
from google.genai import types
from google.genai.errors import ServerError

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.message_constants as msg_const

# アプリケーション
app_name = func.get_app_name(__file__)

# GEMINI API情報
GEMINI_API_KEY = func.get_env_val("GEMINI_API_KEY")
GEMINI_MODEL = func.get_env_val("GEMINI_MODEL")
GEMINI_MODEL_IMG = func.get_env_val("GEMINI_MODEL_IMG")

# 改行
NEW_LINE = const.SYM_NEW_LINE

# プロパティ
NUM_WRAP_WIDTH = 32


# GEMINI回答取得
def get_gemini_response(contents):
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
def get_generate_content(contents):
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


# 生成イメージ取得
def get_generate_image(div: str, contents: str, msg_data) -> str:
    file_path = const.SYM_BLANK

    client = genai.Client(api_key=GEMINI_API_KEY)

    # サンプル
    # contents = (
    #     "Hi, can you create a 3d rendered image of a pig "
    #     "with wings and a top hat flying over a happy "
    #     "futuristic city with lots of greenery?"
    # )

    exception_error = const.SYM_BLANK

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL_IMG,
            contents=contents,
            config=types.GenerateContentConfig(response_modalities=["Text", "Image"]),
        )

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
        return file_path

    for part in response.candidates[0].content.parts:
        if part.text is not None:
            continue
        elif part.inline_data is not None:
            # div = const.DATE_NOW + str(idx).zfill(3)
            file_path = func.get_file_path(div, const.FILE_TYPE_JPEG, const.STR_OUTPUT)
            image_open = Image.open(BytesIO((part.inline_data.data)))
            if msg_data:
                msg = msg_data["msg"]
                font_type = msg_data["font_type"]
                font_size = msg_data["font_size"]
                xy_size = msg_data["xy_size"]

                draw = ImageDraw.Draw(image_open)

                font_path = func.get_file_path(font_type, const.FILE_TYPE_TTC)
                font = ImageFont.truetype(font=font_path, size=font_size)

                draw.text(xy=xy_size, text=msg, fill="black", font=font, align="left")

            size = (480, 360)
            img = image_open.resize(size)
            img.save(file_path, optimize=const.FLG_ON)
            break

    return file_path


# ニュースイメージ取得
def get_today_news_image(forecast: str, msg: str):
    div = const.APP_TODAY
    img_div = "女性"

    contents = (
        "空白で何も表示されていない画面がある。"
        "その画面は、テレビ放送用の大きいモニター画面である。"
        "モニターは、完成イメージの9割を占める。"
        "番組名は、「Today's Morning News」である。"
        "番組ロゴは、モニター画面の中で、左上に表示する。"
        f"背景は、「{forecast}」が分かるようなイメージにする。"
        "但し、黒字がよく見えるように、黒系の色は避ける。"
        f"天気キャスターの{img_div}が、モニター画面の中で、右下にいる。"
        f"{img_div}は、白いブラウスに、清楚な格好をしている。"
        f"{img_div}は、50代の日本人で、童顔で、笑顔が素敵で、明るくて、可愛い人。"
        "イメージのサイズは、480ピクセル X 360ピクセル。"
        "イメージを縦で3等分した場合、右側の1/3の中に、女性が収まるようにする。"
        "そのサイズに合わせて、イメージを生成。"
        "イメージには、日本語、漢字などは、表示しない。"
    )

    today_weather = "sunny"
    if "雨" in forecast:
        today_weather = "rainy"
    elif "雪" in forecast:
        today_weather = "snowy"
    elif "曇" in forecast:
        today_weather = "cloudy"
    contents = (
        "A blank screen with nothing displayed is visible."
        "The full screen is a large monitor used for television broadcasting."
        "The monitor accounts for 90percent of the final image perception."
        "The program's name is 'Today's News.'"
        "The program's name should be displayed in the top-left of the monitor screen."
        f"The background should be an image that conveys the idea of '{today_weather}'."
        "However, to ensure that black text is clearly visible, black-based colors should be avoided."
        "The weather caster woman should be positioned in the bottom-right corner of the monitor screen."
        "The woman is dressed neatly in a white blouse, giving her a modest and elegant appearance."
        "The woman is a Japanese woman in her fifties, a baby face, a lovely smile, and a bright, cheerful personality. She’s very cute and charming."
        "The image size should be 480 pixels by 360 pixels."
        "If the image is divided vertically into thirds, place the woman within the rightmost one-third of the image."
        "Generate the image according to this size."
        "The image should not display any Japanese text or kanji."
    )
    msg_data = {
        "msg": msg,
        "font_type": "uzura",
        "font_size": 28,
        "xy_size": (100, 160),
    }
    file_path = get_generate_image(div, contents, msg_data)
    return file_path


# おすすめコーデ・夕食取得
def get_recommend_outfit_dinner(today_weather: str):
    contents = (
        f"{today_weather}{NEW_LINE}上記の内容を元に、"
        "気温と季節を考慮し、今日のコーデ・夕食をおすすめしてください。"
    )
    condition_list = [
        "コーデは、1番目が上着、2番目が中に着るもの",
        "夕食は、1番目が主食、2番目がおかず",
        "コーデ・夕食のそれぞれおすすめしたものを、&で結合",
        f"コーデ・夕食は、コンマ区切り、{NUM_WRAP_WIDTH}バイト未満",
        "解説と他の文言は不要",
    ]
    conditions = get_prompt_conditions(condition_list)
    reference = f"※出力例{NEW_LINE}" + "長袖&ダウン,キムパ&キャベツの味噌汁"
    contents += conditions + reference
    recommend_outfit_dinner = get_gemini_response(contents)
    return recommend_outfit_dinner


# おすすめコーデ取得
def get_recommend_outfit(outfit_text: str):
    contents = (
        f"{outfit_text}{NEW_LINE}"
        "上記の内容を元に、今日のコーデをおすすめしてください。"
        "コーデは、2アイテム。1番目が上半身、2番目が下半身に着るもの。"
        "各アイテムは、&で繋げる。"
        f"全体の文字数は、16桁未満。"
        "解説と他の文言、記号は不要。"
        f"※出力例{NEW_LINE}白いTシャツ&デニムジーンズ"
    )
    recommend_outfit = get_gemini_response(contents)[0].replace(
        const.SYM_NEW_LINE, const.SYM_BLANK
    )
    return recommend_outfit


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
        add_condition_list = get_add_condition_list(keyword)
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
            "各ニュースの1行目: [ニュースの連番] [キーワード] タイトル",
            "各ニュースの2～3行目: 記事",
            "各ニュースの4行目: 要約した内容の中で、略語とかIT用語があった場合、その意味を記載",
            "以下出力例のように、解説と他の文言などは不要",
        ]

    conditions = get_prompt_conditions(condition_list, add_condition_list)
    return conditions


# ニュース要約参考取得
def get_news_reference(other_reference: list[str]) -> str:
    reference = [
        "※例",
        f"[1] [Gemini] Geminiの未来{NEW_LINE}議事要約{NEW_LINE}議事要約",
        "※Gemini: Google生成AI",
        f"[2] [DeepSeek] deepSeekのショック{NEW_LINE}議事要約{NEW_LINE}議事要約",
        f"[3] [OpenAI] OpenAIの飛躍{NEW_LINE}議事要約{NEW_LINE}議事要約",
    ]

    if other_reference:
        reference = other_reference

    reference = const.SYM_NEW_LINE.join(reference)
    return reference


# 追加条件取得
def get_add_condition_list(keyword: str):
    add_condition_list = [
        "韓国語を勉強している初級レベルの人が記事を学習用で使用する目的",
        "【会話】記事の内容を元に韓国人同士が会話する内容",
        "【会話】会話の中で、記事が何の内容かを全て把握したい",
        f"【会話】会話の中で、{keyword}を一度は使用",
        "【会話】会話の中で、説明する韓国語熟語は、太字にする: <b>と</b>に囲む",
        "【会話】文章の終わりに絵文字を使用。言葉の代わりには使用しない",
        "【会話】絵文字は、環境依存せず、全てのデバイスに適用されるものにする",
        "【会話】連番を付けない",
        "【熟語】会話の途中にある熟語で、日常でよく使う表現5個をピックアップし、説明",
        "【熟語】韓国語熟語は、純ハングル語、韓国式略語、韓国式英語の優先順位",
        "【熟語】日本語で直訳すると、同じ意味の韓国語は、対象外",
        "【熟語】韓国語熟語の説明は、日本語と同じ表現を使用",
        "【熟語】韓国語熟語の説明は、日本語以外の言語は、不要",
        f"1行に、{NUM_WRAP_WIDTH}バイト未満",
        "使用しない: *、コンマ、【会話】、【熟語】、대화、숙어",
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
        "유리: <b>오빠들</b>, <b>음악프로</b> 1등했데.",
        "창빈: <b>대단하다</b>. 정말 축하해.",
        "유리: 다음 노래도 1위 했음 좋겠다.",
        "창빈: <b>그래</b>.",
        "유리: 일본에서 콘서트 <b>보고싶다</b>.",
        "창빈: 그랬으면 좋겠네.",
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
        + [f"条件{i+1}: {condition}" for i, condition in enumerate(condition_list_all)]
    )
    return prompt_conditions


# テスト
def test_gemini():
    contents = "これからの未来について、100文字以内で説明お願いします。"
    response = get_gemini_response(contents)
    result = const.SYM_NEW_LINE.join(response)
    func.print_test_data(result)


# テストイメージ #TODO 現在、無料版では実装不可
def test_gemini_image():
    # クライアントの初期化
    client = genai.Client(api_key=GEMINI_API_KEY)

    # イメージ生成リクエストの送信
    try:
        response = client.models.generate_images(
            model="imagen-3.0-generate-002",  # 無料版で利用可能なモデル名を確認
            prompt="A serene landscape with mountains and a clear blue lake",  # イメージの説明
            # size="360x360",  # 対応する画像サイズを指定
        )

        for generated_image in response.generated_images:
            image = Image.open(BytesIO(generated_image.image.image_bytes))
            image.show()

        # レスポンスから生成された画像URLを取得
        if response and "image_url" in response:
            func.print_test_data(f"Generated Image URL: {response['image_url']}")
        else:
            func.print_test_data(
                "Image generation failed or not available in the free version."
            )
    except Exception as e:
        func.print_error_msg(e)


if __name__ == const.MAIN_FUNCTION:
    # test_gemini()
    # test_gemini_image()
    today_weather = "晴れのち曇り"
    msg = "[test] test"
    get_today_news_image(today_weather, msg)
