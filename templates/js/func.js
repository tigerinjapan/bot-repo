// メッセージ表示
function showMessage(msg, answerFlg) {
  const elem = setElem(STR_MESSAGE, msg, false);
  let color = COLOR_RED;
  if (answerFlg) {
    color = COLOR_GREEN;
  }

  const style = `color:${color};`;
  elem.style = style;
}

// 要素取得
function getElem(elemId) {
  const elem = document.getElementById(elemId);
  return elem;
}

// 要素取得
function getElemByTag(tagName) {
  const elem = document.getElementsByTagName(tagName)[0];
  return elem;
}

// 要素のテキスト取得
function getElemText(elemId) {
  const elem = getElem(elemId);
  return elem.textContent;
}

// 要素設定
function setElem(elemId, text, textFlg) {
  const elem = getElem(elemId);
  if (textFlg) {
    elem.textContent = text;
  } else {
    elem.innerHTML = text;
  }
  return elem;
}

// 要素生成
function createElem(tagName, elemVal, parentElemId) {
  const elem = document.createElement(tagName);

  if (tagName === TAG_LABEL || tagName === TAG_H1 || tagName === TAG_TH) {
    elem.textContent = elemVal;
  } else if (parentElemId === "gameRule") {
    elem.textContent = elemVal;
  } else {
    elem.id = elemVal;
    if (tagName === TAG_TEXTAREA) {
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

// fetch APIを使ってファイルを読み込む関数
async function getFetchApiData(url) {
  const api_header = {
    method: "GET",
    headers: {
      "Content-Type": "application/json"
    },
  };

  try {
    return await fetch(url, api_header)
      .then(response => {
        // ネットワークエラーなどをチェック
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        };
        return response.json();
      }).then(data => {
        return data;
      });

  } catch (error) {
    // エラー処理
    console.error('Failed to load json file:', error);
    alert(MSG_ERR_LOAD_JSON);
  }
}

// ローカル環境判定
function isLocal() {
  let localFlg = false;
  const hostname = window.location.hostname;
  if (hostname === "localhost" || hostname === "127.0.0.1") {
    localFlg = true;
  }
  return localFlg;
};
