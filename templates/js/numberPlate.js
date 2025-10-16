// ページ読み込み時にsessionStorageからデータを取得
let userName = sessionStorage.getItem(STR_USER_NAME);

// 制限時間
let limitTime = 30.00;

// タイマーID
let timerId = null;

// タイマー状態管理
let isTimerRunning = false;

// ヘッダー設定
setElemContentsByTag(TAG_HEAD, CONTENTS_HEAD_1);

// DOM読み込み後の処理
document.addEventListener("DOMContentLoaded", () => {
  // 初期表示
  init();

  // 言語コード
  const langCd = getElemText("langCd");

  // START/STOP処理
  const startBtn = getElem("btnStart");
  if (startBtn) {
    startBtn.textContent = "START";
    startBtn.addEventListener("click", () => {
      const number = getElem("number-display");
      number.style.backgroundColor = "black";

      if (!isTimerRunning) {
        setTimer();
        startBtn.textContent = "STOP";
        isTimerRunning = true;
      } else {
        clearInterval(timerId);
        setElemText("timer", "STOPPED");
        startBtn.textContent = "START";
        isTimerRunning = false;
      }
    });
  }

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
  // レベル
  const level = getElemText("levelVal");

  // 言語コード
  const langCd = getElemText("langCd");

  let title = TITLE_NUMBER_PLATE;

  const number = getElem("number-display");
  number.style.backgroundColor = "cyan";

  const expression = getElem("expression");
  expression.placeholder = "(e.g.) 1+2=3-0";

  let btnRuleNm = "ゲームルール";
  let btnChkNm = "回答確認";
  let btnNextNm = "次の問題へ";

  if (langCd === LANG_CD_KO) {
    title = TITLE_NUMBER_PLATE_KO;
    setElemText("title", title);

    btnRuleNm = "게임규칙";
    btnChkNm = "정답확인";
    btnNextNm = "다음문제";

    const footerElem = getElemByTag("footer");
    footerElem.style.visibility = 'hidden';
  }

  setElemText("timer", limitTime.toFixed(2));
  setElemText("btnRule", btnRuleNm);
  setElemText("btnChk", btnChkNm);
  setElemText("btnNext", btnNextNm);

  setLevel(level);
}

// レベル設定
function setLevel(level) {
  let levelVal = SYM_LEVEL;
  if (level === LEVEL_MEDIUM) {
    levelVal = SYM_LEVEL.repeat(2);
  } else if (level === LEVEL_HARD) {
    levelVal = SYM_LEVEL.repeat(3);
  }
  setElemText("level", `Level ${levelVal}`);
}

// タイマー設定
function setTimer() {
  let sec = 30.00;
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
  const rank = getElemText("rank-time");
  const timeVal = getElemText("timer");
  const expression = getElem("expression");
  const expr = expression.value.trim();

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

      const clearTime = 30 - parseFloat(timeVal);
      const clearTimeVal = clearTime.toFixed(2);
      const rankTimeVal = parseFloat(rank);
      if (clearTime != null && clearTimeVal < rankTimeVal) {
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

  // 数字チェック
  const numDigits = num.split(SYM_BLANK).join(SYM_BLANK);
  const exprDigits = expr.split(SYM_BLANK).filter(c => /\d/.test(c)).join(SYM_BLANK);
  if (exprDigits !== numDigits) {
    return errDegitMsg;
  }

  // イコール1つのみ
  if ((expr.match(/=/g) || []).length !== 1) {
    return errEqualMsg;
  }

  const [left, right] = expr.split("=");
  try {
    // 入力フォーマットチェック（数字・演算子のみ）
    if (!/^[\d+\-*/.\s]+$/.test(left) || !/^[\d+\-*/.\s]+$/.test(right)) {
      return errFormatMsg;
    }
  } catch (e) {
    return errFormatMsg;
  }

  // ゼロ除算チェック
  if (expr.includes("/0")) {
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
