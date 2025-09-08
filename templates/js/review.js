// 文字列
const STR_REVIEW = "Review";

// 要素ID
const ELEM_ID_DIV = TAG_DIV + STR_REVIEW;
const ELEM_ID_FORM = TAG_FORM + STR_REVIEW;
const ELEM_ID_TABLE = TAG_TABLE + STR_REVIEW;
const ELEM_ID_TEXTAREA = TAG_TEXTAREA + STR_REVIEW;
const ELEM_NAME_ITEMS = "items[]";

document.getElementsByTagName(TAG_HEAD)[0].innerHTML = CONTENTS_HEAD;
document.title = STR_REVIEW;

// DOM読み込み後の初期化処理
document.addEventListener("DOMContentLoaded", () => {
  function init() {

    document.getElementsByTagName(TAG_H1)[0].textContent = "設計書レビュー";

    let selectList = [
      [
        "対象プロジェクト",
        STR_PROJECT,
        ["line", "trip", "number"],
        ["Line Message", "Trip & Life", "Number Plate"],
        1
      ],
      [
        "対象設計書",
        STR_DESIGN,
        ["detail", "api", "db"],
        ["詳細", "API", "DB"],
        0
      ],
    ];

    let parentElemId = ELEM_ID_DIV;
    for (const [lblTxt, elemId, valList, txtList, selectValIdx] of selectList) {
      createElem(TAG_LABEL, lblTxt, parentElemId);
      createOption(elemId, elemId, valList, txtList, parentElemId, selectValIdx);
    }

    const thList = ["No.", "区分", "レビュー内容"]
    const categoryValList = ["add", "modify", "layout", "etc"];
    const categoryTxtList = ["機能追加", "機能修正", "レイアウト", "その他"];

    parentElemId = ELEM_ID_TABLE;
    for (let i = 0; i <= 5; i++) {
      const strIdx = i.toString();

      const trId = TAG_TR + strIdx;
      createElem(TAG_TR, trId, parentElemId);

      for (let j = 0; j < thList.length; j++) {
        const strIdx2 = j.toString();

        if (i == 0) {
          createElem(TAG_TH, thList[j], trId);
        } else {
          const idx = strIdx + strIdx2;
          const tdId2 = TAG_TD + idx;
          createElem(TAG_TD, tdId2, trId);

          if (j == 0) {
            getElem(tdId2).textContent = i;
          } else if (j == 1) {
            createOption(STR_CATEGORY + strIdx, STR_CATEGORY, categoryValList, categoryTxtList, tdId2, 0);
          } else {
            createElem(TAG_TEXTAREA, ELEM_ID_TEXTAREA + strIdx, tdId2);
          }
        }
      }
    }

    document.getElementsByTagName(TAG_BUTTON)[0].textContent = "送信";
  }

  // 初期表示
  init();
});

// レビュー送信
function sendReview() {
  const form = getElem(ELEM_ID_FORM);
  if (!form) return;

  form.addEventListener("submit", async function (e) {
    e.preventDefault();
    const project = getElem(STR_PROJECT).value;
    const design = getElem(STR_DESIGN).value;

    let reviewList = [];
    let addCnt = 0;
    for (let i = 1; i <= 5; i++) {
      const idx = i.toString();
      const category = getElem(STR_CATEGORY + idx).value;
      const textareaReview = getElem(ELEM_ID_TEXTAREA + idx).value;
      if (textareaReview) {
        const reviewData = [project, design, category, textareaReview];
        reviewList.push(reviewData);
        addCnt++;
      }
    }

    // 入力チェック
    if (addCnt == 0) {
      getElem(STR_MSG).textContent = MSG_ERR_NO_INPUT;
      return;
    }

    // MongoDB保存API呼び出し
    try {

      let url = URL_REVIEW_ADD;
      if (isLocal()) {
        url = URL_REVIEW_LOCAL;
      }

      const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          data: reviewList
        }),
      });
      const result = await res.json();
      const message = result["message"];
      console.log(message);
      getElem(STR_MSG).textContent = message;
    } catch {
      getElem(STR_MSG).textContent = MSG_ERR_SEND;
    }
  });
}

// 要素取得
function getElem(elemId) {
  const elem = document.getElementById(elemId);
  return elem;
}

// 要素生成
function createElem(tagName, elemVal, parentElemId) {
  const elem = document.createElement(tagName);

  if (tagName == TAG_LABEL || tagName == TAG_H1 || tagName == TAG_TH) {
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
function createOption(elemId, elemName, valList, txtList, parentElemId, selectValIdx) {
  const selectElem = document.createElement(TAG_SELECT);
  selectElem.id = elemId;
  selectElem.name = elemName;

  for (let i = 0; i < valList.length; i++) {
    const option = document.createElement(TAG_OPTION);
    option.value = valList[i];
    option.textContent = txtList[i];
    selectElem.appendChild(option);
  }

  if (0 <= selectValIdx && selectValIdx < valList.length) {
    selectElem.value = valList[selectValIdx];
  }

  const parentElem = getElem(parentElemId);
  parentElem.appendChild(selectElem);
}