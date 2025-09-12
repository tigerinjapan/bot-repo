// メッセージ表示
function showMessage(msg, answerFlg) {
  const elem = setElem('message', msg, false);
  let color = COLOR_RED;
  if (answerFlg) {
    color = COLOR_GREEN;
  }

  const style = 'color:' + color + ';';
  elem.style = style;
}

// 要素取得
function getElem(elemId) {
  const elem = document.getElementById(elemId);
  return elem;
}

// 要素設定
function setElem(elemId, text, textFlg) {
  const elem = getElem(elemId);
  if (textFlg) {
    elem.textContent = text;
  } else {
    elem.innerHTML = text;
  }
}

// 要素生成
function createElem(tagName, elemVal, parentElemId) {
  const elem = document.createElement(tagName);

  if (tagName == TAG_LABEL || tagName == TAG_H1 || tagName == TAG_TH) {
    elem.textContent = elemVal;
  } else if (parentElemId == "gameRule") {
    elem.textContent = elemVal;
  } else {
    elem.id = elemVal;
    if (tagName == TAG_TEXTAREA) {
      elem.maxLength = 40;
      elem.placeholder = "レビュー内容を記載してください";
    }
  }

  if (parentElemId) {
    const parentElem = getElem(parentElemId);
    parentElem.appendChild(elem);
  }
}

// オプション生成
function createOption(elemId, elemName, txtList, parentElemId, selectValIdx) {
  const selectElem = document.createElement(TAG_SELECT);
  selectElem.id = elemId;
  selectElem.name = elemName;

  for (let i = 0; i < txtList.length; i++) {
    const option = document.createElement(TAG_OPTION);
    option.value = i;
    option.textContent = txtList[i];
    selectElem.appendChild(option);
  }

  if (0 <= selectValIdx && selectValIdx < txtList.length) {
    selectElem.value = selectValIdx;
  }

  const parentElem = getElem(parentElemId);
  parentElem.appendChild(selectElem);
}

// ローカル環境判定
function isLocal() {
  let localFlg = false;
  if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
    localFlg = true;
  }
  return localFlg;
};
