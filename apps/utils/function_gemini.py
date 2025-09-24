# 説明: GEMINI関数

import sys
import time

from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

from google import genai
from google.genai import types
from google.genai.errors import ServerError

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.message_constants as msg_const

# スクリプト名
SCRIPT_NAME = func.get_app_name(__file__)

# アプリケーション名
app_name = const.STR_GEMINI

# GEMINI API情報
GEMINI_API_KEY = func.get_env_val("GEMINI_API_KEY")
GEMINI_MODEL = func.get_env_val("GEMINI_MODEL")
GEMINI_MODEL_IMG = func.get_env_val("GEMINI_MODEL_IMG")

# 改行
NEW_LINE = const.SYM_NEW_LINE

# プロパティ
NUM_WRAP_WIDTH = 32


# クライアント取得
def get_client():
    try:
        if not GEMINI_API_KEY:
            raise Exception

        client = genai.Client(api_key=GEMINI_API_KEY)
        return client
    except Exception as e:
        curr_func_nm = sys._getframe().f_code.co_name
        func.print_error_msg(
            SCRIPT_NAME,
            curr_func_nm,
            msg_const.MSG_ERR_CONNECTION_FAILED,
            str(e),
            sys_exit=const.FLG_ON,
        )


# GEMINI回答取得
def get_gemini_response(
    func_name: str, contents, model: str = GEMINI_MODEL, config=const.NONE_CONSTANT
) -> list[str]:
    curr_func_nm = sys._getframe().f_code.co_name

    div_msg = f"[{app_name}] {func_name}"
    func.print_start(div_msg)

    result = []
    exception_error = const.SYM_BLANK

    try:
        client = get_client()
        response = client.models.generate_content(
            model=model, contents=contents, config=config
        )

        if response:
            if model == GEMINI_MODEL_IMG:
                func.print_end(div_msg)
                return response

            response_text = str(response.text)
            split_str = const.SYM_NEW_LINE * 2
            if split_str not in response_text:
                split_str = const.SYM_COMMA
            result = response_text.split(split_str)

    except ConnectionError as ce:
        exception_error = ["ConnectionError", ce]
    except ServerError as se:
        exception_error = ["ServerError", se]
    except Exception as e:
        exception_error = ["Exception", e]

    if exception_error:
        func.print_error_msg(
            SCRIPT_NAME, curr_func_nm, exception_error[0], exception_error[1]
        )

    if not result:
        func.print_error_msg(
            SCRIPT_NAME, curr_func_nm, msg_const.MSG_ERR_API_RESPONSE_NONE
        )

    func.print_end(div_msg)
    return result


# 生成イメージ取得
def get_gemini_image(
    div: str = const.STR_GEMINI, contents: str = const.SYM_BLANK
) -> str:
    if not contents:
        contents = get_sample_contents(div)
    file_path = get_generate_text_image(div, contents)
    return file_path


# 生成イメージ取得
def get_generate_text_image(
    div: str, contents: str, model: str = GEMINI_MODEL_IMG, msg_data=const.NONE_CONSTANT
) -> str:
    file_path = const.SYM_BLANK

    try:
        config = types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"])
        response = get_gemini_response("today_news_image", contents, model, config)
    except Exception as e:
        func.print_error_msg(SCRIPT_NAME, model, div, e)
        response = const.NONE_CONSTANT

    if not response:
        return file_path

    for part in response.candidates[0].content.parts:
        if part.text:
            continue
        elif part.inline_data:
            file_path = func.get_file_path(div, const.FILE_TYPE_JPEG, const.STR_OUTPUT)
            image_open = Image.open(BytesIO((part.inline_data.data)))
            if msg_data:
                msg = msg_data["msg"]
                font_type = msg_data["font_type"]
                font_size = msg_data["font_size"]
                xy_size = msg_data["xy_size"]

                font_path = func.get_file_path(font_type, const.FILE_TYPE_TTC)
                font = ImageFont.truetype(font=font_path, size=font_size)

                draw = ImageDraw.Draw(image_open)

                # 【レビュー対応#11】文字の外枠を、whiteになる #
                # 外枠の色と文字の色
                outline_color = "white"
                text_color = "black"

                # 外枠を描画
                x = xy_size[0]
                y = xy_size[1]
                for dx in [-2, 0, 2]:
                    for dy in [-2, 0, 2]:
                        if dx != 0 or dy != 0:  # 中心はスキップ
                            draw.text(
                                (x + dx, y + dy), msg, font=font, fill=outline_color
                            )

                draw.text(
                    xy=xy_size, text=msg, fill=text_color, font=font, align="left"
                )

            size = (const.LINE_IMG_SIZE_W, const.LINE_IMG_SIZE_H)
            img = image_open.resize(size)
            img.save(file_path, optimize=const.FLG_ON)
            image_open.close()
            break

    if not file_path:
        func.print_info_msg(model, msg_const.MSG_ERR_API_RESPONSE_NONE)

    return file_path


# ニュースイメージ取得
def get_today_news_image(
    msg: str, forecast: str, today_outfit: str, img_div: str = const.STR_WOMAN_JA
) -> str:
    div = const.APP_TODAY

    contents_outfit = img_woman = const.SYM_BLANK
    if today_outfit:
        if img_div == const.STR_WOMAN_JA:
            img_woman = (
                f"{img_div}は、45才の日本人。身長は155cm、体重は50kg。"
                "小柄、童顔、笑顔、可愛い、愛嬌溢れる、優しい人。"
                f"{img_div}のメークアップは、自然なナチュラルタイプ。"
                f"{img_div}の身体のボリューム感を強調する大胆なファッションにする。"
            )

        contents_outfit = (
            f"天気キャスターの{img_div}が一人いる。"
            f"{img_woman}"
            f"{img_div}は、全体イメージの、右寄りに配置する。"
            f"{img_div}は、{const.LINE_IMG_X_AXIS}px * {const.LINE_IMG_Y_AXIS}pxに配置する。"
            f"{img_div}は、本物と同じ自然なイメージにする。イラストではない。"
            f"{img_div}は、正面を見ながら、素敵な笑顔にしている。"
            f"{img_div}の今日のファッションは、{today_outfit}。"
        )

    contents = (
        "※以下内容を参考し、イメージを生成してください。"
        f"{const.LINE_IMG_SIZE_W}px * {const.LINE_IMG_SIZE_H}pxのサイズに合わせる"
        f"{contents_outfit}"
        "英語「Today's News」のシンプルなロゴを、生成イメージの左上に、改行せず1行に表示する。"
        "生成イメージには、ロゴの「Today's News」以外の文字は、何も表示しない。"
        f"生成イメージの背景は、天気情報の「{forecast}」が把握できるようにする。"
        "生成イメージの背景は、黒系の暗い色は避けて、シンプルなイメージにする。"
        "上記の内容以外には、何もイメージに反映しない。"
    )

    # 英語に翻訳
    contents = func.get_translated_text(contents)

    msg_data = {
        "msg": msg,
        "font_type": "yusei",
        "font_size": 30,
        "xy_size": (const.LINE_X_AXIS, const.LINE_Y_AXIS),
    }
    file_path = get_generate_text_image(div, contents, msg_data=msg_data)
    return file_path


# おすすめコーデ・夕食取得
def get_recommend_outfit_dinner(today_weather: str) -> list[str]:
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
    recommend_outfit_dinner = get_gemini_response("outfit_dinner", contents)
    return recommend_outfit_dinner


# おすすめメニュー取得
def get_recommend_menu(outfit_text: str, menu_text: str) -> tuple[str, str]:
    contents = (
        f"{outfit_text}{NEW_LINE}{menu_text}{NEW_LINE}"
        "上記の内容を元に、気温と季節を考慮し、今日のコーデ・夕食をおすすめしてください。"
        "コーデは、2アイテム。1番目が上半身、2番目が下半身に着るもの。"
        "夕食は、1番目が主食、2番目がおかずまたはスープ。"
        "各アイテムは、&で繋げる。"
        "各アイテムの最大の文字数は、8。"
        "各アイテムは、ちゃんとした単語として成立する。"
        "解説と他の文言、記号は不要。"
        f"※出力例{NEW_LINE}"
        "白いTシャツ&デニムジーンズ,チーズキムパ&味噌汁"
    )

    response = get_gemini_response("recommend_menu", contents)
    outfit = response[0]
    dinner = response[1]
    return outfit, dinner


# ニュース要約取得
def get_news_summary(
    news_list: list[str],
    keyword: str = const.SYM_BLANK,
    max_count: int = const.MIN_DISPLAY_CNT,
) -> list[str]:
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

    news_summary = get_gemini_response("news_summary", contents)
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
def get_add_condition_list(keyword: str) -> list[str]:
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
def get_other_reference() -> list[str]:
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


# サンプルコンテンツ取得
def get_sample_contents(div: str = const.STR_GEMINI) -> str:
    if div == const.STR_TEST:
        contents = "これからの未来について、100文字以内で説明お願いします。"
        # contents = (
        #     "Hi, can you create a 3d rendered image of a pig "
        #     "with wings and a top hat flying over a happy "
        #     "futuristic city with lots of greenery?"
        # )

    elif div == const.STR_GEMINI:
        contents = (
            "心が癒されるイメージを生成お願いします。"
            "以下の中でどちらと関連があるようにお願いします。"
            "[豊かな自然 or 可愛い赤ちゃん or 可愛い動物]"
            "文字列は、一切表示しないでください。"
        )

    else:
        contents = (
            f"{div}のことが分かるようにイメージを生成お願いします。"
            "シンプルで、自然なイメージでお願いします。"
        )

    return contents


# 生成イメージ取得  # [ERROR] 無料版で利用可能なモデルない
def get_generate_image(model: str, prompt: str, config=const.NONE_CONSTANT):
    client = get_client()

    # イメージ生成リクエストの送信
    try:
        response = client.models.generate_images(model=model, prompt=prompt)

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
        curr_func_nm = sys._getframe().f_code.co_name
        func.print_error_msg(SCRIPT_NAME, curr_func_nm, e)


# 生成ビデオ取得  # [ERROR] 無料版で利用可能なモデルない
def get_generate_video(div: str, model: str, prompt: str) -> str:
    client = get_client()

    operation = client.models.generate_videos(
        model,
        prompt,
    )

    # Poll the operation status until the video is ready.
    while not operation.done:
        print("Waiting for video generation to complete...")
        time.sleep(10)
        operation = client.operations.get(operation)

    # Download the generated video.
    generated_video = operation.response.generated_videos[0]
    client.files.download(file=generated_video.video)
    file_name = f"{div}.mp4"
    generated_video.video.save(file_name)
    print("Generated video saved to dialogue_example.mp4")


# [テスト] 生成コンテンツ取得
def test_gemini():
    div = const.STR_TEST
    contents = get_sample_contents(div)
    response = get_gemini_response(div, contents)
    result = const.SYM_NEW_LINE.join(response)
    func.print_test_data(div, result)


# [テスト] 生成イメージ取得
def test_gemini_img(div: str):
    contents = get_sample_contents(div)
    get_gemini_image(div, contents)


# [テスト] 今日のニュースイメージ取得
def test_today_img():
    msg = "[test] test"
    today_weather = "晴れのち曇り"
    today_outfit = "白いブラウス&黄色いスカート"
    get_today_news_image(msg, today_weather, today_outfit)


#  [テスト] 生成イメージ取得 # [ERROR] 無料版で利用可能なモデルない
def test_generate_image():
    model = "imagen-3.0-generate-002"
    prompt = "A serene landscape with mountains and a clear blue lake"
    get_generate_image(model, prompt)


# [テスト] 生成ビデオ取得 # [ERROR] 無料版で利用可能なモデルない
def test_generate_video():
    div = "example"
    model = "veo-3.0-generate-preview"
    prompt = """A close up of two people staring at a cryptic drawing on a wall, torchlight flickering.
    A man murmurs, 'This must be it. That's the secret code.' The woman looks at him and whispering excitedly, 'What did you find?'"""

    get_generate_video(div, model, prompt)


if __name__ == const.MAIN_FUNCTION:
    # test_gemini()
    test_gemini_img(const.APP_MLB)
    # test_today_img()
    # test_generate_image()
    # test_generate_video()
