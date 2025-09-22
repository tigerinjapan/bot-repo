// 文字列
const STR_REVIEW = "Review";

// 掲示板数
const NUM_BOARD_CNT = 5;

// 要素ID
const ELEM_ID_DIV = TAG_DIV + STR_REVIEW;
const ELEM_ID_FORM = TAG_FORM + STR_REVIEW;
const ELEM_ID_TABLE = TAG_TABLE + STR_REVIEW;
const ELEM_ID_TEXTAREA = TAG_TEXTAREA + STR_REVIEW;
const ELEM_NAME_ITEMS = "items[]";

// ページ読み込み時にsessionStorageからデータを取得
let userName = sessionStorage.getItem(STR_USER_NAME);

// ヘッダー設定
getElemByTag(TAG_HEAD).innerHTML = CONTENTS_HEAD_2;

// DOM読み込み後の初期化処理
document.addEventListener("DOMContentLoaded", () => {
  // タイトル設定
  document.title = STR_REVIEW;

  function init() {

    getElemByTag(TAG_H1).textContent = "アプリ・レビュー";

    const thList = ["No.", "アプリ", "カテゴリー", "区分", "内容"];
    const appTxtList = ["Line Message", "Travel & Life", "Number Plate", "その他"];
    const ctgTxtList = ["レビュー", "メモ", "エラー", "その他"];
    const typeTxtList = ["機能追加", "機能修正", "レイアウト", "その他"];

    parentElemId = ELEM_ID_TABLE;
    for (let i = 0; i <= NUM_BOARD_CNT; i++) {
      const strIdx = i.toString();

      const trId = TAG_TR + strIdx;
      createElem(TAG_TR, trId, parentElemId);

      for (let j = 0; j < thList.length; j++) {
        const strIdx2 = j.toString();

        if (i === 0) {
          createElem(TAG_TH, thList[j], trId);
        } else {
          const idx = strIdx + strIdx2;
          const tdId2 = TAG_TD + idx;
          createElem(TAG_TD, tdId2, trId);

          if (j === 0) {
            getElem(tdId2).textContent = i;
          } else if (j === 1) {
            createOption(STR_APP + strIdx, STR_APP, appTxtList, tdId2, 0);
          } else if (j === 2) {
            createOption(STR_CATEGORY + strIdx, STR_CATEGORY, ctgTxtList, tdId2, 0);
          } else if (j === 3) {
            createOption(STR_TYPE + strIdx, STR_TYPE, typeTxtList, tdId2, 0);
          } else {
            createElem(TAG_TEXTAREA, ELEM_ID_TEXTAREA + strIdx, tdId2);
          }
        }
      }
    }

    getElemByTag(TAG_BUTTON).textContent = "送信";
  }

  // 初期表示
  init();
});

// ユーザ名設定
function setUserName() {
  if (!userName || userName === SYM_BLANK) {
    userName = prompt(MSG_INFO_INPUT_USER);
    sessionStorage.setItem(STR_USER_NAME, userName);
  }
}

// レビュー送信
function sendReview() {
  const form = getElem(ELEM_ID_FORM);
  if (!form) return;

  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    let reviewList = [];
    let addCnt = 0;
    for (let i = 1; i <= NUM_BOARD_CNT; i++) {
      const idx = i.toString();
      const app = getElem(STR_APP + idx).value;
      const category = getElem(STR_CATEGORY + idx).value;
      const type = getElem(STR_TYPE + idx).value;
      const contents = getElem(ELEM_ID_TEXTAREA + idx).value;
      if (contents) {
        const reviewData = [app, category, type, contents, userName];
        reviewList.push(reviewData);
        addCnt++;
      }
    }

    // 入力チェック
    if (addCnt === 0) {
      getElem(STR_MESSAGE).textContent = MSG_ERR_NO_INPUT;
      return;
    }

    // MongoDB保存API呼び出し
    try {

      let url = URL_BOARD_ADD;
      if (isLocal()) {
        url = URL_BOARD_LOCAL;
      }

      setUserName();

      const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          data: reviewList
        }),
      });
      const result = await res.json();
      const msg = result[STR_MESSAGE];

      // getElem(STR_MESSAGE).textContent = msg;
      // getElem(ELEM_ID_FORM).reset();
      console.log(msg);
      alert(msg);

      // ページ全体をリセット（再読み込み）
      location.reload();
    } catch {
      setElem(STR_MESSAGE, MSG_ERR_SEND, true);
    }
  });
}
