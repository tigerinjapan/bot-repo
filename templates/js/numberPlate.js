// ページ読み込み時にsessionStorageからデータを取得
let userName = sessionStorage.getItem('userName');

// タイマーID
let timerId = null;

// タイマー状態管理
let isTimerRunning = false;

// START/STOPボタン処理
document.addEventListener("DOMContentLoaded", () => {
  const startBtn = document.getElementById("btnStart");
  if (startBtn) {
    startBtn.textContent = "START";
    startBtn.addEventListener("click", () => {
      if (!isTimerRunning) {
        setTimer();
        startBtn.textContent = "STOP";
        isTimerRunning = true;
      } else {
        clearInterval(timerId);
        setElem("timer", "STOPPED", true);
        startBtn.textContent = "START";
        isTimerRunning = false;
      }
    });
  }
});

// 初期表示
function initDisplay(lang, level) {
  let title = TITLE_NUMBER_PLATE;
  document.title = title;

  let btnChkNm = "回答確認";
  let btnNextNm = "次の問題へ";
  let ruleList = LIST_GAME_RULE;
  let inputMsg = MSG_INFO_INPUT_USER;

  if (lang == LANG_CD_KO) {
    title = TITLE_NUMBER_PLATE_KO;
    setElem("title", title, true);

    btnChkNm = "정답확인";
    btnNextNm = "다음문제";
    ruleList = LIST_GAME_RULE_KO;
    inputMsg = MSG_INFO_INPUT_USER_KO;
  }

  setElem("timer", 30.00.toFixed(2), true);
  setElem("btnChk", btnChkNm, true);
  setElem("btnNext", btnNextNm, true);
  setGameRule(ruleList);

  setLevel(level);
  setUserName(inputMsg);
}

// ゲームルール生成
function setGameRule(ruleList) {
  for (let i = 0; i < ruleList.length; i++) {
    createElem(TAG_LI, ruleList[i], "gameRule");
  }
}

// レベル設定
function setLevel(level) {
  let levelVal = SYM_LEVEL;
  if (level == LEVEL_MEDIUM) {
    levelVal = SYM_LEVEL.repeat(2);
  } else if (level == LEVEL_HARD) {
    levelVal = SYM_LEVEL.repeat(3);
  }
  setElem('level', "Level：" + levelVal, true);
}

// タイマー設定
function setTimer() {
  let sec = 30.00;
  const timerElem = getElem('timer');
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
  if (!userName || userName == SYM_BLANK) {
    userName = prompt(inputMsg);
    sessionStorage.setItem('userName', userName);
  }
}

// 正解判定
function checkAnswer(lang) {
  let noAnswerMsg = MSG_ERR_NO_ANSWER;

  if (lang == LANG_CD_KO) {
    noAnswerMsg = MSG_ERR_NO_ANSWER_KO;
  }

  // DOM取得
  const numberDisplay = getElem('number-display');
  const numberAnswer = getElem('number-answer');
  const rankTime = getElem('rank-time');
  const timer = getElem('timer');
  const expression = getElem('expression');

  const num = numberDisplay.textContent;
  const ans = numberAnswer.textContent;
  const rank = rankTime.textContent;
  const timeVal = timer.textContent;
  const expr = expression.value.trim();

  let chkMsg = validate(num, ans, expr, lang);

  if (chkMsg) {
    showMessage(chkMsg, false);
  } else {
    if (ans) {
      let ansList = ans;
      if (typeof ans === "string") {
        ansList = ans.split(";").filter(s => s.trim());
      }
      const ansHtml = '<ul>' + ansList.map(a => `<li>${a}</li>`).join('') + '</ul>';
      showMessage(MSG_INFO_OK_ANSWER + ansHtml, true);

      const clearTime = 30 - parseFloat(timeVal);
      const clearTimeVal = clearTime.toFixed(2);
      const rankTimeVal = parseFloat(rank);
      if (clearTime != null && clearTimeVal < rankTimeVal) {
        const numVal = parseInt(num);
        sendRanking(numVal, clearTimeVal, lang);
      }
      clearInterval(timerId);
    } else {
      showMessage(noAnswerMsg, false);
    }
  }
};

// 入力チェック
function validate(num, ans, expr, lang) {
  let chkMsg = SYM_BLANK;

  let noInputMsg = MSG_ERR_NO_INPUT;
  let errDegitMsg = MSG_ERR_DIGIT;
  let errEqualMsg = MSG_ERR_EQUAL;
  let errFormatMsg = MSG_ERR_FORMAT;
  let noDivideZeroMsg = MSG_ERR_DIVIDE_BY_ZERO;
  let errMatchMsg = MSG_ERR_MATCH;

  if (lang == LANG_CD_KO) {
    noInputMsg = MSG_ERR_NO_INPUT_KO;
    errDegitMsg = MSG_ERR_DIGIT_KO;
    errEqualMsg = MSG_ERR_EQUAL_KO;
    errFormatMsg = MSG_ERR_FORMAT_KO;
    noDivideZeroMsg = MSG_ERR_DIVIDE_BY_ZERO_KO;
    errMatchMsg = MSG_ERR_MATCH_KO;
  }

  // 回答入力チェック
  if (expr == SYM_BLANK) {
    return noInputMsg;
  }

  // 数字チェック
  const numDigits = num.split('').join('');
  const exprDigits = expr.split('').filter(c => /\d/.test(c)).join('');
  if (exprDigits !== numDigits) {
    return errDegitMsg;
  }

  // イコール1つのみ
  if ((expr.match(/=/g) || []).length !== 1) {
    return errEqualMsg;
  }

  const [left, right] = expr.split('=');
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
function sendRanking(number, time, lang) {
  let rankOkMsg = MSG_INFO_OK_RANK;
  let rankNgMsg = MSG_ERR_RANK;

  if (lang == LANG_CD_KO) {
    rankOkMsg = MSG_INFO_OK_RANK_KO;
    rankNgMsg = MSG_ERR_RANK_KO;
  }

  let rankingUrl = URL_RANKING_SERVER;
  if (isLocal()) {
    rankingUrl = URL_RANKING_LOCAL;
  }

  fetch(rankingUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      number: number,
      user: userName,
      time: time,
      date: new Date()
    })
  })
    .then(res => res.json())
    .then(data => {
      console.log(data.message);
      showMessage(rankOkMsg, true);
    })
    .catch(() => {
      alert(rankNgMsg);
    });
}
