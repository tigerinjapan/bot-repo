// メッセージ表示
function showMessage(msg, answerFlg) {
  setElem('message', msg, false, answerFlg);
}

// 要素設定
function setElem(elemId, text, textFlg, answerFlg) {
  const elem = document.getElementById(elemId);
  if (textFlg) {
    elem.textContent = text;
  } else {
    elem.innerHTML = text;
  }

  let color = COLOR_RED;
  if (answerFlg) {
    color = COLOR_GREEN;
  }

  const style = 'color:' + color + ';';
  elem.style = style;
}

// ローカル環境判定
function isLocal() {
  let localFlg = false;
  if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
    localFlg = true;
  }
  return localFlg;
};
