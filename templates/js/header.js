// 記号
const SYM_BLANK = "";

// ユーザ
const AUTH_ADMIN = "admin";
const AUTH_DEV = "dev";
const AUTH_GUEST = "guest";

// アプリケーションリスト
const APP_TODAY = "today";
const APP_NEWS = "news";
const APP_DRAMA = "drama";
const APP_RANKING = "ranking";
const APP_LCC = "lcc";
const APP_TV = "tv";
const APP_STUDY = "study";
const APP_SITE = "site";
const APP_CAFE = "cafe";
const APP_USER = "user";

const LIST_APP_DEV_MO = [APP_NEWS, APP_DRAMA, APP_STUDY, APP_CAFE];
const LIST_APP_GUEST_MO = [APP_DRAMA, APP_RANKING, APP_LCC, APP_TV];
const LIST_APP_GUEST = [APP_TODAY, APP_SITE].concat(LIST_APP_GUEST_MO);
const LIST_APP_NOT_GUEST = [APP_NEWS, APP_STUDY, APP_CAFE, APP_USER];
const LIST_APP = LIST_APP_GUEST.concat(LIST_APP_NOT_GUEST);

// 項目名
const TITLE_SYSTEM = "開発デモシステム";
const TH_NO = "No.";
const BUTTON_LOGIN = "ログイン";
const BUTTON_LOGOUT = "ログアウト";
const BUTTON_SEARCH = "検索";
const BUTTON_SETTING = "設定";

// ヘッダー情報読込
const CONTENTS_HEAD = (`
  <meta http-equiv="Content-Type" content="text/html" charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="/templates/style.css">
  <script src="/templates/jquery-3.6.1.min.js"></script>
`);
document.getElementsByTagName("head")[0].innerHTML = CONTENTS_HEAD;

// 初期表示
function initDisplay() {
  const thSysNmElement = document.getElementById("thSysNm");
  const thNoElement = document.getElementById("thNo");

  if (thSysNmElement) {
    thSysNmElement.textContent = TITLE_SYSTEM;
  }

  if (thNoElement) {
    thNoElement.textContent = TH_NO;
  }
}

// トップメニュー設定
function setTopMenu(userDiv, userNm, appNm) {
  // アプリケーションリスト
  let appList = LIST_APP;
  if (isMobile()) {
    if (userDiv == AUTH_DEV) {
      appList = LIST_APP_DEV_MO; // TODO 画面レイアウト設定をDB保存
    } else if (userDiv == AUTH_GUEST) {
      appList = LIST_APP_GUEST_MO;
    }
  } else {
    if (userDiv == AUTH_GUEST) {
      appList = LIST_APP_GUEST;
    }
  }

  // 配列の初期化
  let liMenuList = [];
  for (let i = 0; i < appList.length; i++) {
    appDiv = appList[i];
    liMenuList.push(`
      <li><a href="/app/${appDiv}" id="${appDiv}">${appDiv}</a></li>
    `);
  }

  // 配列を文字列に変換
  const liMenu = liMenuList.join(SYM_BLANK);

  // ログアウトメニュー
  const liLogout = `<li><a href="/logout"><b>` + userNm + ` </b>` + BUTTON_LOGOUT + `</a></li>`;

  // トップメニュー
  let topMenu = liMenu + liLogout;
  if (isMobile()) {
    topMenu = liLogout + liMenu;
  }

  const topMenuList = `<ul>` + topMenu + `</ul>`;

  document.getElementById("topMenu").innerHTML = topMenuList;

  // メニュー押下時、背景色設定
  const screenId = document.getElementById(appNm);
  screenId.setAttribute("style", "background-color: peru;");
}

function isMobile() {
  // スマホ判定用の変数
  let isMobileDevice = false;

  // ユーザーエージェントを利用した判定
  const userAgent = navigator.userAgent;

  // 一般的なスマホデバイスのユーザーエージェントに基づいて判定
  if (/android/i.test(userAgent)) {
    isMobileDevice = true; // Androidデバイス
  } else if (/iPhone|iPad|iPod/i.test(userAgent)) {
    isMobileDevice = true; // iOSデバイス
  }

  return isMobileDevice; // デスクトップまたはその他のデバイス
}

// チェックメッセージ表示
function displayChkMsg() {
  const chkMsgElem = document.getElementById("chkMsg");

  window.addEventListener("load", function () {
    if (chkMsgElem) {
      const chkMsg = chkMsgElem.textContent;
      if (chkMsg === SYM_BLANK || chkMsg === undefined) {
        chkMsgElem.style.display = "none";
      } else {
        chkMsgElem.style.color = "red";
        chkMsgElem.style.textAlign = "center";
      }
    }
  });
}
