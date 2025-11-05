"""
ナンバープレートゲーム
"""

import itertools
import math
import builtins

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.mongo_constants as mongo_const
import apps.utils.rank_dao as dao

# CSVファイル
number_file_path = func.get_file_path(const.APP_NUMBER, const.FILE_TYPE_CSV)

# カラムリスト
col_list = [
    const.STR_NUMBER,
    const.STR_ANSWER,
    const.STR_LEVEL,
    mongo_const.ITEM_USER_NAME,
    mongo_const.ITEM_RANK_TIME,
]

# ランク情報（デフォルト値）
DEFAULT_RANK = {
    const.STR_EASY: {
        mongo_const.FI_USER_NAME: "beginner",
        mongo_const.FI_RANK_TIME: const.RANK_TIME_NUMBER,
    },
    const.STR_MEDIUM: {
        mongo_const.FI_USER_NAME: "player",
        mongo_const.FI_RANK_TIME: const.RANK_TIME_NUMBER,
    },
    const.STR_HARD: {
        mongo_const.FI_USER_NAME: "master",
        mongo_const.FI_RANK_TIME: const.RANK_TIME_NUMBER,
    },
}


def get_item_list():
    """
    アイテムリスト取得
    """
    item_list = get_game_data_list()
    return item_list


def get_game_data_list():
    """
    ゲームデータ取得
    """
    game_data_list = []
    answer_list = get_answer_list()
    number_list = [row[0] for row in answer_list]
    rank_info_list = dao.get_rank_info_list(number_list)

    for number_data in answer_list:
        ranking_info = {}

        num = number_data[0]
        ans = number_data[1]
        level = number_data[2]

        if rank_info_list:
            for rank_info in rank_info_list:
                number = rank_info[mongo_const.FI_NUMBER]
                if num == number:
                    ranking_info = rank_info

        if not ranking_info:
            ranking_info = DEFAULT_RANK[level]

        rank_user = ranking_info[mongo_const.FI_USER_NAME]
        rank_time = ranking_info[mongo_const.FI_RANK_TIME]
        rank_time = float(rank_time)

        game_data = [num, ans, level, rank_user, rank_time]
        game_data_list.append(game_data)

    return game_data_list


def get_answer_list():
    """
    CSVデータ取得（ランダム）
    """
    df = func.get_df_from_csv(const.APP_NUMBER)[0]
    df_result = df.sample(n=const.MAX_NUMBER_DATA)

    # データの内容をリストのリスト（行のリスト）として取得
    answer_list = df_result.values.tolist()
    return answer_list


def output_df_to_csv():
    """
    DataFrameよりCSVデータ取得（ランダム）
    """
    csv_item_list = get_csv_item_list()
    csv_col_list = [const.STR_NUMBER, const.STR_ANSWER, const.STR_LEVEL]
    df = func.get_df(csv_item_list, csv_col_list)

    # CSVファイルに書き出し
    df.to_csv(
        number_file_path,
        sep=const.SYM_COMMA,
        encoding=const.CHARSET_UTF_8,
        index=const.FLG_OFF,
        header=const.FLG_ON,
    )


def get_csv_item_list():
    """
    アイテムリスト取得（CSV出力用）
    """
    item_list = []

    for num in range(1000, 10000):
        str_num = str(num)
        answer_list = find_answer(str_num)
        if not answer_list or 8 <= len(answer_list):
            continue

        if 4 <= len(answer_list):
            check_list = ["√", "⁰", "¹", "²"]
            target_list = []
            for ans in answer_list:
                if not func.check_in_list(ans, check_list):
                    target_list.append(ans)

            if 4 <= len(target_list):
                continue

        answer = const.SYM_SEMI_COLON.join(answer_list)

        level = get_game_level(answer_list)
        if level == const.SYM_DASH:
            continue

        item = [str_num, answer, level]
        item_list.append(item)

    return item_list


def find_answer(number):
    """
    正解取得（CSV出力用）
    """

    """
    4桁の数字（順番固定）から、四則演算・累乗・平方根・括弧を使った等式を全探索し、解となる式を返す。
    桁間の「結合（空文字）」を演算子候補に追加し、隣接桁を連結して多桁数（例: 4 と 9 -> 49）を作れるようにした。
    ただし連結は両側が純粋な桁（digit）の場合にのみ許可する（sqrt 適用などは連結不可）。
    sqrt の許可範囲を 4..81（sqrt 値 2..9）に制限した（以前は 4..961）。
    """

    digits = list(number)
    # 演算子候補に空文字（結合）を追加
    operators = ["+", "-", "*", "/", "**", ""]  # '' は桁結合（concat）
    answer = set()

    digits_a = const.SYM_BLANK.join(digits[0:2])
    digits_b = f"{digits[1]}{digits[0]}"
    digits_c = const.SYM_BLANK.join(digits[2:])
    if digits_a == digits_c or digits_b == digits_c:
        # 簡単過ぎるため、除外する
        return answer

    n = len(digits)
    # sqrt 適用パターン（各桁ごとに sqrt を使うか）
    for sqrt_mask in range(1 << n):
        disp_digits = []
        eval_digits = []
        invalid_mask = False
        for i, d in enumerate(digits):
            if (sqrt_mask >> i) & 1:
                try:
                    v = int(d)
                except Exception:
                    invalid_mask = True
                    break
                # 修正: sqrt は 4 <= v <= 81（sqrt が 2..9 の整数）のみ許可
                if not (4 <= v <= 81):
                    invalid_mask = True
                    break
                r = math.isqrt(v)
                if r * r != v or not (2 <= r <= 9):
                    invalid_mask = True
                    break
                disp_digits.append(f"√{d}")
                eval_digits.append(f"math.sqrt({d})")
            else:
                disp_digits.append(d)
                eval_digits.append(d)
        if invalid_mask:
            continue

        # 演算子数 1..3（各スロットに演算子または結合を入れる）
        for ops in itertools.product(operators, repeat=3):
            # '**' の右オペランド制約（単一桁 0/1/2 のみ）
            bad = False
            for i, op in enumerate(ops):
                if op == "**":
                    right_eval = eval_digits[i + 1]
                    if (
                        right_eval.startswith("math.sqrt")
                        or not right_eval.isdigit()
                        or right_eval not in ("0", "1", "2")
                    ):
                        bad = True
                        break
                # 追加: 空文字（結合）は両側が純粋数字であることを要求
                if op == "":
                    left_eval = eval_digits[i]
                    right_eval = eval_digits[i + 1]
                    # 片側でも math.sqrt や非数字が来たら結合不可
                    if not (left_eval.isdigit() and right_eval.isdigit()):
                        bad = True
                        break
            if bad:
                continue

            # 表示/評価用トークン列を作成（空文字は要素間の文字連結として扱われる）
            disp_tokens = []
            eval_tokens = []
            for i in range(3):
                disp_tokens.append(disp_digits[i])
                eval_tokens.append(eval_digits[i])
                disp_tokens.append(ops[i])
                eval_tokens.append(ops[i])
            disp_tokens.append(disp_digits[3])
            eval_tokens.append(eval_digits[3])

            # make_display: '**' は上付き表示に変換する既存ロジックを流用
            def make_display(tokens):
                out = []
                i2 = 0
                while i2 < len(tokens):
                    t = tokens[i2]
                    if t == "**" and i2 + 1 < len(tokens):
                        nxt = tokens[i2 + 1]
                        if nxt in ("0", "1", "2") and out:
                            sup = {"0": "⁰", "1": "¹", "2": "²"}[nxt]
                            out[-1] = out[-1] + sup
                            i2 += 2
                            continue
                        else:
                            out.append("**")
                            i2 += 1
                            continue
                    else:
                        out.append(t)
                        i2 += 1
                # tokens に空文字 '' が含まれている場合、join でそのまま文字連結される（期待挙動）
                return "".join(out)

            # k = 左辺の数トークン数（1～3） — ここでは元の桁単位で分割を試行
            for k in range(1, 4):
                # 左辺組立（eval用）
                left_parts = [eval_digits[0]]
                for i_num in range(0, k - 1):
                    left_parts.append(ops[i_num])
                    left_parts.append(eval_digits[i_num + 1])
                # 右辺組立（eval用）
                right_parts = [eval_digits[k]]
                for i_num in range(k, 3):
                    right_parts.append(ops[i_num])
                    right_parts.append(eval_digits[i_num + 1])

                left_eval = "".join(left_parts)
                right_eval = "".join(right_parts)

                # 明示的に "/0" を含む式は除外
                if "/0" in left_eval or "/0" in right_eval:
                    continue

                try:
                    lv = eval(left_eval, {"math": math})
                    rv = eval(right_eval, {"math": math})
                except Exception:
                    continue

                # 数値比較（浮動小数点誤差を許容）
                try:
                    if abs(builtins.float(lv) - builtins.float(rv)) < 1e-9:
                        # 表示用に組み立て（disp_digits と ops を同様に結合）
                        left_disp_parts = [disp_digits[0]]
                        for i_num in range(0, k - 1):
                            left_disp_parts.append(ops[i_num])
                            left_disp_parts.append(disp_digits[i_num + 1])
                        right_disp_parts = [disp_digits[k]]
                        for i_num in range(k, 3):
                            right_disp_parts.append(ops[i_num])
                            right_disp_parts.append(disp_digits[i_num + 1])

                        left_disp = make_display(left_disp_parts)
                        right_disp = make_display(right_disp_parts)
                        expr = f"{left_disp}={right_disp}"

                        expr_digits = list(expr)
                        ng_pattern = r"[⁰¹²][⁰¹²0-9]|0[⁰¹²]|[0-9][0-9][⁰¹²]"
                        if len(expr_digits) == 5 or func.re_search(ng_pattern, expr):
                            continue

                        # 簡易フィルタ（不正な連結記号等）
                        bad_patterns = ["+=", "-=", "*=", "/=", "=-", "=*", "=/"]
                        if not any(p in expr for p in bad_patterns):
                            answer.add(expr)
                except Exception:
                    continue

    return list(answer)


def get_game_level(answer_list):
    """
    ゲームレベル取得（CSV出力用）
    """
    length = len(answer_list)
    if length == 0:
        return const.SYM_DASH

    level_cnt = 0
    check_list = ["√", "⁰", "¹", "²"]
    for answer in answer_list:
        if not func.check_in_list(answer, check_list):
            level_cnt += 1

    if 2 <= level_cnt:
        game_level = const.STR_EASY
    else:
        game_level = const.STR_MEDIUM
        if length == 1 or (length == 2 and level_cnt == 0):
            game_level = const.STR_HARD

    return game_level


def test_number(number):
    """
    テスト
    """
    answer = find_answer(number)
    level = get_game_level(answer)
    data = f"{const.STR_ANSWER}:{answer},{const.STR_LEVEL}:{level}"
    func.print_test_data(data)


if __name__ == const.MAIN_FUNCTION:
    number = 8889
    number = 9924
    # output_df_to_csv()
    # test_number(number)

    level = const.STR_HARD
    get_item_list(level)
