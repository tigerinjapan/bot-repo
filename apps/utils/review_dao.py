import apps.utils.constants as const
import apps.utils.function_mongo as func_mongo
import apps.utils.review_dto as dto

# コレクション
COLL = const.COLL_REVIEW


# レビュー情報取得
def get_review_info(project: str):
    client = func_mongo.db_connect()
    review_info = find_review_info(client, project)
    if not review_info:
        review_info = const.NONE_CONSTANT
    func_mongo.db_close(client)
    return review_info


# レビュー情報検索
def find_review_info(client, project: str):
    cond = {dto.FI_PROJECT: project}
    result = func_mongo.db_find(client, COLL, cond)
    return result


# レビュー情報登録
def insert_review_info(client, insert_data):
    func_mongo.db_insert(client, COLL, insert_data)


# レビュー情報更新
def update_review_info(client, update_data, cond):
    update_data = {"$set": update_data}
    func_mongo.db_update(client, COLL, cond, update_data)


# レビュー情報更新（API）
def update_review_info_of_api(json_data):
    client = func_mongo.db_connect()
    data_list = json_data[const.STR_DATA]
    for data in data_list:
        update_data = dto.get_update_data_for_review_info(data)
        insert_review_info(client, update_data)
    func_mongo.db_close(client)


if __name__ == const.MAIN_FUNCTION:
    project = const.APP_TRIP
    review_info = get_review_info(project)
    print(review_info)
