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

// 要素のテキスト設定
function setElemText(elemId, text) {
  setElem(elemId, text, true);
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

function getDataList(elemId) {
  // 1. HTML要素（IDが'data'のpタグ）を取得
  const dataElement = getElem(elemId);

  // 2. その要素の中身（文字列）を取得
  const dataString = dataElement.textContent.trim();

  // 3. 文字列をJavaScriptのリスト（配列）に変換
  //    Pythonのリスト形式の文字列を、JavaScriptのJSON形式として解釈する。
  //    これにより、文字列がリストになる。

  let dataList = [];
  try {
      // ※ Jinjaで渡されるリストの形式（二重引用符か単一引用符かなど）によっては、
      //    この処理の前に、文字列の調整が必要になる場合がある。
      dataList = JSON.parse(dataString.replace(/'/g, '"'));
  } catch (e) {
      console.error("リストの形式が正しくありません:", e);
      // エラーが起きた場合は空のリストにするか、別の処理をします
      dataList = [];
  }
  return dataList;
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
