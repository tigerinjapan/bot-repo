"""
定数一覧
"""

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
LIST_AUTH = [AUTH_ADMIN, AUTH_DEV, AUTH_GUEST]

NUM_AUTH_ADMIN = 3
NUM_AUTH_DEV = 2
NUM_AUTH_GUEST = 1
LIST_AUTH_NUM = [NUM_AUTH_ADMIN, NUM_AUTH_DEV, NUM_AUTH_GUEST]

##### ユーザーエージェント #####
UA_PC = {"User-Agent": "Chrome/74.0.3729.169"}
UA_OPT_PC = "--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
UA_OPT_MO = "--user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36"
UA_DIV_MO = "Mobile"
UA_DIV_PC = "PC"
UA_DIV_TABLET = "Tablet"
UA_OS_ANDROID = "Android"
UA_OS_IOS = "iOS"
UA_OS_WINDOWS = "Windows"
UA_OS_LINUX = "Linux"
UA_BROWSER_CHROME = "Chrome"
UA_BROWSER_EDGE = "Edge"
UA_BROWSER_SAFARI = "Safari"
UA_BROWSER_FIREFOX = "Firefox"

##### 文字コード #####
CHARSET_UTF_8 = "utf-8"
CHARSET_ASCII = "ascii"
CHARSET_SJIS = "sjis"

##### 国コード #####
COUNTRY_CD_JP = "jp"
COUNTRY_CD_KR = "kr"

##### 言語コード #####
LANG_CD_JA = "ja"
LANG_CD_KO = "ko"
LANG_CD_EN = "en"
LIST_LANG_CD = [LANG_CD_JA, LANG_CD_KO, LANG_CD_EN]

##### 日付フォーマット #####
DATE_FORMAT_OUTPUT_FILE = "%Y%m%d%H%M%S"
DATE_FORMAT_YYYYMMDD = "%Y%m%d"
DATE_FORMAT_YYYYMMDD_DASH = "%Y-%m-%d"
DATE_FORMAT_YYYYMMDD_SLASH = "%Y/%m/%d(%a)"
DATE_FORMAT_YYYYMMDD_HHMM = "%Y/%m/%d(%a) %H:%M"
DATE_FORMAT_YYYYMMDD_JA = "%Y年%#m月%#d日"
DATE_FORMAT_YYYYMMDD_KO = "%Y년%#m월%#d일"
DATE_FORMAT_YYYY = "%Y"
DATE_FORMAT_YYYYMM_SLASH = "%Y/%m"
DATE_FORMAT_MMDD_SLASH = "%m/%d"
DATE_FORMAT_MMDD_SLASH_NO_ZERO = "%#m/%#d"
DATE_FORMAT_ISO = "iso"

TIMEZONE_JST = "JST"
JST_OFFSET_HOURS = 9

##### 正規表現 #####
PATTERN_YYYYMMDD = "^[0-9]{4}(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])$"
PATTERN_NUMBER = "^[0-9]$"
PATTERN_NUMBERS = r"(\d+)"

##### リクエストタイプ #####
REQUEST_TYPE_GET = "get"
REQUEST_TYPE_POST = "post"

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

##### API #####
# API HEADERS
API_HEADERS_JSON = {"Content-Type": "application/json"}
API_HEADERS_UTF8 = {"Content-Type": "application/x-www-form-urlencoded"}

##### 数値 #####
NUM_ZERO = 0
NUM_ONE = 1
NUM_TWO = 2
NUM_THREE = 3
NUM_FOUR = 4

# 日付
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
KAKAO_Y_AXIS = 170
KAKAO_IMG_SIZE_W = 480
KAKAO_IMG_SIZE_H = 480

# 件数
MIN_DISPLAY_CNT = 3
MAX_DISPLAY_CNT = 5
MAX_RETRY_CNT = 3

MAX_TEMP_MSG = 20
MAX_WRAP_WIDTH = 32
MAX_TEXT_LENGTH = 200
MAX_PHRASE_CSV = 999

MAX_TOKEN_EXPIRATION_MINUTES = 10

MAX_RANDOM_IMG = 4
MAX_USER_MENU = 10

NUM_TARGET_DAYS = 7
MAX_TARGET_DAYS_BOARD = -14

MAX_NUMBER_DATA = 50
MAX_MSG_API_CNT = 200

# ランクタイム（DB更新用）
RANK_TIME_NUMBER = 10.00

##### 型 #####
TYPE_STR = "str"
TYPE_NUM = "num"
TYPE_DATE = "date"
TYPE_DICT = "dict"
TYPE_LIST = "list"

##### HTMLタグ #####
TAG_A = "a"
TAG_ABBR = "abbr"
TAG_CAPTION = "caption"
TAG_DD = "dd"
TAG_DL = "dl"
TAG_DT = "dt"
TAG_DIV = "div"
TAG_FORM = "form"
TAG_H1 = "h1"
TAG_H2 = "h2"
TAG_H3 = "h3"
TAG_H4 = "h4"
TAG_IMG = "img"
TAG_LI = "li"
TAG_META = "meta"
TAG_P = "p"
TAG_SPAN = "span"
TAG_TABLE = "table"
TAG_TBODY = "tbody"
TAG_TD = "td"
TAG_TH = "th"
TAG_THEAD = "thead"
TAG_TR = "tr"
TAG_UL = "ul"

##### HTML属性 #####
ATTR_ALT = "alt"
ATTR_CLASS = "class"
ATTR_HREF = "href"
ATTR_ID = "id"
ATTR_PROP = "property"
ATTR_TITLE = "title"

##### ファイルモード #####
FILE_MODE_READ = "r"
FILE_MODE_WRITE = "w"
FILE_MODE_READ_BINARY = "rb"

##### ファイル拡張子 #####
FILE_TYPE_CSV = "csv"
FILE_TYPE_HTML = "html"
FILE_TYPE_JPEG = "jpeg"
FILE_TYPE_JSON = "json"
FILE_TYPE_LOG = "log"
FILE_TYPE_PNG = "png"
FILE_TYPE_PY = "py"
FILE_TYPE_TTC = "ttc"
FILE_TYPE_TXT = "txt"
FILE_TYPE_ZIP = "zip"

##### フォントタイプ #####
FONT_TYPE_MEIRYO = "meiryo"
FONT_TYPE_MSGOTHIC = "msgothic"
FONT_TYPE_UZURA = "uzura"
FONT_TYPE_YUSEI = "yusei"
FONT_TYPE_NANUM = "nanum"

##### 記号、特殊文字 #####
SYM_AMP = "&"
SYM_ASTA = "*"
SYM_AT = "@"
SYM_BLANK = ""
SYM_COLON = ":"
SYM_COMMA = ","
SYM_COMMA_JAP = "、"
SYM_DASH = "-"
SYM_DOT = "."
SYM_EQUAL = "="
SYM_NEW_LINE = "\n"
SYM_PERIOD = "。"
SYM_SEMI_COLON = ";"
SYM_SLASH = "/"
SYM_SPACE = " "
SYM_TAB = "\t"
SYM_UNDER = "_"

SYM_CLOSE = "】"
SYM_OPEN = "【"

##### 文字列 #####
STR_ACCESS = "access"
STR_ADD = "add"
STR_ADDR = "addr"
STR_ANSWER = "answer"
STR_API = "api"
STR_APP = "app"
STR_AUTH = "auth"
STR_BACKUP = "backup"
STR_BEGINNER = "beginner"
STR_BROWSER = "browser"
STR_CAPITALIZE = "capitalize"
STR_CATEGORY = "category"
STR_CLIENT = "client"
STR_CONTENTS = "contents"
STR_COUNTRY = "country"
STR_DATA = "data"
STR_DATE = "date"
STR_DAY = "day"
STR_DB = "db"
STR_DEBUG = "debug"
STR_DECODE = "decode"
STR_DESCRIPTION = "description"
STR_DESIGN = "design"
STR_DEVICE = "device"
STR_DIV = "div"
STR_DUMMY = "dummy"
STR_EASY = "easy"
STR_ENGLISH = "english"
STR_ERROR = "error"
STR_ETC = "etc"
STR_EXPIRATION = "expiration"
STR_FIRST = "first"
STR_FONT = "font"
STR_FUNCTION = "function"
STR_GEMINI = "gemini"
STR_HARD = "hard"
STR_HOLIDAY = "holiday"
STR_HOST = "host"
STR_ID = "id"
STR_IMG = "img"
STR_INDEX = "index"
STR_INFO = "info"
STR_INPUT = "input"
STR_IP = "ip"
STR_ITEM = "item"
STR_KAKAO = "kakao"
STR_KEY = "key"
STR_KEYWORD = "keyword"
STR_KPOP = "kpop"
STR_LABEL = "label"
STR_LABELS = "labels"
STR_LEVEL = "level"
STR_LINE = "line"
STR_LOCAL = "local"
STR_LOG = "log"
STR_LOGIN = "login"
STR_LOGOUT = "logout"
STR_LOWER = "lower"
STR_MASTER = "master"
STR_MEDIUM = "medium"
STR_MESSAGE = "message"
STR_MONGO = "mongo"
STR_MONTH = "month"
STR_NAME = "name"
STR_NISA = "nisa"
STR_NOTIFY = "notify"
STR_NUMBER = "number"
STR_OS = "os"
STR_OUTPUT = "output"
STR_PATH = "path"
STR_PHRASE = "phrase"
STR_PROMPT = "prompt"
STR_REQUEST = "request"
STR_REST = "rest"
STR_RESPONSE = "response"
STR_RESULT = "result"
STR_SERVER = "server"
STR_STATUS = "status"
STR_TERM = "term"
STR_TEST = "test"
STR_TIME = "time"
STR_TITLE = "title"
STR_TOKEN = "token"
STR_TOTAL = "total"
STR_TYPE = "type"
STR_UNLINK = "unlink"
STR_UPDATE = "update"
STR_UPPER = "upper"
STR_URL = "url"
STR_USER = "user"
STR_WEEK = "week"
STR_YEAR = "year"

STR_AI = "AI"
STR_AI_NEWS = "ai_news"
STR_ENV_VAR = "env_var"
STR_JAPAN = "Japan"
STR_KOREA = "Korea"
STR_LINE_API = "LINE API"
STR_PHRASE_KO = "phrase_ko"
STR_SECRET_KEY = "secret_key"
STR_USER_INFO = "userInfo"
STR_ZIP_CODE = "zipCode"

STR_BACKUP_JA = "バックアップ"
STR_CHARSET_JA = "文字コード"
STR_COMPANY_JA = "会社"
STR_CONTENTS_JA = "内容"
STR_DATE_JA = "日付"
STR_DIV_JA = "区分"
STR_DRAMA_JA = "ドラマ"
STR_ENT_JA = "エンタメ"
STR_EXPIRE_JA = "有効期限"
STR_FILE_JA = "ファイル"
STR_IMG_JA = "イメージ"
STR_JAPAN_JA = "日本"
STR_KOREA_JA = "韓国"
STR_KOREAN_JA = "韓国語"
STR_LINK_JA = "リンク"
STR_LOGIN_JA = "ログイン"
STR_LOGOUT_JA = "ログアウト"
STR_MAN_JA = "男性"
STR_MESSAGE_JA = "メッセージ"
STR_NEWS_JA = "ニュース"
STR_NIKKEI_JA = "日経"
STR_NOTIFY_JA = "通知"
STR_PATH_JA = "パス"
STR_RANKING_JA = "ランキング"
STR_STATUS_JA = "状態"
STR_SYSTEM_JA = "システム"
STR_TIME_JA = "時間"
STR_TITLE_JA = "タイトル"
STR_TOKEN_JA = "トークン"
STR_TYPE_JA = "タイプ"
STR_WOMAN_JA = "女性"
STR_X_TREND_JA = "Xトレンド"

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
LOG_MASKING = "XXXXX"
LIST_LOG_MASKING = ["kobe-", "koyeb", "token", "kapi.", "kauth", "oauth", "line."]

##### 曜日リスト #####
LIST_WEEKDAY = ["月", "火", "水", "木", "金", "土", "日"]

##### LINE #####
# メッセージタイプ
MSG_TYPE_TXT = "text"
MSG_TYPE_IMG = "image"
MSG_TYPE_TMP = "template"
MSG_TYPE_FLEX = "flex"
MSG_TYPE_CAROUSEL = "carousel"
MSG_TYPE_BUBBLE = "bubble"

# タイトル
DIV_MARK = "*----*----*----*----*----*"
MARK_PATTERN_1 = "-"
MARK_PATTERN_2 = "■"
MARK_PATTERN_3 = "="

##### ファンド #####
FUND_NO_SP_500 = "182809"
FUND_NO_AI = "179702"
FUND_NO_US_TECH = "173905"
FUND_NAME_SP_500 = "S&P500"
FUND_NAME_AI = "イノベAI"
FUND_NAME_US_TECH = "USテクノロ"

LIST_FUND_NO = [FUND_NO_SP_500, FUND_NO_AI, FUND_NO_US_TECH]
LIST_FUND_NAME = [FUND_NAME_SP_500, FUND_NAME_AI, FUND_NAME_US_TECH]


##### EX（為替） #####
# JPY単位
JPY_LIST = [100, 1000, 10000]

# カラムリスト
EX_LIST = [
    STR_KRW,
    STR_USD,
    STR_TWD,
    STR_THB,
    STR_PHP,
    STR_VND,
]
EX_LIST_JA = [
    STR_KRW_JA,
    STR_USD_JA,
    STR_TWD_JA,
    STR_THB_JA,
    STR_PHP_JA,
    STR_VND_JA,
]

##### MLB #####
# ID
TEAM_ID_LAD = 119
PLAYER_ID_OHTANI = 660271
PLAYER_ID_YAMAMOTO = 808967
PLAYER_ID_KIM = 808975

LIST_TEAM_ID = [TEAM_ID_LAD]
LIST_PLAYER_ID_LAD = [PLAYER_ID_OHTANI, PLAYER_ID_YAMAMOTO, PLAYER_ID_KIM]
LIST_PLAYER_ID = [LIST_PLAYER_ID_LAD]

##### 掲示板 #####
LIST_BOARD_APP = ["LINE", "Travel", "Kakao", "Server"]
LIST_BOARD_CATEGORY = ["Review", "Memo", "Error", "Etc."]
LIST_BOARD_TYPE = ["Add", "Modify", "Design", "Etc."]
LIST_BOARD_STATUS = ["New", "Progress", "Pend", "Done"]

# ステータス
STATUS_NEW = 0
STATUS_PROGRESS = 1
STATUS_PEND = 2
STATUS_DONE = 3
STATUS_DELETE = 4

##### URL #####
# サイトURL
URL_GOOGLE = "https://www.google.com"
URL_TENKI = "https://tenki.jp"
URL_CANCAM = "https://cancam.jp"
URL_SMBC_FUND = "https://www.smd-am.co.jp/fund"
URL_NAVER = "https://www.naver.com"
URL_NAVER_MO = "https://m.naver.com"
URL_NAVER_STOCK_MO = "https://m.stock.naver.com"
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
URL_IP_INFO = "https://ipinfo.io"
URL_LINE_API = "https://api.line.me"
URL_KAKAO_AUTH = "https://kauth.kakao.com"
URL_KAKAO_API = "https://kapi.kakao.com"

##### アプリケーション名 #####
APP_BOARD = "board"
APP_CAFE = "cafe"
APP_DASHBOARD = "dashboard"
APP_DRAMA = "drama"
APP_IT_QUIZ = "itQuiz"
APP_LCC = "lcc"
APP_MLB = "mlb"
APP_NEWS = "news"
APP_NUMBER = "number"
APP_RANKING = "ranking"
APP_REVIEW = "review"
APP_SITE = "site"
APP_STUDY = "study"
APP_SUDOKU = "sudoku"
APP_TODAY = "today"
APP_TODAY_KOREA = "today_korea"
APP_TRAVEL = "travel"
APP_TV = "tv"
APP_USER = "user"

APP_IT_QUIZ_DESIGN = f"{APP_IT_QUIZ}_{STR_DESIGN}"
APP_IT_QUIZ_PROMPT = f"{APP_IT_QUIZ}_{STR_PROMPT}"
APP_KAKAO_DESIGN = f"{STR_KAKAO}_{STR_DESIGN}"
APP_LOCAL_DESIGN = f"{STR_LOCAL}_{STR_DESIGN}"
APP_TRAVEL_DESIGN = f"{APP_TRAVEL}_{STR_DESIGN}"
APP_URL_DESIGN = f"{STR_URL}_{STR_DESIGN}"

##### アプリケーションリスト #####
LIST_APP_SERVER = [
    APP_TODAY,
    APP_NEWS,
    APP_DRAMA,
    APP_RANKING,
    APP_LCC,
    APP_TV,
    APP_STUDY,
]
LIST_APP_SITE = [APP_SITE, APP_CAFE, APP_TRAVEL, APP_BOARD]
LIST_APP_SERVER_KOREA = [APP_TODAY_KOREA]
LIST_APP_ALL = LIST_APP_SERVER + LIST_APP_SITE + LIST_APP_SERVER_KOREA

LIST_APP_SERVER_2 = [APP_DASHBOARD, STR_KOREA]
LIST_APP_SERVER_ALL = LIST_APP_SERVER + LIST_APP_SERVER_KOREA + LIST_APP_SERVER_2

LIST_APPS_ALL = [
    APP_TRAVEL,
    APP_TRAVEL_DESIGN,
    APP_NUMBER,
    APP_SUDOKU,
    APP_IT_QUIZ,
    APP_IT_QUIZ_DESIGN,
    APP_IT_QUIZ_PROMPT,
    APP_REVIEW,
    APP_DASHBOARD,
    APP_URL_DESIGN,
    APP_KAKAO_DESIGN,
    APP_LOCAL_DESIGN,
    STR_GEMINI,
]

LIST_APP_NEWS = [APP_NEWS, APP_TODAY, APP_TODAY_KOREA]
LIST_APP_ENTERTAINMENT = [
    APP_DRAMA,
    APP_IT_QUIZ,
    APP_MLB,
    APP_NUMBER,
    APP_RANKING,
    APP_SUDOKU,
    APP_TV,
    STR_GEMINI,
]
LIST_APP_SERVICE = [APP_CAFE, APP_LCC, APP_SITE, APP_STUDY, APP_TRAVEL]
LIST_APP_MANAGEMENT = [APP_BOARD, APP_DASHBOARD, APP_REVIEW, APP_USER]
LIST_APP_DOCUMENT = [
    APP_IT_QUIZ_DESIGN,
    APP_IT_QUIZ_PROMPT,
    APP_KAKAO_DESIGN,
    APP_TRAVEL_DESIGN,
    APP_URL_DESIGN,
]

LIST_CATEGORY = ["news", "entertainment", "service", "management", "document"]
LIST_APP_CATEGORY = [
    LIST_APP_NEWS,
    LIST_APP_ENTERTAINMENT,
    LIST_APP_SERVICE,
    LIST_APP_MANAGEMENT,
    LIST_APP_DOCUMENT,
]

LIST_APP_KOREA = [
    APP_TODAY,
    APP_TRAVEL,
    APP_NUMBER,
    APP_SUDOKU,
    APP_IT_QUIZ,
    APP_REVIEW,
    TYPE_LIST,
]

LIST_APP_NUM_OFF = [
    APP_BOARD,
    APP_CAFE,
    APP_SITE,
    APP_STUDY,
    APP_TODAY,
    APP_TODAY_KOREA,
    APP_TRAVEL,
]

LIST_APP_AUTH_OFF = [APP_CAFE, APP_TRAVEL]


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
PATH_KAKAO = get_path(STR_KAKAO)
PATH_KAKAO_LOGIN = f"{PATH_KAKAO}{PATH_LOGIN}"
PATH_KAKAO_TODAY = f"{PATH_KAKAO}{get_path(APP_TODAY)}"

##### HTMLファイル名 #####
HTML_INDEX = get_html(STR_INDEX)
HTML_RESULT = get_html(STR_RESULT)
HTML_RESULT_2 = get_html(f"{STR_RESULT}2")
HTML_USER_INFO = get_html(STR_USER_INFO)

if __name__ == MAIN_FUNCTION:
    data = f"[{DATE_WEEKDAY, HTML_INDEX}]"
    type_name = type(data).__name__
    print(STR_TYPE_JA, type_name)
    print(data)
