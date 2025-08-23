// 記号
const SYM_BLANK = "";

// 文字列
COLOR_RED = "red";
COLOR_GREEN = "green";

// メッセージ定義
const MSG_INFO_ANSWER_EXAMPLE = "解の例:";
const MSG_INFO_OK_ANSWER = "正解です!";
const MSG_INFO_OK_RANK = "ランキング送信完了！";
const MSG_INFO_INPUT_USER = "ユーザ名(英数字)を入力し、ランクインしてください。";

const MSG_ERR_NO_ANSWER = "この問題には解が見つかりませんでした";
const MSG_ERR_NO_INPUT = "入力値がありません";
const MSG_ERR_DIGIT = "4つの数字を1回ずつ使ってください!";
const MSG_ERR_EQUAL = "イコールは1つだけ使ってください!";
const MSG_ERR_FORMAT = "数式の形式が正しくありません!";
const MSG_ERR_MATCH = "計算結果が一致しません!";
const MSG_ERR_RANK = "ランク送信に失敗しました";

// URL
const URL_SERVER = "https://kobe-dev.koyeb.app";
const URL_LOCAL = "http://127.0.0.1:5000"
const URL_RANKING_API = "/number/ranking";
const URL_RANKING_SERVER = `${URL_SERVER}${URL_RANKING_API}`;
const URL_RANKING_LOCAL = `${URL_LOCAL}${URL_RANKING_API}`;

// 変数
let timerId = null;

// 要素設定
function setElem(elemId, text, textFlg, answerFlg) {
  const elem = document.getElementById(elemId);
  if (textFlg) {
    elem.textContent = text;
  } else {
    elem.innerHTML = text;
  }

  let color = COLOR_RED;
  if (answerFlg) {
    color = COLOR_GREEN;
  }

  const style = 'color:' + color + ';';
  elem.style = style;
}

// タイマー設定
function setTimer(text, answerFlg) {
  clearInterval(timerId);
  // setElem('timer', text, true, answerFlg);
}

// メッセージ表示
function showMessage(msg, answerFlg) {
  setElem('message', msg, false, answerFlg);
}

// 初期表示
function initDisp() {
  let sec = 30.00;
  const timerElem = document.getElementById('timer');
  timerElem.textContent = sec.toFixed(2);

  timerId = setInterval(() => {
    sec -= 0.01;
    timerElem.textContent = sec.toFixed(2);
    if (sec <= 0) {
      clearInterval(timerId);
      timerElem.textContent = "時間切れ";
      // timerElem.style.color = "red";
    }
    if (sec <= 10) {
      timerElem.classList.add(COLOR_RED);
    } else {
      timerElem.classList.remove(COLOR_RED);
    }
  }, 10);

  // 現在時刻表示
  // setInterval(showClock, 1000)
}

// 2桁表示
function twoDigit(num) {
  let ret;
  if (num < 10)
    ret = "0" + num;
  else
    ret = num;
  return ret;
}

// 現在時刻表示
function showClock() {
  let nowTime = new Date();
  let nowHour = twoDigit(nowTime.getHours());
  let nowMin = twoDigit(nowTime.getMinutes());
  let nowSec = twoDigit(nowTime.getSeconds());
  let msg = "時刻 " + nowHour + ":" + nowMin + ":" + nowSec;
  document.getElementById("realtime").innerHTML = msg;
}

// チェック
function validate(num, ans, expr) {
  const chkMsg = SYM_BLANK;

  // 回答入力チェック
  if (!expr) {
    return MSG_ERR_NO_INPUT_ANSWER;
  }

  // 数字チェック
  const numDigits = num.split('').join('');
  const exprDigits = expr.split('').filter(c => /\d/.test(c)).join('');
  if (exprDigits !== numDigits) {
    return MSG_ERR_DIGIT;
  }

  // イコール1つのみ
  if ((expr.match(/=/g) || []).length !== 1) {
    return MSG_ERR_EQUAL;
  }

  const [left, right] = expr.split('=');

  try {
    // evalの前に安全性を高める（数字・演算子・カッコのみ許可）
    if (!/^[\d+\-*/().\s]+$/.test(left) || !/^[\d+\-*/().\s]+$/.test(right)) {
      return MSG_ERR_FORMAT;
    }
    // 計算結果比較
    if (!ans.includes(expr)) {
      return MSG_ERR_MATCH;
    }
  } catch (e) {
    return MSG_ERR_FORMAT;
  }

  return chkMsg;
}


// 正解判定
function checkAnswer() {
  // DOM取得
  const numberDisplay = document.getElementById('number-display');
  const expression = document.getElementById('expression');
  const numberAnswer = document.getElementById('number-answer');
  const rankTime = document.getElementById('rank-time');
  const timer = document.getElementById('timer');

  const num = numberDisplay.textContent;
  const ans = numberAnswer.textContent;
  const rank = rankTime.textContent;
  const expr = expression.value.trim();
  const timeVal = timer.textContent;

  let chkMsg = validate(num, ans, expr);

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
        sendRanking(numVal, clearTimeVal);
      }
      setTimer("クリア！", true);
    } else {
      showMessage(MSG_ERR_NO_ANSWER, false);
    }
  }
};

// ランキング送信
function sendRanking(number, time) {
  const user = prompt(MSG_INFO_INPUT_USER);

  let rankingUrl = URL_RANKING_SERVER;
  if (isLocal()) {
    rankingUrl = URL_RANKING_LOCAL;
  }

  fetch(rankingUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      number: number,
      user: user,
      time: time,
      date: new Date()
    })
  })
    .then(res => res.json())
    .then(data => {
      alert(data.message || MSG_INFO_OK_RANK);
    })
    .catch(() => {
      alert(MSG_ERR_RANK);
    });
}

// ローカル環境判定
function isLocal() {
  let localFlg = false;
  if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
    localFlg = true;
  }
  return localFlg;
};
