// ユーザ
const AUTH_ADMIN = "admin";
const AUTH_DEV = "dev";
const AUTH_GUEST = "guest";

// アプリケーションリスト
const APP_TODAY = "today";
const APP_NEWS = "news";
const APP_KOREA = "korea";
const APP_RANKING = "ranking";
const APP_LCC = "lcc";
const APP_TV = "tv";
const APP_STUDY = "study";
const APP_SITE = "site";
const LIST_APP = [APP_TODAY, APP_NEWS, APP_KOREA, APP_RANKING, APP_LCC, APP_TV, APP_STUDY, APP_SITE];
const LIST_APP_NOT_GUEST = [APP_NEWS, APP_STUDY];
const LIST_APP_GUEST = LIST_APP.filter(item => !LIST_APP_NOT_GUEST.includes(item));

// メニュー
const MENU_TOP = "トップ";
const MENU_TODAY = "今日の生活情報";
const MENU_NEWS = "今日のニュース";
const MENU_KOREA = "韓国ニュース";
const MENU_RANKING = "ランキングニュース";
const MENU_LCC = "LCCニュース";
const MENU_TV = "TV番組";
const MENU_STUDY = "ニュース韓国語";
const MENU_SITE = "お気に入りサイト";
const LIST_MENU = [MENU_TODAY, MENU_NEWS, MENU_KOREA, MENU_RANKING, MENU_LCC, MENU_TV, MENU_STUDY, MENU_SITE];
const LIST_MENU_NOT_GUEST = [MENU_NEWS, MENU_STUDY];
const LIST_MENU_GUEST = LIST_MENU.filter(item => !LIST_MENU_NOT_GUEST.includes(item));

// 項目名
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
  document.write(`<div class="topMenu"><ul>`);

  appList = LIST_APP;
  menuList = LIST_MENU;
  if (userDiv == AUTH_GUEST) {
    appList = LIST_APP_GUEST;
    menuList = LIST_MENU_GUEST;
  }

  for (let i = 0; i < appList.length; i++) {
    appDiv = appList[i];
    document.write(`
      <li><a href="/app/${appDiv}" id="${appDiv}">${appDiv}</a></li>
    `);
  }

  document.write(`
    <li><a href="/logout"><span>`+ userNm + `</span>` + BUTTON_LOGOUT + `</a></li>
    </ul></div>`);

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
