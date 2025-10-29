// 記号
const SYM_BLANK = "";
const SYM_NEW_LINE = "\n";
const SYM_LEVEL = "🌟";

// タグ
const TAG_HEAD = "head";
const TAG_DIV = "div";
const TAG_H1 = "h1";
const TAG_H2 = "h2";
const TAG_H3 = "h3";
const TAG_FORM = "form";
const TAG_TABLE = "table";
const TAG_TR = "tr";
const TAG_TH = "th";
const TAG_TD = "td";
const TAG_UL = "ul";
const TAG_LI = "li";
const TAG_INPUT = "input";
const TAG_SELECT = "select";
const TAG_OPTION = "option";
const TAG_BUTTON = "button";
const TAG_TEXTAREA = "textarea";
const TAG_LABEL = "label";
const TAG_A = "a";
const TAG_FOOTER = "footer";
const TAG_BR = "br";

// 属性値
const ATTR_BLOCK = "block";
const ATTR_NONE = "none";

// モード
const MODE_IMG = "img";
const MODE_TXT = "txt";

// ユーザ
const AUTH_ADMIN = "admin";
const AUTH_DEV = "dev";
const AUTH_GUEST = "guest";

// 文字列
const STR_APP = "app";
const STR_CATEGORY = "category";
const STR_TYPE = "type";
const STR_STATUS = "status";
const STR_CONTENTS = "contents";
const STR_USER_NAME = "userName";
const STR_MESSAGE = "message";

const STR_LINES = "Lines";
const STR_STATIONS = "Stations";

const STR_SELECT_JA = "選択";
const STR_ZIP_CD_JA = "郵便番号";
const STR_LINE_JA = "沿線";
const STR_STATION_JA = "駅";

// ID
const ID_SEX = "sex";
const ID_ZIP_CD = "zipCd";
const ID_PREF = "pref";
const ID_TOWN = "town";
const ID_LINE = "line";
const ID_STATION = "station";

const BUTTON_LOGIN = "Login";
const BUTTON_LOGOUT = "Logout";

const COLOR_RED = "red";
const COLOR_GREEN = "green";

const ALIGN_CENTER = "center";

const LEVEL_EASY = "easy";
const LEVEL_MEDIUM = "medium";
const LEVEL_HARD = "hard";

// 言語名（表示用）
const LANG_NM_JA = "日本語";
const LANG_NM_KO = "한국어";
const LANG_NM_EN = "English";
const LIST_LANG_NM = [LANG_NM_JA, LANG_NM_KO, LANG_NM_EN];

// 言語コード（データ参照用）
const LANG_CD_JA = "ja";
const LANG_CD_KO = "ko";
const LANG_CD_EN = "en";
const LIST_LANG_CD = [LANG_CD_JA, LANG_CD_KO, LANG_CD_EN];

// 都市コード・都市名リスト
const LIST_CITY_VAL = ["tokyo", "seoul", "taipei", "hanoi", "bangkok", "manila"];
const LIST_CITY_JA = ["東京", "ソウル", "台北", "ハノイ", "バンコク", "マニラ"];
const LIST_CITY_KO = ["도쿄", "서울", "타이베이", "하노이", "방콕", "마닐라"];
const LIST_CITY_EN = ["Tokyo", "Seoul", "Taipei", "Hanoi", "Bangkok", "Manila"];

// アプリケーションリスト
const APP_TODAY = "today";
const APP_SITE = "site";
const APP_DRAMA = "drama";
const APP_RANKING = "ranking";
const APP_LCC = "lcc";
const APP_TV = "tv";
const APP_NEWS = "news";
const APP_STUDY = "study";
const APP_BOARD = "board";
const APP_USER = "user";

const LIST_APP_GUEST_MO = [APP_DRAMA, APP_RANKING, APP_LCC, APP_TV];
const LIST_APP_GUEST = [APP_TODAY, APP_SITE].concat(LIST_APP_GUEST_MO);
const LIST_APP_NOT_GUEST = [APP_NEWS, APP_STUDY, APP_BOARD, APP_USER];
const LIST_APP = LIST_APP_GUEST.concat(LIST_APP_NOT_GUEST);

const APP_TRAVEL = "travel";
const APP_NUMBER = "number";
const APP_IT_QUIZ = "itQuiz";
const APP_REVIEW = "review";
const LIST_APP_KOREA = [APP_TODAY, APP_TRAVEL, APP_NUMBER, APP_IT_QUIZ, APP_REVIEW, APP_BOARD]

const APP_KAKAO = "kakao";

// アプリケーション連番：お気に入り表示用
const NUM_APP_TODAY = "0";
const NUM_APP_SITE = "1";
const NUM_APP_DRAMA = "2";
const NUM_APP_RANKING = "3";
const NUM_APP_LCC = "4";
const NUM_APP_TV = "5";
const NUM_APP_NEWS = "6";
const NUM_APP_STUDY = "7";
const NUM_APP_BOARD = "8";

// タイトル
const TITLE_SYSTEM = "Kobe-Dev Demo System";
const TITLE_TRAVEL = "🌏 Travel & Life";
const TITLE_NUMBER_PLATE = "🚙Number Plate Game";
const TITLE_NUMBER_PLATE_KO = "자동차 번호판 게임";
const TITLE_REVIEW = "🌈 Review Page 🌈";
const TITLE_DESIGN = "📄設計書";
const TITLE_DASH_BOARD = "📊 Dash Board";

const TH_NO = "No.";

// ゲームルール
const LIST_GAME_RULE = [
  "4つの数字を使い正しい数式を作る",
  "イコール(=)：必ず1つのみ使用",
  "四則演算(+ - * /)：必ず1つ以上使用",
  "使用可能な数式記号 + - * / = √ ⁰¹²",
  "backボタン：一つ前の状態に戻る"
];
const LIST_GAME_RULE_KO = [
  "4개의 숫자를 순서대로 한번씩 이용해 수식 만들기",
  "등호(=)는 반드시 한번 사용",
  "사칙연산(+ - * /)은 1개 이상 사용",
  "사용가능한 수식기호 + - * / = √ ⁰¹²",
  "back버튼：앞의 상태로 되돌리기"
];

// レビュー
const LIST_REVIEW_APP = ["LINE", "Travel", "Kakao", "Server"]
const LIST_REVIEW_CATEGORY = ["Review", "Memo", "Error", "Etc."]
const LIST_REVIEW_TYPE = ["Add", "Modify", "Design", "Etc."];
const LIST_REVIEW_STATUS = ["New", "Progress", "Pend", "Done"]

// API
const METHOD_GET = "GET";
const METHOD_POST = "POST";

// URL
const URL_SERVER = "https://kobe-dev.koyeb.app";
const URL_LOCAL = "http://127.0.0.1:5000";

const URL_ZIP_API = "/api/zipCode";
const URL_ZIP_SERVER = `${URL_SERVER}${URL_ZIP_API}`;
const URL_ZIP_LOCAL = `${URL_LOCAL}${URL_ZIP_API}`;

const URL_ADDR_API = "https://express.heartrails.com/api/json?method=get";
const URL_LINE_API = `${URL_ADDR_API}${STR_LINES}`;
const URL_STATION_API = `${URL_ADDR_API}${STR_STATIONS}`;

const URL_GEMINI_API = "/gemini/api";
const URL_GEMINI_SERVER = `${URL_SERVER}${URL_GEMINI_API}`;
const URL_GEMINI_LOCAL = `${URL_LOCAL}${URL_GEMINI_API}`;

const URL_IMG_GEMINI = "/img/gemini";
const URL_GEMINI_IMG_SERVER = `${URL_SERVER}${URL_IMG_GEMINI}`;
const URL_GEMINI_IMG_LOCAL = `${URL_LOCAL}${URL_IMG_GEMINI}`;

const URL_NUMBER_RANKING_API = "/number/ranking";
const URL_NUMBER_RANKING_SERVER = `${URL_SERVER}${URL_NUMBER_RANKING_API}`;
const URL_NUMBER_RANKING_LOCAL = `${URL_LOCAL}${URL_NUMBER_RANKING_API}`;

const URL_QUIZ_RANKING_API = "/quiz/ranking";
const URL_QUIZ_RANKING_SERVER = `${URL_SERVER}${URL_QUIZ_RANKING_API}`;
const URL_QUIZ_RANKING_LOCAL = `${URL_LOCAL}${URL_QUIZ_RANKING_API}`;

const URL_BOARD_ADD_API = "/board/add";
const URL_BOARD_ADD_SERVER = `${URL_SERVER}${URL_BOARD_ADD_API}`;
const URL_BOARD_ADD_LOCAL = `${URL_LOCAL}${URL_BOARD_ADD_API}`;

const URL_BOARD_UPDATE_API = "/board/update";
const URL_BOARD_UPDATE_SERVER = `${URL_SERVER}${URL_BOARD_UPDATE_API}`;
const URL_BOARD_UPDATE_LOCAL = `${URL_LOCAL}${URL_BOARD_UPDATE_API}`;

const URL_GEMINI_ITEMS_API = "/api/geminiData/items";
const URL_GEMINI_ITEMS_SERVER = `${URL_SERVER}${URL_GEMINI_ITEMS_API}`;
const URL_GEMINI_ITEMS_LOCAL = `${URL_LOCAL}${URL_GEMINI_ITEMS_API}`;

const URL_TRAVEL_API = "/api/travelData/items";
const URL_TRAVEL_SERVER = `${URL_SERVER}${URL_TRAVEL_API}`;
const URL_TRAVEL_LOCAL = `${URL_LOCAL}${URL_TRAVEL_API}`;

const URL_LANG_API = "/api/langData/items";
const URL_LANG_SERVER = `${URL_SERVER}${URL_LANG_API}`;
const URL_LANG_LOCAL = `${URL_LOCAL}${URL_LANG_API}`;

const URL_IT_QUIZ_API = "/api/itQuizData/items";
const URL_IT_QUIZ_SERVER = `${URL_SERVER}${URL_IT_QUIZ_API}`;
const URL_IT_QUIZ_LOCAL = `${URL_LOCAL}${URL_IT_QUIZ_API}`;

const URL_DASHBOARD_API = "/json/dashboard";
const URL_DASHBOARD_SERVER = `${URL_SERVER}${URL_DASHBOARD_API}`;
const URL_DASHBOARD_LOCAL = `${URL_LOCAL}${URL_DASHBOARD_API}`;

// メッセージ
const MSG_VAL_NOT_EXIST = "が存在しません";
const MSG_ERR_PASSWORD_NOT_MATCH = "パスワードが一致しません";
const MSG_ERR_MENU_NO_CHECKED_ELEMENTS = "メニューは、1つ以上チェックしてください";
const MSG_ERR_MENU_CHECKED_MAX = "メニューは、最大5つまでチェックしてください";

const MSG_OK_SEND = "送信成功！";
const MSG_ERR_SEND = "送信エラー";
const MSG_ERR_LOAD_JSON = "JSONファイルの読み込みに失敗しました!";

const MSG_ANSWER_EXAMPLE = "解の例:";
const MSG_OK_ANSWER = "正解です!";
const MSG_OK_RANK = "新記録！ランクインしました！";
const MSG_INPUT_USER = "ユーザ名(英数字)を入力してください。";

const MSG_ERR_NO_ANSWER = "この問題には解が見つかりませんでした";
const MSG_ERR_NO_INPUT = "入力値がありません";
const MSG_ERR_DIGIT = "4つの数字を1回ずつ使ってください!";
const MSG_ERR_EQUAL = "イコールは1つだけ使ってください!";
const MSG_ERR_FORMAT = "数式の形式が正しくありません!";
const MSG_ERR_DIVIDE_BY_ZERO = "ゼロ除算はできません!";
const MSG_ERR_MATCH = "計算結果が一致しません!";
const MSG_ERR_RANK = "ランク送信に失敗しました!";

const MSG_OK_ANSWER_KO = "정답입니다!";
const MSG_OK_RANK_KO = "신기록！랭킹 등록！";
const MSG_INPUT_USER_KO = "게임 아이디(최대10문자)를 입력하세요.";

const MSG_ERR_NO_ANSWER_KO = "이 문제에는 해답이 존재하지 않습니다.";
const MSG_ERR_NO_INPUT_KO = "입력한 정보가 없습니다.";
const MSG_ERR_DIGIT_KO = "4개 숫자를 순서별로 1번씩만 입력하세요.";
const MSG_ERR_EQUAL_KO = "등호(=)를 반드시 한번 사용하세요!";
const MSG_ERR_FORMAT_KO = "수식이 바르지 않습니다!";
const MSG_ERR_DIVIDE_BY_ZERO_KO = "0으로 나눌 수 없습니다!";
const MSG_ERR_MATCH_KO = "계산결과가 일치하지 않습니다!";
const MSG_ERR_RANK_KO = "랭킹 등록에 실패했습니다.";

const MSG_INPUT_USER_EN = "Input your nickname.";
const MSG_OK_SEND_EN = "Send OK!";
const MSG_ERR_SEND_EN = "Send NG!!";

const MSG_OK_RANK_EN = "Ranking updated！"
const MSG_ERR_RANK_EN = "Failed to update ranking."

const MSG_ERR_NO_INPUT_EN = "No input data.";
const MSG_ERR_LOAD_JSON_EN = "Failed to load json file!"

// ヘッダー情報
const CONTENTS_HEAD_1 = `
  <meta http-equiv="Content-Type" content="text/html" charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="/templates/jquery-3.6.1.min.js"></script>
`;

// ヘッダー情報
const CONTENTS_HEAD = `
  ${CONTENTS_HEAD_1}
  <link rel="stylesheet" href="/templates/common.css" />
  <link rel="stylesheet" href="/templates/style.css" />
  <link rel="icon" href="/templates/favicon.ico" type="image/x-icon">
`;

// ヘッダー情報
const CONTENTS_HEAD_2 = `
  ${CONTENTS_HEAD_1}
  <link rel="stylesheet" href="/templates/common.css" />
  <link rel="stylesheet" href="/templates/style2.css" />
`;