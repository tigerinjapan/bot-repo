# 説明: 定数一覧

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
DATE_FORMAT_YYYYMMDD_SLASH = "%Y/%m/%d(%a)"
DATE_FORMAT_YYYYMMDD_HHMM = "%Y/%m/%d(%a) %H:%M"
DATE_FORMAT_YYYYMMDD_KO = "%Y년%#m월%#d일"
DATE_FORMAT_MMDD_SLASH_NO_ZERO = "%#m/%#d"
DATE_FORMAT_ISO = "iso"

##### リクエストタイプ #####
REQUEST_TYPE_GET = "get"
REQUEST_TYPE_POST = "post"

##### 正規表現 #####
PATTERN_YYYYMMDD = "^[0-9]{4}(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])$"
PATTERN_NUMBER = "^[0-9]$"
PATTERN_NUMBERS = r"(\d+)"

##### API #####
HEADERS_JSON = {"Content-Type": "application/json"}

##### ステータスコード #####
STATUS_CODE_OK = 200
STATUS_CODE_CREATED = 201
STATUS_CODE_NO_CONTENT = 204

STATUS_CODE_BAD_REQUEST = 400
STATUS_CODE_UNAUTHORIZED = 401
STATUS_CODE_FORBIDDEN = 403
STATUS_CODE_NOT_FOUND = 404
STATUS_CODE_METHOD_NOT_ALLOWED = 405

STATUS_CODE_INTERNAL_SERVER_ERROR = 500
STATUS_CODE_BAD_GATEWAY = 502
STATUS_CODE_SERVICE_UNAVAILABLE = 503
STATUS_CODE_GATEWAY_TIMEOUT = 504

STATUS_CODE_NORMAL = [200, 201, 204]

##### 数値 #####
NUM_ZERO = 0
NUM_ONE = 1
NUM_TWO = 2
NUM_THREE = 3
NUM_FOUR = 4

##### 日付 #####
DATE_NOW = 0
DATE_YEAR = 1
DATE_MONTH = 2
DATE_DAY = 3
DATE_HOUR = 4
DATE_MIN = 5
DATE_TODAY = 6
DATE_WEEKDAY = 7

# 座標
LINE_FONT_SIZE = 30
LINE_X_AXIS = 50
LINE_Y_AXIS = 130
LINE_IMG_SIZE_W = 480
LINE_IMG_SIZE_H = 360
LINE_IMG_X_AXIS = 260
LINE_IMG_Y_AXIS = 90

KAKAO_FONT_SIZE = 32
KAKAO_X_AXIS = 50
KAKAO_Y_AXIS = 140
KAKAO_IMG_SIZE_W = 480
KAKAO_IMG_SIZE_H = 480

# 件数
MIN_DISPLAY_CNT = 3
MAX_DISPLAY_CNT = 5
MAX_RETRY_CNT = 3
MAX_TEMP_MSG = 20
MAX_TEXT_LENGTH = 200
MAX_PHRASE_CSV = 999

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

##### フォントタイプ #####
FONT_TYPE_MEIRYO = "meiryo"
FONT_TYPE_MSGOTHIC = "msgothic"
FONT_TYPE_UZURA = "uzura"
FONT_TYPE_YUSEI = "yusei"
FONT_TYPE_NANUM = "nanum"

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
SYM_PERIOD = "。"
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
STR_INFO = "info"
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
STR_APP = "app"
STR_URL = "url"
STR_IP = "IP"
STR_HOST = "host"
STR_SERVER = "server"
STR_INDEX = "index"
STR_RESULT = "result"
STR_CONTENTS = "contents"
STR_ITEM = "item"
STR_API = "api"
STR_DATA = "data"
STR_UPDATE = "update"
STR_DIV = "div"
STR_TIME = "time"
STR_DATE = "date"
STR_DAY = "day"
STR_HOLIDAY = "holiday"
STR_KEY = "key"
STR_TITLE = "title"
STR_DECODE = "decode"
STR_LINE = "line"
STR_GEMINI = "gemini"
STR_IMG = "img"
STR_FONT = "font"
STR_ADDR = "addr"
STR_ACCESS = "access"
STR_DESCRIPTION = "description"
STR_KEYWORD = "keyword"
STR_NOTIFY = "notify"
STR_FIRST = "first"
STR_TEST = "test"
STR_PHRASE = "phrase"
STR_NUMBER = "number"
STR_ANSWER = "answer"
STR_LEVEL = "level"
STR_REST = "rest"
STR_ENGLISH = "english"
STR_UNLINK = "unlink"

STR_DB = "db"
STR_MONGO = "mongo"
STR_UPPER = "upper"
STR_LOWER = "lower"
STR_CAPITALIZE = "capitalize"

STR_EASY = "easy"
STR_MEDIUM = "medium"
STR_HARD = "hard"

STR_KAKAO = "kakao"
STR_KPOP = "kpop"
STR_NISA = "nisa"

STR_AI = "AI"
STR_USER_INFO = "userInfo"
STR_ZIP_CODE = "zipCode"
STR_ENV_VAR = "env_var"
STR_NUMBER_PLATE = "numberPlate"
STR_PHRASE_KO = "phrase_ko"

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
STR_MAN_JA = "男性"
STR_WOMAN_JA = "女性"

STR_JPY = "JPY"
STR_KRW = "KRW"
STR_USD = "USD"
STR_TWD = "TWD"
STR_VND = "VND"
STR_THB = "THB"
STR_PHP = "PHP"

STR_JPY_JA = "円"
STR_KRW_JA = "ウォン"
STR_USD_JA = "ドル"
STR_TWD_JA = "ユェン"
STR_VND_JA = "ドン"
STR_THB_JA = "バーツ"
STR_PHP_JA = "ペソ"

STR_JPY_KO = "엔"
STR_KRW_KO = "원"

##### マスキング #####
MASKING_COMPANY = "zzzzzz"
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

##### ログ出力対象外文字 #####
LIST_LOG_MASKING = ["kobe-", "token", "kapi.", "kauth"]
LOG_MASKING = "XXXXX"

##### 曜日リスト #####
LIST_WEEKDAY = ["月", "火", "水", "木", "金", "土", "日"]

##### ファンド #####
FUND_NO_SP_500 = "182809"
FUND_NO_AI = "179702"
FUND_NO_US_TECH = "173905"
FUND_NAME_SP_500 = "S&P500"
FUND_NAME_AI = "イノベAI"
FUND_NAME_US_TECH = "USテクノロ"

LIST_FUND_NO = [FUND_NO_SP_500, FUND_NO_AI, FUND_NO_US_TECH]
LIST_FUND_NAME = [FUND_NAME_SP_500, FUND_NAME_AI, FUND_NAME_US_TECH]

##### URL #####
# サイトURL
URL_GOOGLE = "https://www.google.com"
URL_TENKI = "https://tenki.jp"
URL_CANCAM = "https://cancam.jp"
URL_SMBC_FUND = "https://www.smd-am.co.jp/fund"
URL_NAVER = "https://www.naver.com"
URL_NAVER_MO = "https://m.naver.com"
URL_NAVER_FINANCE = "https://finance.naver.com"
URL_NAVER_SEARCH = "https://search.naver.com"
URL_NAVER_NEWS = "https://news.naver.com"
URL_KONEST = "https://www.konest.com"
URL_WOWKOREA = "https://www.wowkorea.jp"
URL_NIKKEI = "https://www.nikkei.com"
URL_ITMEDIA = "https://www.itmedia.co.jp"
URL_ACHIKOCHI = "https://achikochi-data.com"
URL_LCC = "https://dsk.ne.jp"
URL_TV = "https://bangumi.org"
URL_MLB = "https://www.mlb.com"
URL_MLB_STAT_API = "https://statsapi.mlb.com"

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
APP_TRAVEL = "travel"

APP_USER = "user"
APP_MLB = "mlb"

APP_NUMBER = "number"
APP_REVIEW = "review"
APP_BOARD = "board"

APP_TRAVEL_DESIGN = "travel_design"
APP_URL_DESIGN = "url_design"
APP_KAKAO_DESIGN = "kakao_design"

APP_TODAY_KOREA = "today_korea"
APP_TRAVEL_KO = "travel_ko"

LIST_APP_NAME = [
    APP_TODAY,
    APP_NEWS,
    APP_DRAMA,
    APP_RANKING,
    APP_LCC,
    APP_TV,
    APP_STUDY,
]
LIST_APP_SITE = [APP_SITE, APP_CAFE, APP_TRAVEL, APP_BOARD]
LIST_APP_KOREA = [APP_TODAY_KOREA]
LIST_ALL_APP_NAME = LIST_APP_NAME + LIST_APP_SITE + LIST_APP_KOREA

LIST_APPS_NAME = [
    APP_TRAVEL,
    APP_TRAVEL_KO,
    APP_REVIEW,
    APP_TRAVEL_DESIGN,
    APP_URL_DESIGN,
    APP_KAKAO_DESIGN,
]
LIST_APPS_NAME_2 = [STR_GEMINI]


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
PATH_APP = get_path(STR_APP)
PATH_APP_NEWS = f"{PATH_APP}{get_path(APP_NEWS)}"
PATH_APP_BOARD = f"{PATH_APP}{get_path(APP_BOARD)}"
PATH_UPDATE = get_path(STR_UPDATE)

##### HTMLファイル名 #####
HTML_INDEX = get_html(STR_INDEX)
HTML_RESULT = get_html(STR_RESULT)
HTML_USER_INFO = get_html(STR_USER_INFO)
HTML_GEMINI = get_html(STR_GEMINI)
HTML_NUMBER_PLATE = get_html(STR_NUMBER_PLATE)
HTML_RESULT_2 = get_html(f"{STR_RESULT}2")

if __name__ == MAIN_FUNCTION:
    data = f"[{DATE_WEEKDAY, HTML_INDEX}]"
    type_name = type(data).__name__
    print(STR_TYPE_JA, type_name)
    print(data)
