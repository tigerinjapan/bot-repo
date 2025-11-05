# 説明: ユーザー設定

import apps.utils.constants as const
import apps.utils.function as func
import apps.utils.user_dao as dao
import apps.utils.mongo_constants as mongo_const

# タイトル
app_title = "User Info"


# [テスト] ユーザー情報取得
def user_test():
    user_id = "dev@jh.com"
    user_info = dao.get_user_info(user_id)
    func.print_debug_msg(const.STR_USER, user_info)

    user_seq = dao.get_user_seq()
    func.print_debug_msg(mongo_const.ITEM_SEQ, user_seq)


# CSVデータ取得
def get_csv_to_json():
    div = const.STR_ZIP_CODE
    # zip code csv
    # https://www.post.japanpost.jp/zipcode/dl/utf/zip/utf_ken_all.zip
    # CSVカラム
    # 1: 全国地方公共団体コード
    # 2: 旧郵便番号(3桁 or 5桁)
    # 3: 郵便番号(7桁)
    # 4: 都道府県名(カタカナ)
    # 5: 市区町村名(カタカナ)
    # 6: 町域名(カタカナ)
    # 7: 都道府県名(漢字)
    # 8: 市区町村名(漢字)
    # 9: 町域名(漢字)
    # 10:一町域が二以上の郵便番号で表される場合の表示(1 or 0)
    # 11:小字毎に番地が起番されている町域の表示(1 or 0)
    # 12:丁目を有する町域の場合の表示(1 or 0)
    # 13:1つの郵便番号で二以上の町域を表す場合の表示(1 or 0)
    # 14:更新の表示(1 or 0)
    # 15:変更理由(1 or 0)

    # CSVファイルよりDataFrame取得
    df_all = func.get_df_from_csv(div)[0]
    col_list = [div, "pref", "city", "area"]
    df = df_all[col_list]

    # ソートし、重複削除
    df_sort = df.sort_values(by=col_list)

    # DataFrameをリスト形式の辞書に変換
    data = df_sort.to_dict(orient="records")

    # zipCodeをキーとした辞書を作成
    dict_data = {item[div]: item for item in data}

    # JSONファイルに書き出し
    file_path = func.get_file_path(div, const.FILE_TYPE_JSON)
    func.write_file(file_path, dict_data)


if __name__ == const.MAIN_FUNCTION:
    # user_test()
    get_csv_to_json()
