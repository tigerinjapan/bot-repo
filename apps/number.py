import csv
import itertools

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.rank_dao as dao
import apps.utils.rank_dto as dto

# タイトル
app_title = "ナンバープレートゲーム"

# CSVファイル
number_file_path = func.get_file_path(const.STR_NUMBER, const.FILE_TYPE_CSV)

# ランク情報（デフォルト値）
DEFAULT_RANK_USER = "user"
DEFAULT_RANK_TIME = 15.00


# 乱数取得
def get_random_number(level: str = const.STR_MEDIUM) -> str:
    number_list = []
    with open(number_file_path, encoding=const.CHARSET_UTF_8) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row[const.STR_LEVEL] == level:
                number_list.append(int(row[const.STR_NUMBER]))

    random_number = str(func.get_random_choice(number_list))
    return random_number


# CSVから正解取得
def get_answer_by_number(number):
    with open(number_file_path, encoding=const.CHARSET_UTF_8) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row[const.STR_NUMBER] == str(number):
                answer = row[const.STR_ANSWER]
                return answer


# ランキング情報取得
def get_ranking_info(number: int):
    rank_user = DEFAULT_RANK_USER
    rank_time = DEFAULT_RANK_TIME

    ranking_info = dao.get_rank_info(number)
    if ranking_info:
        rank_user = ranking_info[dto.FI_USER_NAME]
        rank_time = ranking_info[dto.FI_RANK_TIME]
        rank_time = float(rank_time)

    return rank_user, rank_time


# CSV出力
def output_df_to_csv():
    item_list = get_item_list()
    col_list = [const.STR_NUMBER, const.STR_ANSWER, const.STR_LEVEL]
    df = func.get_df(item_list, col_list)

    # CSVファイルに書き出し
    df.to_csv(
        number_file_path,
        sep=const.SYM_COMMA,
        encoding=const.CHARSET_UTF_8,
        index=const.FLG_OFF,
        header=const.FLG_ON,
    )


# アイテムリスト取得（CSV出力用）
def get_item_list():
    item_list = []

    for num in range(1000, 10000):
        str_num = str(num)
        answer_list = find_answer(str_num)
        answer = const.SYM_SEMI_COLON.join(answer_list)

        level = get_game_level(answer_list)
        if level == const.SYM_DASH:
            continue

        item = [str_num, answer, level]
        item_list.append(item)

    return item_list


# 正解取得（CSV出力用）
def find_answer(number):
    """
    4桁の数字（順番固定）から、四則演算とイコールを使った等式を全探索で生成し、解となる式を返す。
    ・イコールは必ず1回使用
    ・四則演算は最小1回～最大3回使用
    ・0とは掛け算・割り算しない
    """
    digits = list(number)
    operators = ["+", "-", "*", "/"]
    answer = set()

    p = digits
    # 1回, 2回, 3回の演算子利用パターンをすべて試す
    for op_count in range(1, 4):
        # 演算子の位置を選ぶ（3つの間からop_count個選ぶ）
        for op_pos in itertools.combinations([0, 1, 2], op_count):
            # 使う演算子の全パターン
            for ops in itertools.product(operators, repeat=op_count):
                expr_list = [p[0]]
                op_idx = 0
                for i in range(3):
                    if i in op_pos:
                        expr_list.append(ops[op_idx])
                        op_idx += 1
                    expr_list.append(p[i + 1])
                expr = const.SYM_BLANK.join(expr_list)

                # イコールの位置を2文字目以降～最後の1文字前まで動かす
                for eq_pos in range(2, len(expr)):
                    left = expr[:eq_pos]
                    right = expr[eq_pos:]

                    # 0での割り算を除外
                    if "/0" in left or "/0" in right:
                        continue

                    try:
                        if eval(left) == eval(right):
                            add_flg = const.FLG_ON
                            answer_expr = f"{left}={right}"
                            repl_list = ["+=", "-=", "*=", "/=", "=-", "=*", "=/"]

                            for repl_str in repl_list:
                                if repl_str in answer_expr:
                                    add_flg = const.FLG_OFF
                                    break

                            if add_flg:
                                answer_expr = answer_expr.replace("=+", "=")
                                answer.add(answer_expr)

                    except Exception:
                        continue

    answer_list = list(answer)
    return answer_list


# ゲームレベル取得（CSV出力用）
def get_game_level(answer_list):
    game_level = const.SYM_DASH
    length = len(answer_list)
    if length == 1:
        game_level = const.STR_HARD
    elif length == 2:
        game_level = const.STR_MEDIUM
    elif length >= 3:
        game_level = const.STR_EASY

    return game_level


# テスト
def test_number():
    num = "4444"
    answer = find_answer(num)
    level = get_game_level(answer)
    data = f"{const.STR_ANSWER}:{answer},{const.STR_LEVEL}:{level}"
    func.print_test_data(data)


if __name__ == const.MAIN_FUNCTION:
    # output_df_to_csv()
    # test_number()
    # get_random_number()
    rank_user, rank_time = get_ranking_info(4567)
    print(rank_user, rank_time)
