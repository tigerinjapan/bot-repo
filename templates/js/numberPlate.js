// メッセージ定義
const MSG_ANSWER_EXAMPLE = "解の例:";
const MSG_INFO_CORRECT_ANSWER = "正解です!";
const MSG_ERR_NO_EXIST_ANSWER = "この問題には解が見つかりませんでした";
const MSG_ERR_NO_INPUT_ANSWER = "入力値がありません";

// メッセージ表示
function showMessage(msg, answer_flg) {
  const messageArea = document.getElementById('message');
  messageArea.innerHTML = msg;

  let color = "red";
  if (answer_flg) {
    color = "green";
  }

  const style = 'color:' + color + ';';
  messageArea.style = style;
}


// 入力チェック
function validate(num, ans, expr) {
  const chkMsg = SYM_BLANK;

  // 入力チェック
  if (!expr) {
    return MSG_ERR_NO_INPUT_ANSWER;
  }

  // 数字チェック
  const num_digits = num.split('').join('');
  const expr_digits = expr.split('').filter(c => /\d/.test(c)).join('');
  if (expr_digits !== num_digits) {
    return "4つの数字を1回ずつ使ってください!";
  }

  // イコール1つのみ
  if ((expr.match(/=/g) || []).length !== 1) {
    return "イコールは1つだけ使ってください!";
  }

  const [left, right] = expr.split('=');

  try {
    // evalの前に安全性を高める（数字・演算子・カッコのみ許可）
    if (!/^[\d+\-*/().\s]+$/.test(left) || !/^[\d+\-*/().\s]+$/.test(right)) {
      return "数式の形式が正しくありません!";
    }
    // 計算結果比較
    if (!ans.includes(expr)) {
      return "計算結果が一致しません!";
    }
  } catch (e) {
    return "数式の形式が正しくありません!";
  }
  return chkMsg;
}


// 正解判定
function checkAnswer() {
  // DOM取得
  const numberDisplay = document.getElementById('number-display');
  const expression = document.getElementById('expression');
  const numberAnswer = document.getElementById('number-answer');

  const num = numberDisplay.textContent;
  const ans = numberAnswer.textContent;
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
      showMessage(MSG_INFO_CORRECT_ANSWER + ansHtml, true);
    } else {
      showMessage(MSG_ERR_NO_EXIST_ANSWER, false);
    }
  }
};
