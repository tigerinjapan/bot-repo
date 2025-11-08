// メッセージ表示
function showMessage(msg, answerFlg) {
  const elem = getElem(STR_MESSAGE);
  elem.innerHTML = msg;

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

// 要素のテキスト取得
function getElemText(elemId) {
  const elem = getElem(elemId);
  return elem.textContent;
}

// 要素取得（タグ）
function getElemByTag(tagName) {
  const elem = document.getElementsByTagName(tagName)[0];
  return elem;
}

// 要素設定
function setElem(elemId, text, tagFlg, textFlg) {
  let elem = getElem(elemId);
  if (tagFlg) {
    elem = getElemByTag(elemId);
  }

  if (textFlg) {
    elem.textContent = text;
  } else {
    elem.innerHTML = text;
  }
  return elem;
}

// 要素のテキスト設定
function setElemText(elemId, text) {
  setElem(elemId, text, false, true);
}

// 要素のHTML設定
function setElemContents(elemId, contents) {
  setElem(elemId, contents, false, false);
}

// 要素のテキスト設定（タグ）
function setElemTextByTag(elemId, text) {
  setElem(elemId, text, true, true);
}

// 要素のHTML設定（タグ）
function setElemContentsByTag(elemId, contents) {
  setElem(elemId, contents, true, false);
}

// 要素生成
function createElemOnly(tagName) {
  const elem = createElem(tagName, null, null);
  return elem;
}

// 要素生成
function createElemNoVal(tagName, parentElemId) {
  const elem = createElem(tagName, null, parentElemId);
  return elem;
}

// 要素生成
function createElem(tagName, elemVal, parentElemId) {
  const elem = document.createElement(tagName);

  if (elemVal) {
    if (tagName === TAG_LABEL || tagName === TAG_H1 || tagName === TAG_TH) {
      elem.textContent = elemVal;
    } else if (parentElemId === "gameRule") {
      elem.textContent = elemVal;
    } else {
      elem.id = elemVal;
      elem.className = elemVal;
      if (tagName === TAG_TEXTAREA) {
        elem.maxLength = 40;
        elem.placeholder = "Input the contents.";
      }
    }
  }

  if (parentElemId) {
    const parentElem = getElem(parentElemId);
    parentElem.appendChild(elem);
  }
  return elem;
}

// オプション生成
function createOption(elemId, elemName, txtList, parentElemId, selectValIdx) {
  const selectElem = createElemOnly(TAG_SELECT);
  selectElem.id = elemId;
  selectElem.name = elemName;

  for (let i = 0; i < txtList.length; i++) {
    const option = createElemOnly(TAG_OPTION);
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

// セレクトボックスのオプション生成
function createOptionVal(selectElem, optValList, textValList) {
  selectElem.innerHTML = SYM_BLANK;

  for (let i = 0; i < optValList.length; i++) {
    const option = createElemOnly(TAG_OPTION);
    option.value = optValList[i];
    option.textContent = textValList[i];
    selectElem.appendChild(option);
  }
};

// fetch API関数
async function getFetchApiData(url, requestBody) {
  let method = METHOD_GET;

  // requestBodyが存在する場合
  if (requestBody) {
    method = METHOD_POST;
  }

  let apiHeader = {
    method: method,
    headers: {
      "Content-Type": "application/json"
    },
  };

  if (method === METHOD_POST) {
    // POSTの場合、リクエストボディをJSON文字列化して 'body' プロパティに追加
    apiHeader.body = JSON.stringify(requestBody);
  }

  try {
    return await fetch(url, apiHeader)
      .then(response => {
        // ネットワークエラーなどをチェック
        if (!response.ok) {
          const errMsg = `HTTP error! status: ${response.status}${SYM_NEW_LINE}${response.statusText}`;
          throw new Error(errMsg);
        };
        return response.json();
      }).then(data => {
        return data;
      });

  } catch (error) {
    // エラー処理
    console.error('エラー:', error);
    alert(MSG_ERR_LOAD_JSON_EN);
  }
}

// JSONデータリスト取得
function getDataList(elemId) {
  // 1. HTML要素（IDが'data'のpタグ）を取得
  const dataElem = getElem(elemId);

  // 2. その要素の中身（文字列）を取得
  const dataString = dataElem.textContent.trim();

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

// ms（ミリ秒）だけ待つ関数
function sleep(sec) {
  // 待つ時間が終わったら、処理を進める約束（Promise）を作る
  const ms = sec * 1000;
  return new Promise(resolve => setTimeout(resolve, ms));
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
