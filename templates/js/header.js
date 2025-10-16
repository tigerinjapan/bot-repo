// ヘッダー情報読込
setElemContentsByTag(TAG_HEAD, CONTENTS_HEAD);

// 初期表示
function initDisplay() {
  const sysNmElem = getElem("sysNm");
  const thNoElem = getElem("thNo");

  if (sysNmElem) {
    document.title = TITLE_SYSTEM;
    sysNmElem.textContent = TITLE_SYSTEM;
  }

  if (thNoElem) {
    thNoElem.textContent = TH_NO;
  }
}

// トップメニュー設定
function setTopMenu(userDiv, userNm, appNm, menuVal) {
  if (userDiv === SYM_BLANK) {
    return;
  }

  let pathDiv = STR_APP;
  let pathDiv2 = SYM_BLANK;
  if (userDiv === APP_KAKAO) {
    pathDiv = userDiv;
    pathDiv2 = `/${userDiv}`;
  }

  // アプリケーションリスト取得
  let appList = getAppList(userDiv, menuVal);

  // 配列の初期化
  let liMenuList = [];
  for (let i = 0; i < appList.length; i++) {
    appDiv = appList[i];
    liMenuList.push(`
      <li><a href="/${pathDiv}/${appDiv}" id="${appDiv}">${appDiv}</a></li>
    `);
  }

  // 配列を文字列に変換
  const liMenu = liMenuList.join(SYM_BLANK);

  // ログアウトメニュー
  const liLogout = `<li><a href="${pathDiv2}/logout"><b>${userNm} </b>${BUTTON_LOGOUT}</a></li>`;

  // トップメニュー
  let topMenu = liMenu + liLogout;
  if (isMobile()) {
    topMenu = liLogout + liMenu;
  }

  const topMenuList = `<ul>${topMenu}</ul>`;

  setElemContents("topMenu", topMenuList);

  if (appNm == "today_korea") {
    appNm = APP_TODAY;
  }

  // メニュー押下時、背景色設定
  const screenId = getElem(appNm);
  screenId.setAttribute("style", "background-color: peru;");
}

// アプリケーションリスト取得
function getAppList(userDiv, menuVal) {
  if (userDiv === APP_KAKAO) {
    return LIST_APP_KOREA;
  }

  let appList = LIST_APP;
  if (isMobile()) {
    if (userDiv === AUTH_GUEST) {
      appList = LIST_APP_GUEST_MO;
    } else {
      appList = [];
      for (let j = 0; j < menuVal.length; j++) {
        let val = parseInt(menuVal[j]);

        for (let i = 0; i < LIST_APP.length; i++) {
          appList.push(LIST_APP[val]);
          break;
        }
      }
    }

  } else {
    if (userDiv === AUTH_GUEST) {
      appList = LIST_APP_GUEST;
    }
  }

  return appList;
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
  const chkMsgElem = getElem("chkMsg");

  window.addEventListener("load", function () {
    if (chkMsgElem) {
      const chkMsg = chkMsgElem.textContent;
      if (chkMsg === SYM_BLANK || chkMsg === undefined) {
        chkMsgElem.style.display = ATTR_NONE;
      } else {
        chkMsgElem.style.color = COLOR_RED;
        chkMsgElem.style.textAlign = ALIGN_CENTER;
      }
    }
  });
}

/**
 * ダイアログを表示する関数
 * @param {string} title - ダイアログのタイトル
 * @param {string} text - ダイアログの本文
 */
function openDialog(title, text) {
  // ダイアログ要素取得
  const dialog = createElem(TAG_DIV, "dialog", "searchResult");

  const parentElemId = "dialog-content";
  const dialog_content = createElem(TAG_DIV, parentElemId, "dialog");

  createElem(TAG_H3, "dialog-title", parentElemId);
  setElemText("dialog-title", title);

  const selectList = [
    // [STR_APP, LIST_REVIEW_APP, 3],
    // [STR_CATEGORY, LIST_REVIEW_CATEGORY, 1],
    // [STR_TYPE, LIST_REVIEW_TYPE, 1],
    [STR_STATUS, LIST_REVIEW_STATUS, 1],
  ];

  for (const [elemId, txtList, initValIdx] of selectList) {
    createElem(TAG_LABEL, elemId, parentElemId);
    createOption(elemId, elemId, txtList, parentElemId, initValIdx);
    createElemNoVal(TAG_BR, parentElemId);
    createElemNoVal(TAG_BR, parentElemId);
  }

  createElem(TAG_TEXTAREA, "dialog-text", parentElemId);
  setElemText("dialog-text", text);

  const closeBtn = createElem(TAG_BUTTON, "close-btn", parentElemId);
  setElemText("close-btn", "×");
  closeBtn.onclick = () => closeDialog();

  const saveBtn = createElem(TAG_BUTTON, "save-btn", parentElemId);
  setElemText("save-btn", "Send");
  saveBtn.onclick = () => requestApi();

  // CSSで非表示にしていたものを表示
  dialog.style.display = "block";
}

/**
 * APIリクエスト関数
 */
async function requestApi() {
  const dialog_title = getElemText("dialog-title");
  const dialog_text = getElem("dialog-text").value;
  const status = getElem(STR_STATUS).value;

  let url = URL_BOARD_UPDATE_SERVER;
  if (isLocal()) {
    url = URL_BOARD_UPDATE_LOCAL;
  }

  const requestBody = { title: dialog_title, text: dialog_text, status: status };

  try {
    const data = await getFetchApiData(url, requestBody);
    if (data) {
      const msg = data[STR_MESSAGE];
      console.log(msg);
      alert(MSG_OK_SEND_EN);
    } else {
      closeDialog();
      throw new Error(MSG_ERR_SEND_EN);
    }

    // ページ全体をリセット（再読み込み）
    location.reload();
  } catch (error) {
    console.error('エラー:', error);
    alert(error);
  }
}

/**
 * ダイアログを非表示にする関数
 */
function closeDialog() {
  const dialog = getElem("dialog");
  dialog.style.display = ATTR_NONE;
  dialog.remove();
}
