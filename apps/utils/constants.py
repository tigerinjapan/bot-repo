# 説明: 定数一覧

import os
from datetime import datetime

from selenium.webdriver.common.by import By

##### システム名 #####
SYSTEM_NAME = "開発デモシステム"

##### main関数 #####
MAIN_FUNCTION = "__main__"

##### debug定数 #####
DEBUG_CONSTANT = "__debug__"

##### NoneType #####
NONE_CONSTANT = None

##### フラグ #####
FLG_ON = True
FLG_OFF = False

##### 接続情報 #####
IP_DEFAULT = "0.0.0.0"
PORT_DEFAULT = 8000
IP_PRIVATE = "192.168"
IP_LOCAL = "127.0.0.1"
HOST_LOCAL = "kobe-pc"
PORT_NUM = 5000

##### セッション #####
SESSION_KEY = "admindevguest"
SESSION_TIMEOUT_SEC = 600

##### ユーザ権限 #####
AUTH_ADMIN = "admin"
AUTH_DEV = "dev"
AUTH_GUEST = "guest"

NUM_AUTH_ADMIN = 3
NUM_AUTH_DEV = 2
NUM_AUTH_GUEST = 1

##### ユーザーエージェント #####
UA_PC = {"User-Agent": "Chrome/74.0.3729.169"}
UA_OPT_PC = "--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
UA_OPT_MO = "--user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36"
UA_DIV_MO = "Mobile"
UA_DIV_PC = "PC"

##### パス #####
DIR_CURR_WORK = os.getcwd()

##### 文字コード #####
CHARSET_UTF_8 = "utf-8"
CHARSET_ASCII = "ascii"
CHARSET_SJIS = "sjis"

##### 言語コード #####
LANG_EN = "en"
LANG_JA = "ja"
LANG_KO = "ko"

##### 日付フォーマット #####
DATE_FORMAT_OUTPUT_FILE = "%Y%m%d%H%M%S"
DATE_FORMAT_YYYYMMDD = "%Y%m%d"
DATE_FORMAT_YYYYMMDD_DASH = "%Y-%m-%d"
DATE_FORMAT_YYYYMMDD_SLASH = "%Y/%m/%d"
DATE_FORMAT_YYYYMM = "%Y%m"
DATE_FORMAT_YYYYMMDD_HHMM = "%Y/%m/%d(%a) %H:%M"
DATE_FORMAT_ISO = "iso"

##### 日付 #####
DATETIME_NOW = datetime.now()
DATE_NOW = DATETIME_NOW.strftime(DATE_FORMAT_OUTPUT_FILE)
DATE_TODAY = DATETIME_NOW.strftime(DATE_FORMAT_YYYYMMDD)
DATE_TODAY_SLASH = DATETIME_NOW.strftime(DATE_FORMAT_YYYYMMDD_SLASH)
DATE_YEAR_MONTH = DATETIME_NOW.strftime(DATE_FORMAT_YYYYMM)
DATE_YEAR = DATETIME_NOW.year
DATE_MONTH = DATETIME_NOW.month
DATE_DAY = DATETIME_NOW.day
DATE_WEEKDAY = DATETIME_NOW.weekday()

##### リクエストタイプ #####
REQUEST_TYPE_GET = "get"
REQUEST_TYPE_POST = "post"

##### ステータスコード #####
STATUS_CODE_NORMAL = [200, 201, 204]

##### 正規表現 #####
PATTERN_YYYYMMDD = "^[0-9]{4}(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])$"
PATTERN_NUMBER = "^[0-9]$"
PATTERN_NUMBERS = r"(\d+)"

##### API #####
HEADERS_JSON = {"Content-Type": "application/json"}

##### 数値 #####
NUM_ZERO = 0
NUM_ONE = 1
NUM_TWO = 2
NUM_THREE = 3

# 画面表示件数
MAX_DISPLAY_CNT = 5
MIN_DISPLAY_CNT = 3
MAX_RETRY_CNT = 3

##### 型 #####
TYPE_DICT = "dict"
TYPE_LIST = "list"
TYPE_STR = "str"
TYPE_NUM = "num"
TYPE_DATE = "date"

##### HTMLタグ #####
TAG_FORM = "form"
TAG_DIV = "div"
TAG_DL = "dl"
TAG_DT = "dt"
TAG_DD = "dd"
TAG_P = "p"
TAG_UL = "ul"
TAG_LI = "li"
TAG_A = "a"
TAG_TABLE = "table"
TAG_THEAD = "thead"
TAG_TBODY = "tbody"
TAG_TR = "tr"
TAG_TH = "th"
TAG_TD = "td"
TAG_SPAN = "span"
TAG_META = "meta"
TAG_CAPTION = "caption"
TAG_ABBR = "abbr"
TAG_H1 = "h1"
TAG_H2 = "h2"
TAG_H3 = "h3"
TAG_H4 = "h4"
TAG_IMG = "img"

##### HTML属性 #####
ATTR_CLASS = "class"
ATTR_ID = "id"
ATTR_PROP = "property"
ATTR_HREF = "href"
ATTR_ALT = "alt"
ATTR_TITLE = "title"

##### ファイルモード #####
FILE_MODE_READ = "r"
FILE_MODE_WRITE = "w"
FILE_MODE_READ_BINARY = "rb"

##### ファイル拡張子 #####
FILE_TYPE_HTML = "html"
FILE_TYPE_CSV = "csv"
FILE_TYPE_TXT = "txt"
FILE_TYPE_ZIP = "zip"
FILE_TYPE_PY = "py"
FILE_TYPE_JSON = "json"
FILE_TYPE_LOG = "log"
FILE_TYPE_PNG = "png"
FILE_TYPE_JPEG = "jpeg"
FILE_TYPE_TTC = "ttc"

##### 入力タイプ #####
INPUT_TYPE_TEXT = "text"
INPUT_TYPE_RADIO = "radio"
INPUT_TYPE_SELECT = "select"
INPUT_TYPE_DATE = "date"
INPUT_TYPE_BUTTON = "button"

##### Selenium:By #####
BY_ID = By.ID
BY_XPATH = By.XPATH
BY_LINK = By.LINK_TEXT
BY_NM = By.NAME
BY_TAG = By.TAG_NAME
BY_CLASS = By.CLASS_NAME
BY_CSS = By.CSS_SELECTOR

##### 記号、特殊文字 #####
SYM_NEW_LINE = "\n"
SYM_TAB = "\t"
SYM_BLANK = ""
SYM_SPACE = " "
SYM_COMMA = ","
SYM_DOT = "."
SYM_COLON = ":"
SYM_SEMI_COLON = ";"
SYM_DASH = "-"
SYM_UNDER = "_"
SYM_EQUAL = "="
SYM_SLASH = "/"
SYM_AMP = "&"
SYM_ASTA = "*"
SYM_COMMA_JAP = "、"
SYM_PUNC = "。"
SYM_OPEN = "【"
SYM_CLOSE = "】"
SYM_AT = "@"

##### 文字列 #####
STR_AUTH = "auth"
STR_INPUT = "input"
STR_OUTPUT = "output"
STR_LOGIN = "login"
STR_LOGOUT = "logout"
STR_LOG = "log"
STR_ERROR = "error"
STR_USER = "user"
STR_NAME = "name"
STR_ID = "id"
STR_TYPE = "type"
STR_CLIENT = "client"
STR_TOKEN = "token"
STR_EXPIRATION = "expiration"
STR_REQUEST = "request"
STR_RESPONSE = "response"
STR_STATUS = "status"
STR_MESSAGE = "message"
STR_URL = "url"
STR_IP = "IP"
STR_HOST = "host"
STR_INDEX = "index"
STR_RESULT = "result"
STR_CONTENTS = "contents"
STR_ITEM = "item"
STR_SERVER = "server"
STR_UPDATE = "update"
STR_TIME = "time"
STR_KEY = "key"
STR_DIV = "div"
STR_TITLE = "title"
STR_DECODE = "decode"
STR_LINE = "line"
STR_GEMINI = "gemini"
STR_API = "api"
STR_ADDR = "addr"
STR_IMG = "img"
STR_FONT = "font"
STR_ENV_VAR = "env_var"
STR_KEYWORD = "keyword"
STR_NOTIFY = "notify"
STR_FIRST = "first"
STR_TEST = "test"
STR_KPOP = "kpop"
STR_AI = "AI"
STR_USER_INFO = "userInfo"
STR_ZIP_CODE = "zipCode"

STR_DB = "db"
STR_MONGO = "mongo"
STR_UPPER = "upper"
STR_LOWER = "lower"
STR_CAPITALIZE = "capitalize"

STR_LOGIN_JA = "ログイン"
STR_LOGOUT_JA = "ログアウト"
STR_PATH_JA = "パス"
STR_FILE_JA = "ファイル"
STR_MESSAGE_JA = "メッセージ"
STR_TOKEN_JA = "トークン"
STR_EXPIRE_JA = "有効期限"
STR_CHARSET_JA = "文字コード"
STR_TYPE_JA = "タイプ"
STR_SYSTEM_JA = "システム"
STR_DIV_JA = "区分"
STR_CONTENTS_JA = "内容"
STR_TITLE_JA = "タイトル"
STR_IMG_JA = "イメージ"
STR_LINK_JA = "リンク"
STR_NOTIFY_JA = "通知"
STR_COMPANY_JA = "会社"
STR_DATE_JA = "日付"
STR_NEWS_JA = "ニュース"
STR_KOREA_JA = "韓国"
STR_ENT_JA = "エンタメ"
STR_NIKKEI_JA = "日経"
STR_DRAMA_JA = "ドラマ"
STR_RANKING_JA = "ランキング"
STR_X_TREND_JA = "Xトレンド"
STR_KOREAN_JA = "韓国語"
STR_YEN_JA = "円"
STR_WON_JA = "ウォン"

##### マスキング #####
MASKING_COMPANY = "xxxxxx"
MASKING_STR_UPPER = "XXXX"
MASKING_STR_LOWER = "xxxx"
MASKING_NUM = "9999"
MASKING_YEAR = "YYYY"

LIST_MASKING = [
    MASKING_COMPANY,
    MASKING_STR_UPPER,
    MASKING_STR_LOWER,
    MASKING_NUM,
    MASKING_YEAR,
]

##### 置換文字列リスト #####
LIST_REPLACE = [
    "-",
    "=",
    "　",
    "?",
    "!",
    "？",
    "！",
    "〇",
    "□",
    "◇",
    "☆",
    "●",
    "■",
    "◆",
    "★",
    "※",
    "・",
    "━",
    "∞",
    "\u3000",
    "\u200b",
    "\t",
    "\n",
    "\r\n",
    "<br>",
    "</br>",
    "<br/>",
]

##### 曜日リスト #####
LIST_WEEKDAY = ["月", "火", "水", "木", "金", "土", "日"]

##### DB情報 #####
COLL_USER_INFO = "userInfo"

SEX_MAN = "男"
SEX_WOMAN = "女"


def convert_field(type_div, id):
    div = "ao" if type_div == TYPE_LIST else type_div[0]
    # func[capitalize]:Converts the first character of a string to an uppercase letter
    id_new = id.capitalize()[0] + id[1:]
    field = f"{div}{id_new}"
    return field


# 項目ID:user info
ITEM_USER_ID = "userId"
ITEM_USER_DIV = "userDiv"
ITEM_USER_NAME = "userName"
ITEM_USER_PW = "userPw"
ITEM_YEAR = "year"
ITEM_SEX = "sex"
ITEM_ZIP_CD = "zipCd"
ITEM_PREF = "pref"
ITEM_TOWN = "town"
ITEM_LINE = "line"
ITEM_STATION = "station"
ITEM_TEL = "tel"
ITEM_SEQ = "seq"
ITEM_MODIFIED_DATE = "modifiedDate"
ITEM_LAST_LOGIN_DATE = "lastLoginDate"

# フィールド:user info
FI_USER_ID = convert_field(TYPE_STR, ITEM_USER_ID)
FI_USER_DIV = convert_field(TYPE_STR, ITEM_USER_DIV)
FI_USER_NAME = convert_field(TYPE_STR, ITEM_USER_NAME)
FI_USER_PW = convert_field(TYPE_STR, ITEM_USER_PW)
FI_YEAR = convert_field(TYPE_NUM, ITEM_YEAR)
FI_SEX = convert_field(TYPE_NUM, ITEM_SEX)
FI_ZIP_CD = convert_field(TYPE_STR, ITEM_ZIP_CD)
FI_PREF = convert_field(TYPE_STR, ITEM_PREF)
FI_TOWN = convert_field(TYPE_STR, ITEM_TOWN)
FI_LINE = convert_field(TYPE_STR, ITEM_LINE)
FI_STATION = convert_field(TYPE_STR, ITEM_STATION)
FI_TEL = convert_field(TYPE_STR, ITEM_TEL)
FI_SEQ = convert_field(TYPE_NUM, ITEM_SEQ)
FI_MODIFIED_DATE = convert_field(TYPE_DATE, ITEM_MODIFIED_DATE)
FI_LAST_LOGIN_DATE = convert_field(TYPE_DATE, ITEM_LAST_LOGIN_DATE)

##### URL #####
# サイトURL
URL_GOOGLE = "https://www.google.com"
URL_TENKI = "https://tenki.jp"
URL_CANCAM = "https://cancam.jp"
URL_RAKUTEN_RECIPE = "https://recipe.rakuten.co.jp/menu/"
URL_SMBC_FUND = "https://www.smd-am.co.jp/fund"
URL_NAVER_FINANCE = "https://finance.naver.com"
URL_NAVER_SEARCH = "https://search.naver.com"
URL_KONEST = "https://www.konest.com"
URL_WOWKOREA = "https://www.wowkorea.jp"
URL_NIKKEI = "https://www.nikkei.com"
URL_ITMEDIA = "https://www.itmedia.co.jp"
URL_ACHIKOCHI = "https://achikochi-data.com"
URL_LCC = "https://dsk.ne.jp"
URL_TV = "https://www.tvkingdom.jp"

##### アプリケーション名 #####
APP_TODAY = "today"
APP_NEWS = "news"
APP_DRAMA = "drama"
APP_RANKING = "ranking"
APP_LCC = "lcc"
APP_TV = "tv"
APP_STUDY = "study"
APP_SITE = "site"
APP_CAFE = "cafe"
APP_USER = "user"
LIST_APP_NAME = [
    APP_TODAY,
    APP_NEWS,
    APP_DRAMA,
    APP_RANKING,
    APP_LCC,
    APP_TV,
    APP_STUDY,
]
LIST_ALL_APP_NAME = LIST_APP_NAME + [APP_SITE, APP_CAFE]


# パス取得
def get_path(app_name):
    path = f"/{app_name}"
    return path


# HTML取得
def get_html(app_name):
    html = f"{app_name}.{FILE_TYPE_HTML}"
    return html


# 画面パス
PATH_ROOT = "/"
PATH_LOGIN = get_path(STR_LOGIN)
PATH_LOGOUT = get_path(STR_LOGOUT)
PATH_TODAY = "/app" + get_path(APP_TODAY)
PATH_NEWS = "/app" + get_path(APP_NEWS)
PATH_USER = "/app" + get_path(APP_USER)
PATH_UPDATE = get_path(STR_UPDATE)

##### HTMLファイル名 #####
HTML_INDEX = get_html(STR_INDEX)
HTML_RESULT = get_html(STR_RESULT)
HTML_USER_INFO = get_html(STR_USER_INFO)

if __name__ == MAIN_FUNCTION:
    data = f"[{DATE_WEEKDAY, HTML_INDEX}]"
    type_name = type(data).__name__
    print(STR_TYPE_JA, type_name)
    print(data)
