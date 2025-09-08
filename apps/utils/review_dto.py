from dataclasses import asdict, dataclass
from datetime import datetime

from apps.utils.user_dto import convert_field
import apps.utils.constants as const

# 項目ID
ITEM_PROJECT = "project"
ITEM_DESIGN = "design"
ITEM_CATEGORY = "category"
ITEM_REVIEW_TEXT = "reviewText"
ITEM_UPDATE_DATE = "updateDate"

# フィールド
FI_PROJECT = convert_field(const.TYPE_STR, ITEM_PROJECT)
FI_DESIGN = convert_field(const.TYPE_STR, ITEM_DESIGN)
FI_CATEGORY = convert_field(const.TYPE_STR, ITEM_CATEGORY)
FI_REVIEW_TEXT = convert_field(const.TYPE_STR, ITEM_REVIEW_TEXT)
FI_UPDATE_DATE = convert_field(const.TYPE_DATE, ITEM_UPDATE_DATE)


@dataclass
class review:
    """
    レビュー情報のデータクラス
    """

    sProject: str
    sDesign: str
    sCategory: str
    sReviewText: str
    dUpdateDate: datetime = datetime.now()

    def get_data(self):
        return asdict(self)


# JSONデータ取得（レビュー情報の登録）
def get_update_data_for_review_info(data):
    project = data[0]
    design = data[1]
    category = data[2]
    reviewTxt = data[3]

    json_data = asdict(review(project, design, category, reviewTxt))
    return json_data
