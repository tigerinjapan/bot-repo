// 記号
const SYM_BLANK = "";
const SYM_LEVEL = "🌟";

// タグ
const TAG_HEAD = "head";
const TAG_DIV = "div";
const TAG_H1 = "h1";
const TAG_FORM = "form";
const TAG_TABLE = "table";
const TAG_TR = "tr";
const TAG_TH = "th";
const TAG_TD = "td";
const TAG_UL = "ul";
const TAG_LI = "li";
const TAG_SELECT = "select";
const TAG_OPTION = "option";
const TAG_TEXTAREA = "textarea";
const TAG_BUTTON = "button";
const TAG_LABEL = "label";

// 文字列
const STR_APP = "app";
const STR_CATEGORY = "category";
const STR_TYPE = "type";
const STR_CONTENTS = "contents";
const STR_USER_NAME = "userName";
const STR_MESSAGE = "message";

const COLOR_RED = "red";
const COLOR_GREEN = "green";

const LEVEL_EASY = "easy";
const LEVEL_MEDIUM = "medium";
const LEVEL_HARD = "hard";

const TITLE_NUMBER_PLATE = "🚙Number Plate Game";
const TITLE_NUMBER_PLATE_KO = "자동차 번호판 게임";

// 言語名（表示用）
const LANG_JA = "日本語";
const LANG_KO = "한국어";
const LANG_EN = "English";
const LIST_LANG = [LANG_JA, LANG_KO, LANG_EN];

// 言語コード（データ参照用）
const LANG_CD_JA = "ja";
const LANG_CD_KO = "ko";
const LANG_CD_EN = "en";
const LIST_LANG_VAL = [LANG_CD_JA, LANG_CD_KO, LANG_CD_EN];

// 都市コード・都市名リスト
const LIST_CITY_VAL = ["tokyo", "seoul", "taipei", "hanoi", "bangkok", "manila"];
const LIST_CITY_JA = ["東京", "ソウル", "台北", "ハノイ", "バンコク", "マニラ"];
const LIST_CITY_KO = ["도쿄", "서울", "타이베이", "하노이", "방콕", "마닐라"];
const LIST_CITY_EN = ["Tokyo", "Seoul", "Taipei", "Hanoi", "Bangkok", "Manila"];

// ゲームルール
const LIST_GAME_RULE = [
  "4つの数字を使い正しい数式を作る",
  "四則演算(+ - * /)：最大3つ使用",
  "イコール(=)：必ず1つのみ使用"
];
const LIST_GAME_RULE_KO = [
  "4개의 숫자를 순서대로 한번씩 이용해 수식 만들기",
  "사칙연산(+ - * /)은 최대 3개가 사용가능.",
  "등호(=)는 반드시 한번 사용!"
];

// メッセージ
const MSG_OK_SEND = "送信成功！";
const MSG_ERR_SEND = "送信エラー";

const MSG_INFO_ANSWER_EXAMPLE = "解の例:";
const MSG_INFO_OK_ANSWER = "正解です!";
const MSG_INFO_OK_RANK = "新記録！ランクインしました！";
const MSG_INFO_INPUT_USER = "ユーザ名(英数字)を入力してください。";

const MSG_ERR_NO_ANSWER = "この問題には解が見つかりませんでした";
const MSG_ERR_NO_INPUT = "入力値がありません";
const MSG_ERR_DIGIT = "4つの数字を1回ずつ使ってください!";
const MSG_ERR_EQUAL = "イコールは1つだけ使ってください!";
const MSG_ERR_FORMAT = "数式の形式が正しくありません!";
const MSG_ERR_DIVIDE_BY_ZERO = "ゼロ除算はできません!";
const MSG_ERR_MATCH = "計算結果が一致しません!";
const MSG_ERR_RANK = "ランク送信に失敗しました!";
const MSG_ERR_LOAD_JSON = "JSONファイルの読み込みに失敗しました!";

const MSG_INFO_OK_ANSWER_KO = "정답입니다!";
const MSG_INFO_OK_RANK_KO = "신기록！랭킹 등록！";
const MSG_INFO_INPUT_USER_KO = "게임 아이디(최대10문자)를 입력하세요.";

const MSG_ERR_NO_ANSWER_KO = "이 문제에는 해답이 존재하지 않습니다.";
const MSG_ERR_NO_INPUT_KO = "입력한 정보가 없습니다.";
const MSG_ERR_DIGIT_KO = "4개 숫자를 순서별로 1번씩만 입력하세요.";
const MSG_ERR_EQUAL_KO = "등호(=)를 반드시 한번 사용하세요!";
const MSG_ERR_FORMAT_KO = "수식이 바르지 않습니다!";
const MSG_ERR_DIVIDE_BY_ZERO_KO = "0으로 나눌 수 없습니다!";
const MSG_ERR_MATCH_KO = "계산결과가 일치하지 않습니다!";
const MSG_ERR_RANK_KO = "랭킹 등록에 실패했습니다.";

// URL
const URL_SERVER = "https://kobe-dev.koyeb.app";
const URL_LOCAL = "http://127.0.0.1:5000";

const URL_RANKING_API = "/number/ranking";
const URL_RANKING_SERVER = `${URL_SERVER}${URL_RANKING_API}`;
const URL_RANKING_LOCAL = `${URL_LOCAL}${URL_RANKING_API}`;

const API_BOARD_ADD = "/board/add";
const URL_BOARD_ADD = `${URL_SERVER}${API_BOARD_ADD}`;
const URL_BOARD_LOCAL = `${URL_LOCAL}${API_BOARD_ADD}`;

const URL_TRAVEL_API = "/api/travelData/items";
const URL_TRAVEL_SERVER = `${URL_SERVER}${URL_TRAVEL_API}`;
const URL_TRAVEL_LOCAL = `${URL_LOCAL}${URL_TRAVEL_API}`;

const URL_LANG_API = "/api/langData/items";
const URL_LANG_SERVER = `${URL_SERVER}${URL_LANG_API}`;
const URL_LANG_LOCAL = `${URL_LOCAL}${URL_LANG_API}`;

// ヘッダー情報読込
const CONTENTS_HEAD_2 = `
  <meta http-equiv="Content-Type" content="text/html" charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="/templates/style2.css" />
  <script src="/templates/jquery-3.6.1.min.js"></script>
`;