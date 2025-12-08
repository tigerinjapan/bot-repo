/**
 * メッセージ表示
 * 
 * @param {string} msg - メッセージ内容
 * @param {boolean} answerFlg - true : 処理OK、false : 処理NG
 */
function showMessage(msg, answerFlg = false) {
  const elem = getElem(STR_MESSAGE);
  elem.innerHTML = msg;

  let color = COLOR_RED;
  if (answerFlg) {
    color = COLOR_GREEN;
  }

  const style = `color:${color};`;
  elem.style = style;
}

/**
 * 要素取得
 * 
 * @param {string} elemId - 要素id
 * @return {HTMLElement} HTML要素
 */
function getElem(elemId) {
  const elem = document.getElementById(elemId);
  return elem;
}

/**
 * 要素よりテキスト取得
 * 
 * @param {string} elemId - 要素id
 * @return {string} テキスト
 */
function getElemText(elemId) {
  const elem = getElem(elemId);
  return elem.textContent;
}

/**
 * 要素取得 (タグ)
 * 
 * @param {string} tagName - タグ名
 * @return {HTMLElement} HTML要素
 */
function getElemByTag(tagName) {
  const elem = document.getElementsByTagName(tagName)[0];
  return elem;
}

/**
 * 要素設定
 * 
 * @param {string} elemId - 要素id
 * @param {string} contents - コンテンツ
 * @param {boolean} textFlg - true : テキスト、false : HTMLの中身
 * @param {boolean} tagFlg - true : タグ、false : id
 * @return {HTMLElement} HTML要素
 */
function setElem(elemId, contents, textFlg, tagFlg = false) {
  let elem = getElem(elemId);
  if (tagFlg) {
    elem = getElemByTag(elemId);
  }

  if (textFlg) {
    elem.textContent = contents;
  } else {
    elem.innerHTML = contents;
  }
  return elem;
}

/**
 * 要素のテキスト設定
 * 
 * @param {string} elemId - 要素id
 * @param {string} text - テキスト
 */
function setElemText(elemId, text) {
  setElem(elemId, text, true);
}

/**
 * 要素のHTML設定
 * 
 * @param {string} elemId - 要素id
 * @param {string} innerHTML - HTMLの中身
 */
function setElemContents(elemId, innerHTML) {
  setElem(elemId, innerHTML, false);
}

/**
 * 要素のテキスト設定 (タグ)
 * 
 * @param {string} tagName - タグ名
 * @param {string} text - テキスト
 */
function setElemTextByTag(tagName, text) {
  setElem(tagName, text, true, true);
}

/**
* 要素のHTML設定 (タグ)
* 
* @param {string} tagName - タグ名
* @param {string} innerHTML - HTMLの中身
*/
function setElemContentsByTag(tagName, innerHTML) {
  setElem(tagName, innerHTML, false, true);
}

/**
 * 要素生成
 * 
 * @param {string} tagName - タグ名
 * @return {HTMLElement} HTML要素
 */
function createElemOnly(tagName) {
  const elem = createElem(tagName, null, null);
  return elem;
}

/**
 * 要素生成
 * 
 * @param {string} tagName - タグ名
 * @param {string} parentElemId - 親要素id
 * @return {HTMLElement} HTML要素
 */
function createElemNoVal(tagName, parentElemId) {
  const elem = createElem(tagName, null, parentElemId);
  return elem;
}

/**
 * 要素生成
 * 
 * @param {string} tagName - タグ名
 * @param {string} elemVal - 要素値
 * @param {string} parentElemId - 親要素id
 * @return {HTMLElement} HTML要素
 */
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

/**
 * オプション要素生成
 * 
 * @param {string} elemId - 要素id
 * @param {string} elemName - 要素名
 * @param {string[]} txtList - 要素テキストリスト
 * @param {string} parentElemId - 親要素id
 * @param {number} selectValIdx - 初期値インデックス
 */
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

/**
 * セレクトボックスのオプション生成
 * 
 * @param {string} selectElem - セレクト要素
 * @param {string[]} optValList - 要素値リスト
 * @param {string[]} textValList - 要素テキストリスト
 */
function createOptionVal(selectElem, optValList, textValList) {
  selectElem.innerHTML = SYM_BLANK;

  for (let i = 0; i < optValList.length; i++) {
    const option = createElemOnly(TAG_OPTION);
    option.value = optValList[i];
    option.textContent = textValList[i];
    selectElem.appendChild(option);
  }
};

/**
 * [fetch API] データを非同期で取得
 *
 * @param {string} url - APIのURL
 * @param {object} [requestBody] - 送信するデータ (省略可能)
 * @returns {Promise<object>} JSONデータ
 */
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

/**
 * JSONデータリスト取得
 *
 * @param {string} elemId - 要素id
 * @returns {Promise<object>} JSONデータ
 */
function getDataList(elemId) {
  // 1. HTML要素 (IDが'data'のpタグ)を取得
  const dataElem = getElem(elemId);

  // 2. その要素の中身 (文字列)を取得
  const dataString = dataElem.textContent.trim();

  // 3. 文字列をJavaScriptのリスト (配列)に変換
  //    Pythonのリスト形式の文字列を、JavaScriptのJSON形式として解釈する。
  //    これにより、文字列がリストになる。

  let dataList = [];
  try {
    // ※ Jinjaで渡されるリストの形式 (二重引用符か単一引用符かなど)によっては、
    //    この処理の前に、文字列の調整が必要になる場合がある。
    dataList = JSON.parse(dataString.replace(/'/g, '"'));
  } catch (e) {
    console.error("リストの形式が正しくありません:", e);
    // エラーが起きた場合は空のリストにするか、別の処理をします
    dataList = [];
  }
  return dataList;
}

/**
 * 待機
 *
 * @param {number} sec - 秒
 * @returns {Promise<object>} タイムアウトオブジェクト
 */
function sleep(sec) {
  // 待つ時間 (ms:ミリ秒)が終わったら、処理を進める
  const ms = sec * 1000;
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * ローカル環境判定
 *
 * @return {boolean} true : ローカル, false : ローカルではない
 */
function isLocal() {
  let localFlg = false;
  const hostname = window.location.hostname;
  if (hostname === "localhost" || hostname === "127.0.0.1") {
    localFlg = true;
  }
  return localFlg;
};
