// ユーザ
const AUTH_ADMIN = "admin";
const AUTH_DEV = "dev";
const AUTH_GUEST = "guest";

// 画面メニュー
const MENU_TOP = "トップ";
const MENU_TODAY_INFO = "今日の生活情報";
const MENU_NEWS = "今日のニュース";
const MENU_KOREA = "韓国ニュース";
const MENU_LCC = "LCCニュース";
const MENU_TV = "韓国TV番組";

const TITLE_SYSTEM = "開発デモシステム";
const INPUT_ID = "ID";
const INPUT_PW = "パスワード";
const TH_NO = "No.";
const BUTTON_LOGIN = "ログイン";
const BUTTON_LOGOUT = "ログアウト";
const BUTTON_SEARCH = "検索";

// 記号
const SYM_BLANK = "";

// ヘッダー情報読込
document.write(`
  <meta http-equiv="Content-Type" content="text/html" charset="UTF-8">
  <link rel="stylesheet" href="/templates/style.css">
  <script src="/templates/footer.js"></script>
  <script src="/templates/jquery-3.6.1.min.js"></script>
`);

// ヘッダー情報書込
function writeHeader(userDiv, userNm, appNm) {
  // ユーザ名
  userNm = "【" + userNm + "】";

  // トップメニュー
  document.write(`
    <div class="topMenu">
      <ul>
          <li><a href="/today" id="today">` + MENU_TODAY_INFO + `</a></li>
          <li><a href="/news" id="news">` + MENU_NEWS + `</a></li>
          <li><a href="/korea" id="korea">` + MENU_KOREA + `</a></li>
          <li><a href="/lcc" id="lcc">` + MENU_LCC + `</a></li>
          <li><a href="/tv" id="tv">` + MENU_TV + `</a></li>
          <li><a href="/logout"><span>`+ userNm + `</span>` + BUTTON_LOGOUT + `</a></li>
      </ul>
    </div>
  `);

  // メニュー押下時、背景色設定
  var screenId = document.getElementById(appNm);
  screenId.setAttribute("style", "background-color: peru;");
}

// チェックメッセージ表示
function displayChkMsg() {
  $(function () {
    $("#chkMsg").clear;
    $("#thSysNm").text(TITLE_SYSTEM);
    $("#thId").text(INPUT_ID);
    $("#thPw").text(INPUT_PW);
    $("#thNo").text(TH_NO);
    $("#btnLogin").text(BUTTON_LOGIN);
    $("#btnSearch").text(BUTTON_SEARCH);
  });

  $(window).on("load", function () {
    var chkMsg = $("#chkMsg").text();
    if (chkMsg == SYM_BLANK || chkMsg == undefined) {
      $("#chkMsg").hide();
    } else {
      $("#chkMsg").attr("style", "color:red");
      $("#chkMsg").attr("align", "center");
    }
  });
}
