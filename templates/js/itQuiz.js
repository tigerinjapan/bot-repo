// ヘッダー設定
setElemContentsByTag(TAG_HEAD, CONTENTS_HEAD_1);

// タイトル設定
document.title = TITLE_IT_QUIZ;

// ページ読み込み時にsessionStorageからデータを取得
let userName = sessionStorage.getItem(STR_USER_NAME);

/**
 * 定数と初期データ定義
 */

// クイズ数
const quizNum = 5;

// 単語長さ制限
const MAX_WORD_LENGTH = 6;

// 1問のポイント
const PLUS_POINT = 20;

// 1問のポイント
const PLUS_POINT_HALF = PLUS_POINT / 2;

// 減点
const MINUS_POINT = (PLUS_POINT / 10) * -1;

// id
const ID_MESSAGE_DIALOG = "message-dialog";
const ID_CHOICE_DIALOG = "choice-dialog";
const ID_RULE_DIALOG = "rule-dialog";

// 変数
let dataList, rankingDataJson;

// グローバルなゲーム状態を保持するオブジェクト
const gameState = {
  selectedLanguage: LANG_CD_KO, // 初期言語設定は韓国語
  currentQuizIndex: 0,
  score: 0,
  currentWord: [], // 現在の単語の状態（例: ['G', '_', 'M', '_', 'N', 'I']）
  quizSet: [],
  timeRemaining: 0,
  initialTime: 0,
  timerInterval: null,
  hintsUsed: 0,
  selectedCharIndex: -1, // 現在選択されている空欄のインデックス
  isGameOver: false,
};

// UI要素の多言語テキスト辞書（ボタン名やラベルなど）
const textMap = {
  "title": { "ko": "IT 상식 퀴즈", "ja": "IT クイズ", "en": "IT Quiz" },
  "user_label": { "ko": "유저 ", "ja": "ユーザー ", "en": "User " },
  "score_label": { "ko": "점수 ", "ja": "スコア ", "en": "Score " },
  "quiz_status_label": { "ko": "문제 ", "ja": "問題 ", "en": "Quiz " },
  "start_game": { "ko": "게임 시작", "ja": "ゲームスタート", "en": BUTTON_START },
  "game_rule": { "ko": "게임 규칙", "ja": "ゲームルール", "en": TITLE_GAME_RULES },
  "hint": { "ko": "힌트", "ja": "ヒント", "en": BUTTON_HINT },
  "home": { "ko": "홈", "ja": "ホームへ", "en": BUTTON_HOME },
  "check_answer": { "ko": "정답 확인", "ja": "正解確認", "en": "CHECK ANSWER" },
  "instruction_message": {
    "ko": "알파벳 또는 숫자만 입력가능합니다.",
    "ja": "英数字のみ入力してください。",
    "en": "Select a character or use your keyboard."
  },
};

// メッセージ、エラー、ダイアログコンテンツの多言語辞書
const msgMap = {
  "rule_content": {
    "ko": `
        <p><strong>1. 게임내용</strong><br>주어진 설명으로 IT 단어 맞추기 (총 ${quizNum} 문제)</p>
        <p><strong>2. 제한시간</strong><br>단어 글자수 x 10초 (예: 3글자: 30초)</p>
        <p><strong>3. 힌트</strong><br>단어의 첫 글자는 공개. <br>
        [힌트]를 누르면 1글자씩 공개 (힌트 = 최대 글자수 -1)</p>
        <p><strong>4. 득점</strong><br></p>
        <ul>
            <li>제한 시간의 절반 이내 정답: <b>${PLUS_POINT}점</b></li>
            <li>그 외 시간 내 정답: <b>${PLUS_POINT_HALF}점</b></li>
        </ul>
        <p><strong>5. 감점</strong><br></p>
        <ul>
            <li>글자 선택 오답: <b>${MINUS_POINT}점</b></li>
            <li>힌트 사용 시: <b>${MINUS_POINT}점</b></li>
        </ul>
        <p>※최소 점수: 0점</p>
    `,
    "ja": `
        <p><strong>1. 目標:</strong> 与えられた説明をヒントにIT用語を当てます (全${quizNum}問)。</p>
        <p><strong>2. 時間:</strong> 制限時間は単語の文字数 x 10秒です。(例: 3文字: 30秒)</p>
        <p><strong>3. ヒント:</strong> 単語の最初の文字は公開されます。<br>
        「ヒント」を押すと1文字ずつ公開されます (最大文字数 $-1$まで)。</p>
        <p><strong>4. 得点:</strong></p>
        <ul>
            <li>制限時間の半分以内での正解: <b>${PLUS_POINT}点</b></li>
            <li>それ以外の時間内での正解: <b>${PLUS_POINT_HALF}点</b></li>
        </ul>
        <p><strong>5. 減点:</strong></p>
        <ul>
            <li>文字選択での不正解: <b>${MINUS_POINT}点</b></li>
            <li>ヒント使用時: <b>${MINUS_POINT}点</b></li>
        </ul>
        <p>最低点数は0点です。</p>
    `,
    "en": `
        <p><strong>1. Goal:</strong> Guess the IT term based on the provided description (Total ${quizNum} questions).</p>
        <p><strong>2. Time Limit:</strong> Word length x 10 seconds.(ex) 3ch: 30s.</p>
        <p><strong>3. Hint:</strong> The first letter is revealed. <br>
        Using 'HINT' reveals one letter at a time (up to Word Length - 1).</p>
        <p><strong>4. Scoring:</strong></p>
        <ul>
            <li>Correct within half the time limit: <b>${PLUS_POINT} points</b></li>
            <li>Correct after half the time limit: <b>${PLUS_POINT_HALF} points</b></li>
        </ul>
        <p><strong>5. Penalties:</strong></p>
        <ul>
            <li>Incorrect character selection: <b>${MINUS_POINT} point</b></li>
            <li>Using a hint: <b>${MINUS_POINT} point</b></li>
        </ul>
        <p>The minimum score is 0.</p>
    `
  },
  "game_over": { "ko": "게임 오버! 최종 점수:", "ja": "ゲームオーバー! 最終スコア:", "en": "GAME OVER! Final Score:" },
  "correct": { "ko": "정답입니다! 다음 문제로 넘어갑니다.", "ja": "正解です！次の問題に進みます。", "en": "Correct! Moving to the next quiz." },
  "timeout": { "ko": "시간 초과! 정답은 %WORD%였습니다.", "ja": "時間切れです！正解は %WORD% でした。", "en": "Time up! The answer was %WORD%." },
  "invalid_choice": {
    "ko": `X 오답입니다! (${MINUS_POINT}점)`,
    "ja": `X 不正解です！(${MINUS_POINT}点)`,
    "en": `X Incorrect choice! (${MINUS_POINT} point)`
  },
  "wrong_answer": { "ko": "아직 정답이 아닙니다.", "ja": "まだ正解ではありません。", "en": "Not the correct answer yet." },
  "hint_used": {
    "ko": `힌트를 사용했습니다! (${MINUS_POINT}점)`,
    "ja": `ヒントを使用しました！(${MINUS_POINT}点)`,
    "en": `Hint used! (${MINUS_POINT} point)`
  },
  "no_more_hints": { "ko": "더 이상 힌트를 사용할 수 없습니다.", "ja": "これ以上ヒントは使えません。", "en": "No more hints available." },
  "already_solved": { "ko": "이미 해결된 빈칸입니다.", "ja": "すでに解決済みの空欄です。", "en": "This blank is already solved." },
  "input_error": { "ko": "잘못된 입력입니다.", "ja": "不正な入力です。", "en": "Invalid input." }
};

// 英語の文字と数字のプール
const charPool = {
  letters: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
  numbers: '0123456789'
};


// 多言語テキスト取得ヘルパー
const getLocalizedText = (key) => {
  const lang = gameState.selectedLanguage;
  return textMap[key] ? (textMap[key][lang] || textMap[key][LANG_CD_EN]) : key;
};

// 多言語メッセージ取得ヘルパー
const getLocalizedMessage = (key, placeholder = {}) => {
  const lang = gameState.selectedLanguage;
  let msg = msgMap[key] ? (msgMap[key][lang] || msgMap[key][LANG_CD_EN]) : key;
  for (const p in placeholder) {
    msg = msg.replace(`%${p}%`, placeholder[p]);
  }
  return msg;
};

// モーダル表示
const showDialog = (id, contentKey = null, placeholder = {}) => {
  const dialog = getElem(id);
  if (contentKey) {
    setElemContents('dialog-content', getLocalizedMessage(contentKey, placeholder));
  }
  if (dialog) {
    dialog.showModal();
  }
};

// モーダル非表示
const closeDialog = (id) => {
  const dialog = getElem(id);
  if (dialog) {
    dialog.close();
  }
};

// 配列シャッフル（フィッシャー・イェーツ）
const shuffleArray = (array) => {
  for (let i = array.length - 1; 0 < i; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
};

/**
 * ゲーム画面のレンダリング
 */

// 初期画面：言語選択/ランキング表示
const renderInitialScreen = () => {
  const container = getElem('main-container');

  // ランキングデータ
  dataList = getElemText("dataList");

  // JSON形式の文字列に変換する
  rankingDataJson = JSON.parse(dataList);

  // ランキングリストの作成
  const rankingsHtml = rankingDataJson.map(item => `
    <li class="ranking-item">
      <span class="rank">${item.rank}</span>
      <span>${item.score} pts</span>
      <span>${item.userName}</span>
      <span>${item.updateDate}</span>
    </li>
  `).join(SYM_BLANK);

  container.innerHTML = `
      <h1 class="title">${TITLE_IT_QUIZ}</h1>
      <div class="flex-center">
        <button class="btn btn-secondary lang-btn" data-lang=${LANG_CD_JA} onclick="onLanguageSelect('${LANG_CD_JA}')">日本語</button>
        <button class="btn btn-secondary lang-btn" data-lang=${LANG_CD_KO} onclick="onLanguageSelect('${LANG_CD_KO}')">한국어</button>
        <button class="btn btn-secondary lang-btn" data-lang=${LANG_CD_EN} onclick="onLanguageSelect('${LANG_CD_EN}')">English</button>
      </div>
      <div class="flex-center">
        <label class="inputLbl" for="inputUserName">${STR_USER.toUpperCase()}</label>
        <input class="inputTxt" type="text" id="inputUserName" minlength="4" maxlength="10" placeholder="Input user name.">
      </div>
      <div class="flex-center">
        <button class="btn" id="btnStartGame" disabled>${BUTTON_START}</button>
        <button class="btn" id="btnGameRule" disabled onclick="showRuleDialog()">${BUTTON_RULE}</button>
      </div>
      <h2>${TITLE_TOP_RANK}</h2>
      <ul id="ranking-list">
        ${rankingsHtml}
      </ul>
  `;

  // ボタンのループ処理
  const divList = ["message", "rule", "choice"];
  divList.forEach(div => {
    const btnElem = getElem(`${div}-close-btn`);
    btnElem.className = "btn btn-secondary";
    btnElem.textContent = BUTTON_CLOSE;
    btnElem.onclick = () => closeDialog(`${div}-dialog`);
  });

  // START GAMEボタンにイベント付与
  const btnStart = getElem('btnStartGame');
  const inputUserName = getElem('inputUserName');
  if (btnStart) {
    btnStart.addEventListener(EVENT_CLICK, () => {
      userName = inputUserName.value.trim();

      // ユーザー名が4文字以上10文字以下の場合のみ有効
      if (4 <= userName.length && userName.length <= 10) {
        sessionStorage.setItem(STR_USER_NAME, userName);
        startGame();
      } else {
        alert(MSG_INPUT_USER_EN);
      }
    });
  }
};

// 言語選択ボタン押下時の処理（背景色変更＆START GAME活性化）
function onLanguageSelect(lang) {
  gameState.selectedLanguage = lang;

  // 言語ボタンの背景色を切り替え
  const langBtns = document.querySelectorAll('.lang-btn');
  langBtns.forEach(btn => {
    if (btn.dataset.lang === lang) {
      btn.style.backgroundColor = COLOR_BLUE;
      btn.style.color = COLOR_WHITE;
      btn.style.fontWeight = FONT_BOLD;
    } else {
      btn.style.backgroundColor = SYM_BLANK;
      btn.style.color = SYM_BLANK;
      btn.style.fontWeight = SYM_BLANK;
    }
  });

  // START GAMEボタンを有効化
  const btnStart = getElem('btnStartGame');
  const btnRule = getElem('btnGameRule');
  if (btnStart && btnRule) {
    btnStart.className = "btn btn-primary";
    btnStart.disabled = false;
    btnStart.classList.add('active');
    btnRule.className = "btn btn-secondary";
    btnRule.disabled = false;
    btnRule.classList.add('active');
  }
}

// ゲームプレイ画面をレンダリングする
const renderQuizScreen = () => {
  const container = getElem('main-container');

  // UIラベルは英語固定
  container.innerHTML = `
    <h1 class="title">${getLocalizedText('title')}</h1>
    
    <!-- ユーザー情報とステータス -->
    <div class="flex-row">
      <span class="text-label">【${getLocalizedText('quiz_status_label')}】</span>
      <span class="text-value" id="quiz-status">1 / ${quizNum}</span>
      <span class="text-label">【${getLocalizedText('score_label')}】</span>
      <span class="text-value" id="current-score">${gameState.score} pts</span>
      <span class="text-label">【${getLocalizedText('user_label')}】</span>
      <span class="text-value">${userName}</span>
      </div>

    <!-- タイムバー -->
    <div id="timer-bar"><div id="timer-progress"></div></div>

    <!-- ゲームルールボタン -->
    <div class="flex-end">
      <button class="btn btn-secondary" onclick="showRuleDialog()">${getLocalizedText('game_rule')}</button>
    </div>

    <!-- クイズ単語表示領域 -->
    <div id="quiz-word" oncontextmenu="return false;">
      <!-- 文字ボックスがここに挿入されます -->
    </div>

    <!-- クイズ説明 -->
    <div id="quiz-description"></div>

    <!-- 操作ボタン -->
    <div class="flex-center">
      <button class="btn btn-secondary" id="hint-button" onclick="useHint()">${getLocalizedText('hint')}</button>
      <button class="btn btn-secondary" id="home-button" onclick="goHome()">${getLocalizedText('home')}</button>
      <button class="btn btn-primary" id="check-button" onclick="checkAnswer()">${getLocalizedText('check_answer')}</button>
    </div>
  `;

  renderQuizStatus();
  renderQuizWord();
};

// スコア、ステータス、説明を更新する
const renderQuizStatus = () => {
  const currentQuiz = gameState.quizSet[gameState.currentQuizIndex];
  if (!currentQuiz) return;

  setElemText('current-score', `${gameState.score} pts`);
  setElemText('quiz-status', `${gameState.currentQuizIndex + 1} / ${gameState.quizSet.length}`);

  // 説明文は選択言語に合わせる
  const descriptionKey = `description_${gameState.selectedLanguage}`;
  setElemText('quiz-description', currentQuiz[descriptionKey]);

  updateTimerDisplay();
};

// クイズ単語の状態を画面に反映する
const renderQuizWord = () => {
  const quizWordElem = getElem('quiz-word');
  if (!quizWordElem) return;

  quizWordElem.innerHTML = gameState.currentWord.map((char, index) => {
    // スペースの場合
    if (char === ' ') {
      return `<div class="quiz-char-box quiz-char-space">&nbsp;</div>`;
    }
    // 空欄の場合
    if (char === '_') {
      return `<div class="quiz-char-box quiz-char-blank" data-index="${index}" onclick="openChoiceDialog(${index})" tabindex="0">?</div>`;
    }
    // 公開されている文字の場合
    return `<div class="quiz-char-box">${char}</div>`;
  }).join(SYM_BLANK);
};

// タイマー表示の更新
const updateTimerDisplay = () => {
  const progress = getElem('timer-progress');
  if (!progress || gameState.initialTime === 0) return;

  const percentage = (gameState.timeRemaining / gameState.initialTime) * 100;
  progress.style.width = `${Math.max(0, percentage)}%`;
  progress.style.backgroundColor = 25 < percentage ? (50 < percentage ? '#ff69b4' : '#ffc0cb') : '#ff4500'; // 色変化
};

/**
 * ゲームロジックと状態管理
 */

// ゲームの開始
async function startGame() {
  if (gameState.timerInterval) clearInterval(gameState.timerInterval);

  gameState.score = 0;
  gameState.currentQuizIndex = -1; // nextQuizで0から開始するため
  gameState.isGameOver = false;

  let quizDataUrl = URL_IT_QUIZ_SERVER;
  if (isLocal()) {
    quizDataUrl = URL_IT_QUIZ_LOCAL;
  }

  // クイズデータ (IT関連用語、単語は全て大文字) - シャッフルし、選択
  const quizDataList = await getFetchApiData(quizDataUrl, null);
  const filteredList = quizDataList.filter(q => q.word.replace(/\s/g, SYM_BLANK).length <= MAX_WORD_LENGTH);
  const randomTenList = shuffleArray([...filteredList]).slice(0, quizNum);
  gameState.quizSet = randomTenList;

  // ゲーム画面へ移行
  renderQuizScreen();

  // 最初の問題を開始
  nextQuiz();

  // キーボードイベントリスナーを設定
  setupKeyboardListener();
};

// 次のクイズへ
const nextQuiz = () => {
  // タイマーを停止
  if (gameState.timerInterval) {
    clearInterval(gameState.timerInterval);
  }

  gameState.currentQuizIndex++;
  if (gameState.quizSet.length <= gameState.currentQuizIndex) {
    // 全てのクイズが終了
    gameOver();
    return;
  }

  const currentQuiz = gameState.quizSet[gameState.currentQuizIndex];
  const word = currentQuiz.word;

  // 状態リセット
  gameState.hintsUsed = 0;
  gameState.currentWord = Array(word.length).fill('_');

  // 最初の文字を公開する（2文字の単語は除く）
  if (2 < word.length) {
    // 最初の有効な文字（スペース以外）を見つけて公開
    for (let i = 0; i < word.length; i++) {
      if (word[i] !== ' ') {
        gameState.currentWord[i] = word[i];
        break;
      }
    }
  }

  // スペースは最初から公開
  for (let i = 0; i < word.length; i++) {
    if (word[i] === ' ') {
      gameState.currentWord[i] = ' ';
    }
  }

  // 新しい時間制限を設定
  const wordWithoutSpaces = word.replace(/\s/g, SYM_BLANK);
  gameState.initialTime = wordWithoutSpaces.length * 10;
  gameState.timeRemaining = gameState.initialTime;

  // 画面を更新し、タイマーを開始
  renderQuizStatus();
  renderQuizWord();
  startTimer();
};

// タイマー開始
const startTimer = () => {
  if (gameState.timerInterval) clearInterval(gameState.timerInterval);

  gameState.timerInterval = setInterval(() => {
    gameState.timeRemaining--;
    updateTimerDisplay();

    if (gameState.timeRemaining <= 0) {
      clearInterval(gameState.timerInterval);
      handleTimeout();
    }
  }, 1000);
};

// タイムアウト処理
const handleTimeout = () => {
  if (gameState.isGameOver) return; // 二重処理防止

  const currentQuiz = gameState.quizSet[gameState.currentQuizIndex];
  showDialog(ID_MESSAGE_DIALOG, 'timeout', { 'WORD': currentQuiz.word });

  // 3秒後に次の問題へ
  setTimeout(nextQuiz, 3000);
};

// ホーム画面へ
function goHome() {
  gameState.isGameOver = true;
  if (gameState.timerInterval) clearInterval(gameState.timerInterval);

  userName = SYM_BLANK;
  renderInitialScreen();
}

// ヒント使用
const useHint = () => {
  const currentWord = gameState.quizSet[gameState.currentQuizIndex].word;
  const blanks = gameState.currentWord
    .map((char, index) => char === '_' ? index : -1)
    .filter(index => index !== -1);

  // 残りの空欄数が最大ヒント回数を超えていないかチェック
  if (currentWord.length - 1 <= gameState.hintsUsed || blanks.length === 0) {
    showDialog(ID_MESSAGE_DIALOG, 'no_more_hints');
    return;
  }

  // ランダムに空欄を一つ選ぶ
  const randomIndex = blanks[Math.floor(Math.random() * blanks.length)];

  // 文字を公開し、状態とスコアを更新
  gameState.currentWord[randomIndex] = currentWord[randomIndex];
  gameState.hintsUsed++;

  // 減点処理
  gameState.score = Math.max(0, gameState.score + MINUS_POINT);

  showDialog(ID_MESSAGE_DIALOG, 'hint_used');
  renderQuizStatus();
  renderQuizWord();
};

// 正解チェック
const checkAnswer = () => {
  const currentQuiz = gameState.quizSet[gameState.currentQuizIndex];
  const currentWordString = gameState.currentWord.join(SYM_BLANK); // 配列を文字列に変換

  // 2単語の場合に対応するため、全てのスペース('_'になっていないことを確認)を含めた完全一致をチェック
  if (currentWordString === currentQuiz.word) {
    // 正解時のスコアリング
    clearInterval(gameState.timerInterval);

    const halfTime = gameState.initialTime / 2;
    let points = 0;

    if (halfTime < gameState.timeRemaining) {
      points = PLUS_POINT;
    } else {
      // halfTime を5等分した1区間の時間
      const segmentTime = halfTime / 5;

      // timeRemaining が halfTime からどれだけ遅れているかを計算
      const delay = halfTime - gameState.timeRemaining;

      // 遅延がどの区間に該当するかを計算 (1区間目なら1, 2区間目なら2, ...)
      // Math.ceil() で切り上げることにより、0.01秒遅れた時点で次の区間に入るようにする
      let segmentIndex = Math.ceil(delay / segmentTime);

      // 区間インデックスを最大5（5等分）に制限
      if (5 < segmentIndex) {
        segmentIndex = 5;
      }

      // 減点ポイントを計算 (1区間目は -2点, 2区間目は -4点, ...)
      const deduction = segmentIndex * 2;

      // 点数を計算
      points = PLUS_POINT - deduction;
    }

    gameState.score += points;

    showDialog(ID_MESSAGE_DIALOG, 'correct');

    // 3秒後に次の問題へ
    setTimeout(nextQuiz, 3000);
  } else {
    showDialog(ID_MESSAGE_DIALOG, 'wrong_answer');
  }
};

// 文字選択ダイアログを開く
const openChoiceDialog = (index) => {
  if (gameState.currentWord[index] !== '_') {
    showDialog(ID_MESSAGE_DIALOG, 'already_solved');
    return;
  }

  gameState.selectedCharIndex = index;

  setElemText("choice-title", TITLE_CHOICE_CHAR);

  const targetWord = gameState.quizSet[gameState.currentQuizIndex].word;
  const correctChar = targetWord[index];
  const isLetter = charPool.letters.includes(correctChar);
  const isNumber = charPool.numbers.includes(correctChar);

  let availablePool = [];
  if (isLetter) {
    availablePool = charPool.letters.split(SYM_BLANK);
  } else if (isNumber) {
    availablePool = charPool.numbers.split(SYM_BLANK);
  } else {
    // 文字でも数字でもない場合（通常はスペースのはずだが、_として残っている場合はエラー回避）
    return;
  }

  // 正解文字をプールから除外（後のシャッフル用）
  const filteredPool = availablePool.filter(char => char !== correctChar);

  // 候補を作成: 正解文字 + 誤答文字4つ（重複なし）
  let choices = [correctChar];
  while (choices.length < 5 && 0 < filteredPool.length) {
    const randomIndex = Math.floor(Math.random() * filteredPool.length);
    choices.push(filteredPool.splice(randomIndex, 1)[0]);
  }

  shuffleArray(choices); // 候補をシャッフル

  // ダイアログの中身をレンダリング
  const container = getElem('choice-buttons-container');
  container.innerHTML = SYM_BLANK;

  const instruction = getElem('choice-instruction');

  // キーボード入力案内
  instruction.textContent = `${getLocalizedText('instruction_message')} (A-Z, 0-9)`;

  choices.forEach(char => {
    const button = createElemOnly(TAG_BUTTON);
    button.className = 'choice-btn';
    button.textContent = char;
    button.setAttribute('data-char', char);
    button.onclick = () => handleChoice(char);
    container.appendChild(button);
  });

  // ダイアログを表示
  getElem(ID_CHOICE_DIALOG).showModal();
};

// 文字選択処理
const handleChoice = (char) => {
  const index = gameState.selectedCharIndex;
  const targetWord = gameState.quizSet[gameState.currentQuizIndex].word;
  const correctChar = targetWord[index];
  const choiceDialog = getElem(ID_CHOICE_DIALOG);

  if (char === correctChar) {
    // 正解の場合
    gameState.currentWord[index] = char;
    closeDialog(ID_CHOICE_DIALOG);
    renderQuizWord();

    // 正解をチェックし、クリアしていれば次の問題へ
    if (gameState.currentWord.join(SYM_BLANK) === targetWord) {
      checkAnswer();
    }
  } else {
    // 不正解の場合
    // 減点処理
    gameState.score = Math.max(0, gameState.score + MINUS_POINT);
    renderQuizStatus();

    // ダイアログを閉じずに、不正解のボタンを無効化
    const chosenButton = choiceDialog.querySelector(`[data-char="${char}"]`);
    if (chosenButton) {
      chosenButton.disabled = true;
    }

    // 誤答メッセージを可愛く表示
    showDialog(ID_MESSAGE_DIALOG, 'invalid_choice');
  }
};

// キーボード入力のセットアップ
const setupKeyboardListener = () => {
  // 既存のリスナーがあれば一度削除（二重登録防止）
  document.removeEventListener('keydown', handleGlobalKeydown);
  document.addEventListener('keydown', handleGlobalKeydown);
};

// グローバルなキーボードイベントハンドラ
const handleGlobalKeydown = (event) => {
  const key = event.key.toUpperCase();
  const choiceDialog = getElem(ID_CHOICE_DIALOG);

  // 文字選択ダイアログが開いている場合のみ処理
  if (choiceDialog.open && gameState.selectedCharIndex !== -1) {
    // A-Z または 0-9 のキー入力をチェック
    if (charPool.letters.includes(key) || charPool.numbers.includes(key)) {
      const choiceButton = choiceDialog.querySelector(`[data-char="${key}"]`);

      // 候補ボタンが存在し、かつ無効化されていない場合のみ処理を実行
      if (choiceButton && !choiceButton.disabled) {
        event.preventDefault(); // 予期せぬブラウザ動作を防止
        handleChoice(key);
      } else if (charPool.letters.includes(key) || charPool.numbers.includes(key)) {
        // 候補にない文字や無効なボタンを押した場合もエラー表示
        showDialog(ID_MESSAGE_DIALOG, 'input_error');
      }
    }
  } else if (key === 'ESCAPE') {
    // Escapeキーで開いているダイアログを閉じる
    if (choiceDialog.open) closeDialog(ID_CHOICE_DIALOG);
    if (getElem(ID_MESSAGE_DIALOG).open) closeDialog(ID_MESSAGE_DIALOG);
    if (getElem(ID_RULE_DIALOG).open) closeDialog(ID_RULE_DIALOG);
  }
};

/**
 * ランキング更新処理
 */
function getUpdateRank() {
  // 5位以内のランキングで自分のスコアより低いランクを検索
  let updateRank = null;

  for (let i = 0; i < Math.min(5, rankingDataJson.length); i++) {
    if (rankingDataJson[i].score <= gameState.score) {
      updateRank = rankingDataJson[i].rank;
      break;
    }
  }
  return updateRank;
}

/**
 * ゲーム終了処理
 */
const gameOver = () => {
  gameState.isGameOver = true;
  if (gameState.timerInterval) clearInterval(gameState.timerInterval);

  // スコアを明示的に表示
  const msg = `${getLocalizedMessage('game_over')} ${gameState.score} pts`;
  setElemText('dialog-content', msg);
  getElem(ID_MESSAGE_DIALOG).showModal();

  // ランキング更新判定・API送信
  const updateRank = getUpdateRank();
  if (updateRank !== null) {
    updateRanking(updateRank, gameState.score, userName);
  }

  // 3秒後に初期画面へ
  setTimeout(renderInitialScreen, 3000);
};

// ランキングをAPI経由で更新
async function updateRanking(rank, score, userName) {
  let rankOkMsg = MSG_OK_RANK;
  let rankNgMsg = MSG_ERR_RANK;

  const langCd = gameState.selectedLanguage;
  if (langCd === LANG_CD_KO) {
    rankOkMsg = MSG_OK_RANK_KO;
    rankNgMsg = MSG_ERR_RANK_KO;
  } else if (langCd === LANG_CD_EN) {
    rankOkMsg = MSG_OK_RANK_EN;
    rankNgMsg = MSG_ERR_RANK_EN;
  }

  let url = URL_QUIZ_RANKING_SERVER;
  if (isLocal()) {
    url = URL_QUIZ_RANKING_LOCAL;
  }

  const requestBody = { rank: rank, score: score, userName: userName };

  try {
    const data = await getFetchApiData(url, requestBody);
    console.log(data.message);
    alert(rankOkMsg);
  } catch (e) {
    alert(rankNgMsg);
  }

  // ページ全体をリセット（再読み込み）
  location.reload();
}

// ルールダイアログ表示
const showRuleDialog = () => {
  setElemText("rule-title", TITLE_GAME_RULES)
  setElemContents('rule-content', getLocalizedMessage('rule_content'));
  getElem(ID_RULE_DIALOG).showModal();
};

/**
 * ページロード時の初期化
 */
window.onload = () => {
  renderInitialScreen();
};