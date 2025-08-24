// 記号
const SYM_BLANK = "";
const SYM_LEVEL = "🌟";

// 文字列
COLOR_RED = "red";
COLOR_GREEN = "green";

LEVEL_EASY = "easy";
LEVEL_MEDIUM = "medium";
LEVEL_HARD = "hard";

// メッセージ定義
const MSG_INFO_ANSWER_EXAMPLE = "解の例:";
const MSG_INFO_INPUT_USER = "ユーザ名(英数字)を入力してください。";
const MSG_INFO_OK_ANSWER = "正解です!";
const MSG_INFO_OK_RANK = "新記録！ランクインしました！";

const MSG_ERR_NO_ANSWER = "この問題には解が見つかりませんでした";
const MSG_ERR_NO_INPUT = "入力値がありません";
const MSG_ERR_DIGIT = "4つの数字を1回ずつ使ってください!";
const MSG_ERR_EQUAL = "イコールは1つだけ使ってください!";
const MSG_ERR_FORMAT = "数式の形式が正しくありません!";
const MSG_ERR_DIVIDE_BY_ZERO = "ゼロ除算はできません!";
const MSG_ERR_MATCH = "計算結果が一致しません!";
const MSG_ERR_RANK = "ランク送信に失敗しました";

// URL
const URL_SERVER = "https://kobe-dev.koyeb.app";
const URL_LOCAL = "http://127.0.0.1:5000"
const URL_RANKING_API = "/number/ranking";
const URL_RANKING_SERVER = `${URL_SERVER}${URL_RANKING_API}`;
const URL_RANKING_LOCAL = `${URL_LOCAL}${URL_RANKING_API}`;

// ページ読み込み時にsessionStorageからデータを取得
let userName = sessionStorage.getItem('userName');

// タイマーID
let timerId = null;

// 初期表示
function initDisplay(level) {
  setLevel(level);
  setTimer();
  setUserName();
}

// レベル設定
function setLevel(level) {
  let levelVal = SYM_LEVEL;
  if (level == LEVEL_MEDIUM) {
    levelVal = SYM_LEVEL.repeat(2);
  } else if (level == LEVEL_HARD) {
    levelVal = SYM_LEVEL.repeat(3);
  }
  const levelElem = document.getElementById('level');
  levelElem.textContent = "レベル：" + levelVal;
}

// タイマー設定
function setTimer() {
  let sec = 30.00;
  const timerElem = document.getElementById('timer');
  timerElem.textContent = sec.toFixed(2);

  timerId = setInterval(() => {
    sec -= 0.01;
    timerElem.textContent = sec.toFixed(2);
    if (sec <= 0) {
      clearInterval(timerId);
      timerElem.textContent = "時間切れ";
    }
    if (sec <= 10) {
      timerElem.classList.add(COLOR_RED);
    } else {
      timerElem.classList.remove(COLOR_RED);
    }
  }, 10);
}

// ユーザ名設定
function setUserName() {
  if (!userName || userName == SYM_BLANK) {
    userName = prompt(MSG_INFO_INPUT_USER);
    sessionStorage.setItem('userName', userName);
  }
}

// 正解判定
function checkAnswer() {
  // DOM取得
  const numberDisplay = document.getElementById('number-display');
  const numberAnswer = document.getElementById('number-answer');
  const rankTime = document.getElementById('rank-time');
  const timer = document.getElementById('timer');
  const expression = document.getElementById('expression');

  const num = numberDisplay.textContent;
  const ans = numberAnswer.textContent;
  const rank = rankTime.textContent;
  const timeVal = timer.textContent;
  const expr = expression.value.trim();

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
      clearInterval(timerId);
    } else {
      showMessage(MSG_ERR_NO_ANSWER, false);
    }
  }
};

// 入力チェック
function validate(num, ans, expr) {
  let chkMsg = SYM_BLANK;

  // 回答入力チェック
  if (expr == SYM_BLANK) {
    return MSG_ERR_NO_INPUT;
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
    // 入力フォーマットチェック（数字・演算子のみ）
    if (!/^[\d+\-*/.\s]+$/.test(left) || !/^[\d+\-*/.\s]+$/.test(right)) {
      return MSG_ERR_FORMAT;
    }
  } catch (e) {
    return MSG_ERR_FORMAT;
  }

  // ゼロ除算チェック
  if (expr.includes("/0")) {
    return MSG_ERR_DIVIDE_BY_ZERO;
  }

  // 計算結果比較
  if (!ans.includes(expr)) {
    return MSG_ERR_MATCH;
  }

  return chkMsg;
}

// ランキング送信
function sendRanking(number, time) {
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
      showMessage(MSG_INFO_OK_RANK, true);
    })
    .catch(() => {
      alert(MSG_ERR_RANK);
    });
}

// メッセージ表示
function showMessage(msg, answerFlg) {
  setElem('message', msg, false, answerFlg);
}

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

// ローカル環境判定
function isLocal() {
  let localFlg = false;
  if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
    localFlg = true;
  }
  return localFlg;
};
