// ヘッダー設定
setElemContentsByTag(TAG_HEAD, CONTENTS_HEAD_1);

// タイトル設定
document.title = TITLE_NUMBER;

// ページ読み込み時にsessionStorageからデータを取得
let userName = sessionStorage.getItem(STR_USER_NAME);

// 制限時間
let limitTime = 20.00;

// タイマーID
let timerId = null;

// タイマー状態管理
let isTimerRunning = false;

// 強制停止
let stopFlg = false;

// DOM読み込み後の処理
document.addEventListener("DOMContentLoaded", () => {
  // 初期表示
  init();

  // STARTボタン設定
  setStartBtn();

  // 言語コード
  const langCd = getElemText("langCd");

  // ゲームルール表示
  const ruleBtn = getElem("btnRule");
  if (ruleBtn) {
    ruleBtn.addEventListener("click", () => {
      showDialog(langCd);
    });
  }

  // 回答確認
  const chkBtn = getElem("btnChk");
  if (chkBtn) {
    chkBtn.addEventListener("click", () => {
      checkAnswer(langCd);
    });
  }
});

// 初期表示
function init() {
  // ゲームデータ設定
  setGameData();

  // レベル
  const level = getElemText("levelVal");

  // 言語コード
  const langCd = getElemText("langCd");

  let title = TITLE_NUMBER;

  const number = getElem("number-display");
  number.style.backgroundColor = "cyan";

  // --- exprArea を必ず用意（存在しない場合は DOM に生成して挿入） ---
  let exprArea = getElem("exprArea");
  if (!exprArea) {
    exprArea = document.createElement("div");
    exprArea.id = "exprArea";
    exprArea.className = "expr-area";
    if (number && number.parentNode) number.parentNode.insertBefore(exprArea, number.nextSibling);
    else document.body.appendChild(exprArea);
  }
  // 内部保持用プロパティ初期化（expression id に依存しない）
  exprArea.dataset.expr = exprArea.dataset.expr || "";
  exprArea._tokens = exprArea._tokens || [];
  // 初期は非表示にしておく（START 押下で表示）
  exprArea.style.opacity = "0";
  exprArea.style.pointerEvents = "none";
  exprArea.style.transition = "opacity 0.15s ease";

  // Number 表示をボタン化して初期描画
  const num = getElemText("number-display");
  renderInputButtons(num);

  let btnRuleNm = "GAME RULE";
  let btnChkNm = "CHECK";
  let btnNextNm = "NEXT";

  if (langCd === LANG_CD_KO) {
    title = TITLE_NUMBER_KO;
    btnRuleNm = "게임규칙";
    btnChkNm = "정답확인";
    btnNextNm = "다음문제";

    const footerElem = getElemByTag(TAG_FOOTER);
    footerElem.style.visibility = 'hidden';
  }

  setElemText("title", title);
  setElemText("btnRule", btnRuleNm);
  setElemText("btnChk", btnChkNm);
  setElemText("btnNext", btnNextNm);
}

// ゲームデータ設定
function setGameData() {
  setElemText("timer", limitTime.toFixed(2));

  const dataList = getElemText("dataList");

  // JSON形式の文字列に変換する
  const rankingDataJson = JSON.parse(dataList);

  const idx = Math.floor(Math.random() * rankingDataJson.length);
  const gameData = rankingDataJson[idx];

  const number = gameData.number;
  const answer = gameData.answer;
  const level = gameData.level;
  const rankUser = gameData.userName;
  const rankTime = gameData.rankTime.toFixed(2);

  setElemText("number-display", number);
  setElemText("number-answer", answer);
  setElemText("rank-user", rankUser);
  setElemText("rank-time", rankTime);
  setLevel(level);
}

// レベル設定
function setLevel(level) {
  let levelMark = SYM_LEVEL;
  if (level === LEVEL_MEDIUM) {
    levelMark = SYM_LEVEL.repeat(2);
  } else if (level === LEVEL_HARD) {
    levelMark = SYM_LEVEL.repeat(3);
  }
  setElemText("level", `Level ${levelMark}`);
  setElemText("levelVal", level);
}

// STARTボタン設定
function setStartBtn() {
  // START/STOP処理
  const startBtn = getElem("btnStart");
  if (startBtn) {
    startBtn.textContent = "START";
    startBtn.addEventListener("click", () => {
      const number = getElem("number-display");
      number.style.backgroundColor = "black";

      // START/STOP トグル（表示は opacity で制御）
      let exprArea = getElem("exprArea");
      if (!isTimerRunning) {
        // START: 表示してタイマー開始（操作可能に）
        if (exprArea) {
          exprArea.style.opacity = "1";
          exprArea.style.pointerEvents = "auto";
        }
        setTimer();
        startBtn.textContent = "STOP";
        isTimerRunning = true;
      } else {
        // STOP: 停止、タイマーリセット、非表示にして新番号取得
        setStop();
      }
    });
  }
}

// 停止処理
function setStop() {
  clearInterval(timerId);
  isTimerRunning = false;

  setElemText("timer", "STOPPED");
  setElemText("btnStart", "START");

  let exprArea = getElem("exprArea");
  if (exprArea) {
    exprArea.style.opacity = "0";
    exprArea.style.pointerEvents = "none";
  }
  init();
}

// タイマー設定
function setTimer() {
  let sec = limitTime;
  const timerElem = getElem("timer");
  timerElem.textContent = sec.toFixed(2);

  timerId = setInterval(() => {
    sec -= 0.01;
    timerElem.textContent = sec.toFixed(2);
    if (sec <= 0) {
      clearInterval(timerId);
      timerElem.textContent = "TIME OUT !!";
    }
    if (sec <= 10) {
      timerElem.classList.add(COLOR_RED);
    } else {
      timerElem.classList.remove(COLOR_RED);
    }
  }, 10);
}

// ユーザ名設定
function setUserName(inputMsg) {
  if (!userName || userName === SYM_BLANK) {
    userName = prompt(inputMsg);
    sessionStorage.setItem(STR_USER_NAME, userName);
  }
}

// ゲームルール生成
function setGameRule(langCd) {
  let ruleList = LIST_GAME_RULE;
  if (langCd === LANG_CD_KO) {
    ruleList = LIST_GAME_RULE_KO;
  }

  for (let i = 0; i < ruleList.length; i++) {
    createElem(TAG_LI, ruleList[i], "gameRule");
  }
}

// ダイアログ表示用関数
function showDialog(langCd) {
  dialog = createElemOnly(TAG_DIV);
  dialog.id = "gameRuleDialog";
  dialog.innerHTML = `
    <h3>Game Rule</h3>
    <ul id="gameRule"></ul><br><br>
    <button type="button" id="closeGameRuleDialog">Close</button>
  `;
  document.body.appendChild(dialog);

  setGameRule(langCd);

  getElem("closeGameRuleDialog").onclick = () => {
    dialog.remove();
  };
}

// 正解判定
function checkAnswer(langCd) {
  let okAnswerMsg = MSG_OK_ANSWER;
  let noAnswerMsg = MSG_ERR_NO_ANSWER;

  if (langCd === LANG_CD_KO) {
    okAnswerMsg = MSG_OK_ANSWER_KO;
    noAnswerMsg = MSG_ERR_NO_ANSWER_KO;
  }

  // DOM取得
  const num = getElemText("number-display");
  const ans = getElemText("number-answer");
  const rankTime = getElemText("rank-time");
  const timeVal = getElemText("timer");

  // exprArea の内部トークンから現在の式文字列を組み立てる（expression id に依存しない）
  const exprArea = getElem("exprArea");
  let expr = "";
  if (exprArea && Array.isArray(exprArea._tokens)) {
    expr = exprArea._tokens.map(tok => (tok.type === "num" ? tok.val : (tok.val ? tok.val : ""))).join("").trim();
  }

  // 入力チェック
  let chkMsg = validate(num, ans, expr, langCd);
  if (chkMsg) {
    showMessage(chkMsg, false);
  } else {
    if (ans) {
      let ansList = ans;
      if (typeof ans === "string") {
        ansList = ans.split(";").filter(s => s.trim());
      }
      const ansHtml = "<ul>" + ansList.map(a => `<li>${a}</li>`).join(SYM_BLANK) + "</ul>";
      showMessage(okAnswerMsg + ansHtml, true);

      const clearTime = limitTime - parseFloat(timeVal);
      const clearTimeVal = clearTime.toFixed(2);
      const rankTimeVal = parseFloat(rankTime);
      const level = getElemText("levelVal");
      if (clearTime != null && clearTimeVal < rankTimeVal && level == LEVEL_HARD) {
        const numVal = parseInt(num);
        // ランキング送信
        sendRanking(numVal, clearTimeVal, langCd);
      }
      clearInterval(timerId);
    } else {
      showMessage(noAnswerMsg, false);
    }
  }
};

/**
 * 現在のトークン配列をレンダリング。
 * トークンは [num, slot, num, slot, num, slot, num] の形を想定。
 */
function renderInputButtons(numberStr) {
  const exprArea = getElem("exprArea");
  if (!exprArea) return;
  exprArea.innerHTML = "";

  // tokens 初期化（num と slot）
  const digits = String(numberStr).split("");
  const tokens = [];
  for (let i = 0; i < digits.length; i++) {
    tokens.push({ type: "num", val: digits[i] });
    if (i < digits.length - 1) tokens.push({ type: "slot", val: null });
  }
  exprArea._tokens = tokens;

  // 再描画
  function refresh() {
    exprArea.innerHTML = "";
    const t = exprArea._tokens;
    for (let i = 0; i < t.length; i++) {
      const token = t[i];
      if (token.type === "num") {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "digit-btn";
        btn.textContent = token.val;
        btn.dataset.idx = i;
        btn.addEventListener("click", onDigitClick);
        exprArea.appendChild(btn);
      } else { // slot
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "slot-btn";
        btn.textContent = token.val ? token.val : "▢";
        btn.dataset.idx = i;
        btn.addEventListener("click", onSlotClick);
        exprArea.appendChild(btn);
      }
    }
    updateHiddenExpression();
  }

  // 数字ボタン押下: 選択肢の表示（√ と 上付き / back 対応）
  function onDigitClick(e) {
    const idx = Number(e.currentTarget.dataset.idx);
    const token = exprArea._tokens[idx];
    const raw = stripDecor(token.val);

    // 状態判定
    const hasSqrt = String(token.val).startsWith("√");
    const hasSup = /[⁰¹²]$/.test(String(token.val));
    const hasHistory = token._history && 0 < token._history.length;

    // 判定: このトークンが「空箱削除で結合された2桁トークン」か
    const isMergedTwoDigit = /^\d{2}$/.test(raw) && token._history && token._history.some(h => h.type === "merge");

    // 左側に空箱があるか（トークン構造上、左隣が slot で val===null）
    const leftIdx = idx - 1;
    const leftIsEmptySlot = 0 <= leftIdx && exprArea._tokens[leftIdx] && exprArea._tokens[leftIdx].type === "slot" && exprArea._tokens[leftIdx].val == null;

    let choices = [];

    // 装飾や履歴がある場合は back を常に提示（他候補も追加可能にする）
    if (hasSqrt || hasSup || hasHistory) {
      choices.push("back");
    }

    // merge による2桁合成トークンでは、合成向け候補を追加
    if (isMergedTwoDigit) {
      // √（合成値に対して有効なら）
      if (isSqrtEligible(raw)) choices.push("√");
      // base+上付き（右桁が0/1/2のとき）
      const base = raw.charAt(0);
      const expo = raw.charAt(1);
      if (/[012]/.test(expo)) {
        const supMap = { "0": "⁰", "1": "¹", "2": "²" };
        choices.push(base + supMap[expo]);
      }
    }

    if (!hasSqrt && !hasSup && !hasHistory) {
      // 未装飾かつ左空箱では √ も提示できる
      if (isSqrtEligible(raw)) {
        choices.push("√");
      }
    }

    // 重複を削除し順序を整える
    choices = Array.from(new Set(choices));

    // 何も出すものがなければ何もしない
    if (choices.length === 0) return;

    const popup = createSmallPopup(choices, e.currentTarget);
    popup.querySelectorAll("button").forEach(b => {
      b.addEventListener("click", () => {
        const choice = b.dataset.choice;
        popup.remove();
        if (!choice) return;

        // back: 履歴があれば復元（merge の場合は split を復元）
        if (choice === "back") {
          if (token._history && 0 < token._history.length) {
            const last = token._history.pop();
            if (last.type === "modify") {
              token.val = last.prevVal;
              if (token._history.length === 0) delete token._history;
              refresh();
              return;
            } else if (last.type === "merge") {
              // split: leftPrev / rightPrev を復元（現在 token は leftPrev+rightPrev）
              token.val = last.leftPrev;
              exprArea._tokens.splice(idx + 1, 0, { type: "slot", val: null }, { type: "num", val: last.rightPrev });
              if (token._history && token._history.length === 0) delete token._history;
              refresh();
              return;
            }
          }
          // 履歴なしでも装飾を外す互換処理
          if (String(token.val).startsWith("√")) {
            exprArea._tokens[idx].val = stripDecor(token.val);
            refresh();
            return;
          }
          if (hasSup) {
            exprArea._tokens[idx].val = stripDecor(token.val);
            refresh();
            return;
          }
          return;
        }

        // √ 選択
        if (choice === "√") {
          if (isSqrtEligible(token.val)) {
            token._history = token._history || [];
            token._history.push({ type: "modify", prevVal: token.val });
            token.val = "√" + stripDecor(token.val);
            refresh();
          }
          return;
        }

        // 例: "2¹" のような base+上付き（merge 2桁向け）
        if (/^[1-9][⁰¹²]$/.test(choice)) {
          token._history = token._history || [];
          token._history.push({ type: "modify", prevVal: token.val });
          token.val = choice;
          refresh();
          return;
        }
      });
    });
  }

  // スロット押下: 演算子選択 or 削除
  function onSlotClick(e) {
    const idx = Number(e.currentTarget.dataset.idx);
    const token = exprArea._tokens[idx];
    // options: back は表示しない（slot が空のとき）
    const options = ["+", "-", "*", "/", "=", "delete"];
    if (token.val) options.push("back");
    const popup = createSmallPopup(options, e.currentTarget);
    popup.querySelectorAll("button").forEach(b => {
      b.addEventListener("click", () => {
        const choice = b.dataset.choice;
        popup.remove();
        if (choice === "delete") {
          // スロット削除 -> 左右の数を結合（文字列連結）
          const leftIdx = idx - 1;
          const rightIdx = idx + 1;
          if (0 <= leftIdx && rightIdx < exprArea._tokens.length &&
            exprArea._tokens[leftIdx].type === "num" &&
            exprArea._tokens[rightIdx].type === "num") {
            // 履歴を残してからマージ（back で復元可能にする）
            const leftTok = exprArea._tokens[leftIdx];
            const rightTok = exprArea._tokens[rightIdx];
            leftTok._history = leftTok._history || [];
            leftTok._history.push({ type: "merge", leftPrev: leftTok.val, rightPrev: rightTok.val });
            // 文字列結合（既存装飾は保持される形で単純連結）
            leftTok.val = String(leftTok.val) + String(rightTok.val);
            exprArea._tokens.splice(rightIdx, 1);
            exprArea._tokens.splice(idx, 1);
            refresh();
          }
          return;
        }
        if (choice === "back") {
          // slot の back は operator をクリアして空箱に戻す
          token.val = null;
          token.type = "slot";
          refresh();
          return;
        }

        // 通常の演算子設定
        token.type = "slot";
        token.val = choice;
        refresh();
      });
    });
  }

  /**
   * createSmallPopup(choices, anchorElem)
   * - choices 配列からボタンを生成してアンカー要素の下に表示する
   * - ウィンドウ端にかからないように簡易補正を行う
   * - クリック外で自動的に閉じる
   */
  function createSmallPopup(choices, anchorElem) {
    const popup = document.createElement("div");
    popup.className = "small-popup";

    // ボタンを生成して popup に追加（重要: append を忘れない）
    choices.forEach(ch => {
      const b = document.createElement("button");
      b.type = "button";
      b.textContent = ch;
      b.dataset.choice = ch;
      b.className = "popup-btn";
      popup.appendChild(b);
    });

    document.body.appendChild(popup);

    // 位置決め: アンカーの下に表示。左端・右端でのはみ出しは簡易補正
    const rect = anchorElem.getBoundingClientRect();
    const winW = window.innerWidth || document.documentElement.clientWidth;
    popup.style.position = "absolute";
    popup.style.top = (rect.bottom + window.scrollY + 8) + "px";
    // 左位置を安定させる（右端にはみ出す場合は調整）
    let left = rect.left + window.scrollX;
    // 最小マージン
    if (left < 6) left = 6;
    // 右端にはみ出すなら左を調整
    const popupEstWidth = Math.min(360, choices.length * 56 + 24);
    if (winW - 6 < left + popupEstWidth) {
      left = Math.max(6, winW - popupEstWidth - 6);
    }
    popup.style.left = left + "px";
    popup.style.zIndex = "3000";

    // クリック外で閉じる（1フレーム遅延してイベントを設置）
    setTimeout(() => {
      const onDoc = (ev) => {
        if (!popup.contains(ev.target) && ev.target !== anchorElem) {
          popup.remove();
          document.removeEventListener("click", onDoc);
        }
      };
      document.addEventListener("click", onDoc);
    }, 0);
    return popup;
  }

  // √の適用可否（要求仕様: 4..81 の完全平方数で sqrt が 2..9 の整数）
  function isSqrtEligible(valStr) {
    if (!/^\d+$/.test(valStr)) return false;
    const v = parseInt(valStr, 10);
    if (!(4 <= v && v < 100)) return false;
    const r = Math.floor(Math.sqrt(v));
    return r * r === v && (2 <= r && r <= 9);
  }

  // 表示用値から装飾(√/上付き)を外して生数字のみを返す
  function stripDecor(displayVal) {
    return String(displayVal).replace(/^√/, "").replace(/[⁰¹²]$/u, "");
  }

  /**
   * updateHiddenExpression
   * - exprArea 内のトークン配列から現在の式文字列を作成して
   *   exprArea.dataset.expr に保存します（内部保持、DOM input に依存しない）
   * - 保守性向上のため expression 要素参照は使わない
   */
  function updateHiddenExpression() {
    const ea = getElem("exprArea");
    if (!ea) return;
    const parts = (ea._tokens || []).map(tok => (tok.type === "num" ? tok.val : (tok.val ? tok.val : "")));
    ea.dataset.expr = parts.join("");
  }

  // 初回描画
  refresh();
}

// 入力チェック
function validate(num, ans, expr, langCd) {
  let chkMsg = SYM_BLANK;

  let noInputMsg = MSG_ERR_NO_INPUT;
  let errDegitMsg = MSG_ERR_DIGIT;
  let errEqualMsg = MSG_ERR_EQUAL;
  let errFormatMsg = MSG_ERR_FORMAT;
  let noDivideZeroMsg = MSG_ERR_DIVIDE_BY_ZERO;
  let errMatchMsg = MSG_ERR_MATCH;

  if (langCd === LANG_CD_KO) {
    noInputMsg = MSG_ERR_NO_INPUT_KO;
    errDegitMsg = MSG_ERR_DIGIT_KO;
    errEqualMsg = MSG_ERR_EQUAL_KO;
    errFormatMsg = MSG_ERR_FORMAT_KO;
    noDivideZeroMsg = MSG_ERR_DIVIDE_BY_ZERO_KO;
    errMatchMsg = MSG_ERR_MATCH_KO;
  }

  // 回答入力チェック
  if (expr === SYM_BLANK) {
    return noInputMsg;
  }

  // 表示上の上付き文字（⁰¹²）は数字 0/1/2 として扱うため正規化
  const exprNorm = String(expr).replace(/⁰/g, "0").replace(/¹/g, "1").replace(/²/g, "2");

  // 数字チェック（表示中の数字文字のみ抽出）
  const numDigits = String(num).replace(/\D/g, "");
  const exprDigitsArr = exprNorm.match(/\d/g) || [];
  const exprDigits = exprDigitsArr.join("");
  if (exprDigits !== numDigits) {
    return errDegitMsg;
  }

  // イコール1つのみ
  if ((expr.match(/=/g) || []).length !== 1) {
    return errEqualMsg;
  }

  const [left, right] = expr.split("=");

  try {
    // 入力フォーマットチェック（数字・演算子・√・上付き0-2のみ許可）
    // 許可する文字: 0-9, √, ⁰¹², + - * / . 空白
    const validRe = /^[\d√⁰¹²+\-*/.\s]+$/u;
    // validate は表示上のままの left/right をチェック（上付きを許容）
    if (!validRe.test(left) || !validRe.test(right)) {
      return errFormatMsg;
    }
  } catch (e) {
    return errFormatMsg;
  }

  // ゼロ除算チェック（上付きを数字に戻してチェック）
  if (exprNorm.includes("/0")) {
    return noDivideZeroMsg;
  }

  // 計算結果比較
  if (!ans.includes(expr)) {
    return errMatchMsg;
  }

  return chkMsg;
}

// ランキング送信
async function sendRanking(number, time, langCd) {
  let inputMsg = MSG_INPUT_USER;
  let rankOkMsg = MSG_OK_RANK;
  let rankNgMsg = MSG_ERR_RANK;

  if (langCd === LANG_CD_KO) {
    inputMsg = MSG_INPUT_USER_KO;
    rankOkMsg = MSG_OK_RANK_KO;
    rankNgMsg = MSG_ERR_RANK_KO;
  }

  setUserName(inputMsg);

  let url = URL_NUMBER_RANKING_SERVER;
  if (isLocal()) {
    url = URL_NUMBER_RANKING_LOCAL;
  }

  const requestBody = { number: number, user: userName, time: time, date: new Date() };

  try {
    const data = await getFetchApiData(url, requestBody);
    console.log(data.message);
    showMessage(rankOkMsg, true);

  } catch (error) {
    console.error('エラー:', error);
    alert(rankNgMsg);
  }
}
