// --- ランキングダミーデータ (静的ランキングダミーデータ) ---
const staticRankings = [
  { username: "kobe", score: 100, date: "2025/10/01" },
  { username: "song", score: 90, date: "2025/10/02" },
  { username: "sera", score: 75, date: "2025/10/03" },
  { username: "juni", score: 60, date: "2025/10/04" },
  { username: "hana", score: 55, date: "2025/10/05" },
];

// ランキングデータをソートして取得する関数
function loadRankings() {
  // スコアが高い順にソート
  const sortedRankings = [...staticRankings].sort((a, b) => b.score - a.score);
  return sortedRankings;
}
window.loadRankings = loadRankings;

// ユーザーIDを取得するダミー関数
function getUserId() {
  return 'Cute_User_ID_0000';
}
window.getUserId = getUserId;

// --- クイズデータ (Quiz Data) ---
const quizData = [
  { id: 1, word: "GEMINI", description_kr: "구글에서 만든 AI모델로, 텍스트와 이미지 생성이 가능해요.", description_jp: "Googleが開発したAIモデル。テキストや画像を生成可能。", description_en: "AI model by Google, generating text and images." },
  { id: 2, word: "HTML", description_kr: "웹페이지의 뼈대를 만드는 데 사용하는 언어예요.", description_jp: "ウェブページの骨格を作成するために使う言語。", description_en: "Language used to create the structure of a webpage." },
  { id: 3, word: "CSS", description_kr: "웹페이지의 색깔이나 디자인을 꾸밀 때 사용해요.", description_jp: "ウェブページの色やデザインを装飾する際に使用。", description_en: "Used to style the colors and design of a webpage." },
  { id: 4, word: "FIREWALL", description_kr: "외부의 나쁜 침입을 막아주는 보안 장치예요.", description_jp: "外部からの不正侵入を防ぐためのセキュリティ装置。", description_en: "A security device that blocks harmful external intrusions." },
  { id: 5, word: "COOKIE", description_kr: "웹사이트가 사용자 정보를 잠시 저장하는 작은 파일이에요.", description_jp: "ウェブサイトがユーザー情報を一時的に保存する小さなファイル。", description_en: "A small file where a website stores user information temporarily." },
  { id: 6, word: "CLOUD", description_kr: "인터넷으로 파일을 저장하고 프로그램을 쓰는 기술이에요.", description_jp: "インターネット経由でファイルを保存し、プログラムを使う技術。", description_en: "Technology for storing files and using programs via the internet." },
  { id: 7, word: "API", description_kr: "서로 다른 프로그램이 정보를 주고받게 연결해 줘요.", description_jp: "異なるプログラム同士が情報をやり取りできるように繋ぐもの。", description_en: "Connects different programs to exchange information." },
  { id: 8, word: "SQL", description_kr: "데이터베이스에서 정보를 찾거나 관리하는 언어예요.", description_jp: "データベースから情報を検索・管理するための言語。", description_en: "Language for finding and managing information in a database." },
  { id: 9, word: "AI", description_kr: "사람처럼 생각하고 배우는 컴퓨터 기술을 말해요.", description_jp: "人のように考え学習するコンピューター技術。", description_en: "Computer technology that thinks and learns like a human." },
  { id: 10, word: "IP ADDRESS", description_kr: "인터넷에 연결된 기기마다 있는 고유한 주소예요.", description_jp: "インターネットに接続された機器それぞれが持つ固有のアドレス。", description_en: "A unique address for every device connected to the internet." }
];

// --- グローバルゲーム状態管理オブジェクト (Global game state) ---
const gameState = {
  currentQuizIndex: 0, // 現在のクイズ番号
  score: 0,           // 現在のスコア
  currentWord: [],    // 現在の単語の解答状況 (例: ['G', '_', 'M', '_'])
  timer: null,        // タイマーID
  timeRemaining: 0,   // 残り時間（秒）
  initialTime: 0,     // クイズ開始時の初期時間
  quizSet: [],        // 今回のゲームで使用するクイズセット
  hintsUsed: 0,       // 使用したヒントの数
  selectedLanguage: 'ko', // 選択された言語
  isAuthReady: true,  // 認証準備完了フラグ (ダミー)
};
window.gameState = gameState;

// テキストマッピングオブジェクト (言語別テキスト)
const textMap = {
  'ko': {
    title: "IT 상식 퀴즈", rankingTitle: "TOP 5 랭킹", user: "유저명", score: "점수", status: "퀴즈상황",
    rules: "게임 규칙", hint: "힌트 사용 (-1점)", check: "정답 확인", quizDescTitle: "퀴즈 설명",
    placeholder: "빈 칸을 눌러 글자를 선택하고, 모두 채운 후 정답 확인 버튼을 누르세요.",
    noRanking: "아직 랭킹 데이터가 없어요.", sec: "초", point: "점", ok: "확인"
  },
  'jp': {
    title: "IT常識クイズ", rankingTitle: "TOP 5 ランキング", user: "ユーザー名", score: "スコア", status: "クイズ状況",
    rules: "ゲームのルール", hint: "ヒントを使う (-1点)", check: "正解を確認", quizDescTitle: "クイズの説明",
    placeholder: "空欄をタップして文字を選択し、全て埋めたら正解確認ボタンを押してください。",
    noRanking: "まだランキングデータはありません。", sec: "秒", point: "点", ok: "OK"
  },
  'en': {
    title: "IT Common Sense Quiz", rankingTitle: "TOP 5 Ranking", user: "User", score: "Score", status: "Quiz Status",
    rules: "Game Rules", hint: "Use Hint (-1 point)", check: "Check Answer", quizDescTitle: "Quiz Description",
    placeholder: "Tap the empty space to select a letter, then check the answer.",
    noRanking: "No ranking data yet.", sec: "sec", point: "points", ok: "OK"
  }
};

// ダイアログおよび動的メッセージマッピング
const msgMap = {
  'time_over_title': { 'ko': '시간 초과', 'jp': '時間切れ', 'en': 'Time Over' },
  'time_over_msg': { 'ko': '시간이 다 되었어요. 다음 문제로 넘어갑니다.', 'jp': '時間が終了しました。次の問題に進みます。', 'en': 'Time is up. Moving to the next quiz.' },

  'correct_10_title': (time, lang) => {
    const t = textMap[lang];
    return `정답! (+10${t.point})`;
  },
  'correct_10_msg': (time, lang) => {
    const t = textMap[lang];
    return `${time}${t.sec} 이내 정답! +10${t.point}을 획득했어요!`;
  },

  'correct_5_title': { 'ko': '정답! (+5점)', 'jp': '正解! (+5点)', 'en': 'Correct! (+5 Points)' },
  'correct_5_msg': { 'ko': '+5점을 획득했어요!', 'jp': '+5点を獲得しました!', 'en': 'You got +5 points!' },

  'game_over_title': { 'ko': '게임 종료!', 'jp': 'ゲーム終了!', 'en': 'GAME OVER!' },
  'game_over_msg': (score, lang) => {
    const t = textMap[lang];
    return `${t.score}: ${score}${t.point} 입니다! 수고하셨어요.`;
  },

  'no_hints_title': { 'ko': '힌트 없음', 'jp': 'ヒントなし', 'en': 'No Hints' },
  'no_hints_all_revealed_msg': { 'ko': '모든 글자가 공개되었어요.', 'jp': '全ての文字が公開されました。', 'en': 'All letters are revealed.' },
  'no_hints_max_used_msg': { 'ko': '더 이상 힌트를 사용할 수 없어요.', 'jp': 'これ以上ヒントは使えません。', 'en': 'No more hints available.' },

  'hint_revealed_title': { 'ko': '힌트 사용 (-1점)', 'jp': 'ヒント使用 (-1点)', 'en': 'Hint Used (-1 Point)' },
  'hint_revealed_msg': { 'ko': '단어의 한 글자가 공개되었고, 점수 -1점 처리되었습니다.', 'jp': '単語の文字が一つ公開され、スコアから-1点が引かれました。', 'en': 'A letter has been revealed, and 1 point has been deducted.' },

  'select_letter_title': { 'ko': '글자 선택', 'jp': '文字選択', 'en': 'Select Letter' },
  'select_letter_msg': { 'ko': '이 칸에 들어갈 글자를 5개의 후보 중 골라보세요!', 'jp': 'この欄に入る文字を5つの候補から選んでください!', 'en': 'Choose the letter for this space from 5 candidates!' },

  'incorrect_title': { 'ko': '❌ 아쉽네요! (-1점)', 'jp': '❌ 残念! (-1点)', 'en': '❌ Oops! (-1 Point)' },
  'incorrect_msg': { 'ko': '선택이 틀렸어요. 점수 -1점. 다시 시도해 보세요.', 'jp': '選択が間違っています。スコア -1点。再試行してください。', 'en': 'Incorrect selection. Score -1 point. Please try again.' },

  'incomplete_title': { 'ko': '미완성', 'jp': '未完成', 'en': 'Incomplete' },
  'incomplete_msg': { 'ko': '아직 단어가 완성되지 않았어요. 빈 칸을 눌러 글자를 채워주세요.', 'jp': 'まだ単語が完成していません。空欄をタップして文字を埋めてください。', 'en': 'The word is not complete. Tap the empty spaces.' },

  'rules_title': { 'ko': '게임 규칙', 'jp': 'ゲームのルール', 'en': 'Game Rules' },
  'rules_msg': (wordLength, lang) => {
    const t = textMap[lang];
    const initialTime = wordLength * 10;
    const thresholdTime = initialTime / 2;
    return `
            <p class="mb-2" style="color: var(--text-color-dark);">1. 10개의 퀴즈를 풀어요. 문제당 글자 수 $\\times 10$초가 주어져요. (예: 6글자 단어 $\\to$ ${initialTime}${t.sec})</p>
            <p class="mb-2" style="color: var(--text-color-dark);">2. **${thresholdTime}${t.sec} 이내** 정답: **+10${t.point}**, 그 외 정답: **+5${t.point}**</p>
            <p class="mb-2" style="color: var(--text-color-dark);">3. 글자 선택 오답 시: **-1${t.point}** (최소 점수는 0점)</p>
            <p class="mb-2" style="color: var(--text-color-dark);">4. 힌트: '힌트 사용' 버튼을 누르면 한 글자씩 공개되며, **-1${t.point}** 차감됩니다. (최대 글자 수 -1)</p>
            <p style="color: var(--text-color-dark);">5. 단어의 빈 칸을 눌러 5개의 후보 중 정답 글자를 선택합니다.</p>
        `;
  },
};

/**
 * @brief ローカライズされたメッセージを取得する
 * @param {string} key - メッセージキー
 * @param {any} data - メッセージ関数に渡すデータ (スコアや文字長など)
 * @returns {string} ローカライズされたメッセージ
 */
function getLocalizedMessage(key, data) {
  const lang = gameState.selectedLanguage;
  const message = msgMap[key];
  if (typeof message === 'function') {
    // 関数型メッセージの場合、データと言語コードを渡して実行
    return message(data, lang);
  }
  // 通常のオブジェクトの場合、該当言語、または英語で代用
  return message[lang] || message['en'];
}

/**
 * @brief スペースを除いた現在のクイズの単語の長さを取得する
 * @returns {number} 単語の有効な文字数
 */
function getCurrentWordLength() {
  if (!gameState.quizSet.length) return 0;
  const currentQuiz = gameState.quizSet[gameState.currentQuizIndex];
  if (!currentQuiz) return 0;
  // スペースを除外した文字数
  return currentQuiz.word.toUpperCase().replace(/ /g, '').length;
}

// --- ダイアログユーティリティ関数 (Dialog Utility Functions) ---
/**
 * @brief カスタムボタン付きのモーダルダイアログを表示する
 */
function showDialog(title, message, onClose, customButtonsHtml) {
  const t = textMap[gameState.selectedLanguage] || textMap['ko'];

  document.getElementById('dialog-title').textContent = title;
  document.getElementById('dialog-message').innerHTML = message;

  const dialogButtons = document.getElementById('dialog-buttons');
  dialogButtons.innerHTML = '';

  if (customButtonsHtml) {
    dialogButtons.innerHTML = customButtonsHtml;
  } else {
    const closeBtn = document.createElement('button');
    // モーダル内でボタン幅がautoになるように調整
    closeBtn.className = 'cute-button px-4 py-2 text-sm gray';
    closeBtn.style.width = 'auto';
    closeBtn.textContent = t.ok;
    closeBtn.onclick = () => {
      closeDialog();
      if (onClose) onClose();
    };
    dialogButtons.appendChild(closeBtn);
  }

  document.getElementById('dialog-overlay').classList.remove('hidden');
}

/**
 * @brief モーダルダイアログを閉じる
 */
function closeDialog() {
  document.getElementById('dialog-overlay').classList.add('hidden');
  document.getElementById('dialog-buttons').innerHTML = '';
}

// --- ゲームフロー関数 (Game Flow Functions) ---
/**
 * @brief ゲームを初期化する
 */
function initializeGame() {
  // クイズデータをシャッフルして10問選択
  gameState.quizSet = [...quizData].sort(() => 0.5 - Math.random()).slice(0, 10);
  gameState.currentQuizIndex = 0;
  gameState.score = 0;
  loadQuiz(gameState.currentQuizIndex);
}

/**
 * @brief クイズを読み込む (時間設定を含む)
 * @param {number} index - ロードするクイズのインデックス
 */
function loadQuiz(index) {
  if (index >= gameState.quizSet.length) {
    endGame();
    return;
  }

  const currentQuiz = gameState.quizSet[index];
  const word = currentQuiz.word.toUpperCase();
  const wordLength = getCurrentWordLength();

  // 新しい時間設定ロジック: 文字数 * 10秒
  gameState.initialTime = wordLength * 10;
  gameState.timeRemaining = gameState.initialTime;

  // 現在の単語の状態を初期化
  gameState.currentWord = Array(word.length).fill('_');
  gameState.hintsUsed = 0;

  // 最初の有効な文字を自動で公開する (空白でない最初の文字)
  if (word.length > 2) {
    let firstCharIndex = -1;
    for (let i = 0; i < word.length; i++) {
      if (word[i] !== ' ') {
        firstCharIndex = i;
        break;
      }
    }
    if (firstCharIndex !== -1) {
      gameState.currentWord[firstCharIndex] = word[firstCharIndex];
    }
  }

  renderGameScreen();
  startTimer();
}

/**
  * @brief タイマーを開始する
  */
function startTimer() {
  if (gameState.timer) clearInterval(gameState.timer);
  const t = textMap[gameState.selectedLanguage] || textMap['ko'];

  gameState.timer = setInterval(() => {
    gameState.timeRemaining--;
    const timerDisplay = document.getElementById('timer-display');
    if (timerDisplay) {
      timerDisplay.textContent = `${gameState.timeRemaining}${t.sec}`;
    }

    // 時間切れの場合
    if (gameState.timeRemaining <= 0) {
      clearInterval(gameState.timer);
      showDialog(
        getLocalizedMessage('time_over_title'),
        getLocalizedMessage('time_over_msg'),
        () => goToNextQuiz()
      );
    }
  }, 1000);
}

/**
  * @brief 次のクイズへ進む
  */
function goToNextQuiz() {
  gameState.currentQuizIndex++;
  loadQuiz(gameState.currentQuizIndex);
}

/**
  * @brief 正解時の処理 (得点ロジック更新)
  */
function handleCorrectAnswer() {
  clearInterval(gameState.timer);
  const t = textMap[gameState.selectedLanguage] || textMap['ko'];

  const initialTime = gameState.initialTime;
  const thresholdTime = initialTime / 2; // 基準時間
  const elapsedTime = initialTime - gameState.timeRemaining; // 経過時間

  let points = 0;
  let titleKey, msgKey;
  let msgData = null;

  if (elapsedTime <= thresholdTime) {
    // 基準時間(initialTime / 2)以内に正解 -> +10点
    points = 10;
    titleKey = 'correct_10_title';
    msgKey = 'correct_10_msg';
    msgData = thresholdTime; // メッセージに関数を渡す
  } else {
    // 基準時間超過後に正解 -> +5点
    points = 5;
    titleKey = 'correct_5_title';
    msgKey = 'correct_5_msg';
  }

  gameState.score += points;
  const scoreDisplay = document.getElementById('score-display');
  if (scoreDisplay) {
    scoreDisplay.textContent = `${gameState.score} ${t.point}`;
  }

  // ローカライズされたタイトルとメッセージを動的に取得
  showDialog(
    getLocalizedMessage(titleKey, msgData),
    getLocalizedMessage(msgKey, msgData),
    () => goToNextQuiz()
  );
}

/**
  * @brief ゲームを終了する
  */
function endGame() {
  clearInterval(gameState.timer);

  gameState.score = Math.max(0, gameState.score); // スコアがマイナスにならないように

  showDialog(
    getLocalizedMessage('game_over_title'),
    getLocalizedMessage('game_over_msg', gameState.score),
    () => {
      closeDialog();
      renderInitialScreen(); // 初期画面に戻る
    }
  );
}

// --- ゲーム内アクション関数 (In-Game Action Functions) ---
/**
  * @brief ヒントを使用する (ペナルティ -1点)
  */
function useHint() {
  const currentQuiz = gameState.quizSet[gameState.currentQuizIndex];
  const word = currentQuiz.word.toUpperCase();

  const maxHints = word.replace(/ /g, '').length - 1; // 最初の文字公開分を除いた最大ヒント数
  const currentReveals = gameState.currentWord.filter(c => c !== '_' && c !== ' ').length;

  if (currentReveals >= word.replace(/ /g, '').length) {
    // すでに全文字公開済み
    showDialog(getLocalizedMessage('no_hints_title'), getLocalizedMessage('no_hints_all_revealed_msg'), () => closeDialog());
    return;
  }
  if (gameState.hintsUsed >= maxHints) {
    // 最大ヒント数に達した
    showDialog(getLocalizedMessage('no_hints_title'), getLocalizedMessage('no_hints_max_used_msg'), () => closeDialog());
    return;
  }

  // ペナルティロジック: スコア -1点
  gameState.score = Math.max(0, gameState.score - 1);
  const t = textMap[gameState.selectedLanguage] || textMap['ko'];
  const scoreDisplay = document.getElementById('score-display');
  if (scoreDisplay) {
    scoreDisplay.textContent = `${gameState.score} ${t.point}`;
  }

  // マスクされているインデックスを収集
  let maskedIndices = [];
  for (let i = 0; i < gameState.currentWord.length; i++) {
    if (gameState.currentWord[i] === '_') {
      maskedIndices.push(i);
    }
  }

  if (maskedIndices.length === 0) { return; }

  // ランダムに一つのマスクを解除
  const randomIndex = maskedIndices[Math.floor(Math.random() * maskedIndices.length)];
  gameState.currentWord[randomIndex] = word[randomIndex];
  gameState.hintsUsed++;

  renderQuizWord();

  showDialog(getLocalizedMessage('hint_revealed_title'), getLocalizedMessage('hint_revealed_msg'), () => closeDialog());
}

/**
  * @brief 未公開文字クリック処理 (文字選択ダイアログ表示) - 文字タイプ一致ロジックを含む
  * @param {number} index - クリックされた単語のインデックス
  */
function handleLetterClick(index) {
  const currentQuiz = gameState.quizSet[gameState.currentQuizIndex];
  const word = currentQuiz.word.toUpperCase();

  if (gameState.currentWord[index] !== '_') {
    return; // 既に公開されている文字は無視
  }

  const correctLetter = word[index];
  let possibleCharsPool = []; // 候補を取得するための文字プール

  // 1. 正解文字のタイプ確認とプール設定
  if (/[A-Z]/.test(correctLetter)) {
    // 英語大文字の場合: アルファベットプールを使用
    possibleCharsPool = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split('');
  } else if (/[0-9]/.test(correctLetter)) {
    // 数字の場合: 数字プールを使用
    possibleCharsPool = "0123456789".split('');
  } else {
    // その他の文字（スペースなど）はクリック対象外
    return;
  }

  let candidates = new Set();
  candidates.add(correctLetter); // 2. 正解文字を必ず含める

  // 正解文字をプールから一時的に除外し、重複しない誤答を選択できるようにする
  let filteredPool = possibleCharsPool.filter(char => char !== correctLetter);

  // 3. 4つの誤答候補を生成 (合計5つの候補)
  while (candidates.size < 5 && filteredPool.length > 0) {
    const randomIndex = Math.floor(Math.random() * filteredPool.length);
    // 選択された誤答をプールから削除し (splice)、候補に追加
    const randomLetter = filteredPool.splice(randomIndex, 1)[0];
    candidates.add(randomLetter);
  }

  // 候補をランダムに並び替える
  const candidateArray = Array.from(candidates).sort(() => 0.5 - Math.random());

  // ダイアログ内のボタンHTMLを生成
  const buttonsHtml = candidateArray.map(letter =>
    `<button class="cute-button px-4 py-2 text-xl bg-pink-300 hover:bg-pink-400 text-white" 
                  style="width: 45%; margin: 0.5rem 0;" 
                  onclick="selectCandidate('${letter}', ${index})">
            ${letter}
        </button>`
  ).join('');

  showDialog(
    getLocalizedMessage('select_letter_title'),
    getLocalizedMessage('select_letter_msg'),
    null,
    `<div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 0.5rem;">${buttonsHtml}</div>`
  );
}

/**
  * @brief 文字選択ダイアログで候補文字が選択された時の処理
  * @param {string} selectedLetter - ユーザーが選択した文字
  * @param {number} index - 単語のインデックス
  */
function selectCandidate(selectedLetter, index) {
  const currentQuiz = gameState.quizSet[gameState.currentQuizIndex];
  const word = currentQuiz.word.toUpperCase();
  const correctLetter = word[index];

  closeDialog();

  if (selectedLetter === correctLetter) {
    // 正解の場合
    gameState.currentWord[index] = correctLetter;
    renderQuizWord();

    // 単語が完成したかチェック (スペースを除いて比較)
    if (gameState.currentWord.join('').replace(/ /g, '') === word.replace(/ /g, '')) {
      handleCorrectAnswer();
    }

  } else {
    // 不正解の場合: 1点減点 (ペナルティ -1点)
    gameState.score = Math.max(0, gameState.score - 1);
    const t = textMap[gameState.selectedLanguage] || textMap['ko'];
    const scoreDisplay = document.getElementById('score-display');
    if (scoreDisplay) {
      scoreDisplay.textContent = `${gameState.score} ${t.point}`;
    }

    showDialog(
      getLocalizedMessage('incorrect_title'),
      getLocalizedMessage('incorrect_msg'),
      () => closeDialog()
    );
  }
}

/**
  * @brief 答えを確認する
  */
function checkAnswer() {
  const currentQuiz = gameState.quizSet[gameState.currentQuizIndex];
  const word = currentQuiz.word.toUpperCase();

  const currentGuess = gameState.currentWord.join('');

  // スペースを除いて比較
  if (currentGuess.replace(/ /g, '') === word.replace(/ /g, '')) {
    handleCorrectAnswer();
  } else {
    showDialog(getLocalizedMessage('incomplete_title'), getLocalizedMessage('incomplete_msg'), () => closeDialog());
  }
}

/**
  * @brief ゲームルールを表示する
  */
function showRules() {
  const wordLength = getCurrentWordLength();
  showDialog(getLocalizedMessage('rules_title'), getLocalizedMessage('rules_msg', wordLength));
}

// --- UIレンダリング関数 (UI Rendering Functions) ---
/**
  * @brief 初期画面をレンダリングする (言語選択・ランキング表示)
  */
async function renderInitialScreen() {

  const rankings = loadRankings();
  const t = textMap[gameState.selectedLanguage] || textMap['ko'];

  // ランキングリストのHTMLを生成
  const rankingHtml = rankings.length > 0 ? rankings.map((r, i) => `
        <li style="display: flex; justify-content: space-between; font-size: 0.875rem; padding-top: 0.25rem; padding-bottom: 0.25rem; border-bottom: 1px solid #f3f4f6;">
            <span class="text-accent" style="width: 1.5rem; text-align: center; font-weight: bold;">${i + 1}</span>
            <span style="color: var(--text-color-dark); flex: 1 1 0%;">${r.username}</span>
            <span style="color: var(--main-blue); font-weight: bold; width: 4rem; text-align: right;">${r.score}</span>
        </li>
    `).join('') : `<li style="text-align: center; font-size: 0.875rem; padding-top: 1rem; padding-bottom: 1rem; color: var(--text-color-light);">${t.noRanking}</li>`;

  // HTMLコンテンツを構築
  const html = `
        <div class="fade-in" style="margin-top: 0.5rem;">
            <h1 style="font-size: 1.875rem; text-align: center; color: var(--main-pink); font-weight: bold; border-bottom: 2px solid var(--main-blue); padding-bottom: 1rem; margin-bottom: 1.5rem;">
                ${t.title}
            </h1>

            <!-- 言語選択 -->
            <div style="padding: 1rem; background-color: #f9fafb; border-radius: 0.75rem; margin-bottom: 1.5rem;">
                <h2 style="font-size: 1.125rem; text-align: center; margin-bottom: 1rem; font-weight: bold; color: var(--main-blue);">${t.rules}</h2>
                <div style="display: flex; flex-direction: column; justify-content: center; gap: 0.75rem;">
                    <!-- ボタンの幅をモバイルでも対応できるように調整 -->
                    <button class="cute-button" style="font-size: 1rem; background-color: var(--main-blue);" onclick="setLanguage('jp')">日本語</button>
                    <button class="cute-button" style="font-size: 1rem; background-color: var(--main-blue);" onclick="setLanguage('ko')">한국어</button>
                    <button class="cute-button" style="font-size: 1rem; background-color: var(--main-blue);" onclick="setLanguage('en')">English</button>
                </div>
            </div>

            <!-- ランキング表示 (静的データ) -->
            <div style="padding: 1.5rem; background-color: #f9fafb; border-radius: 0.75rem; border: 2px solid var(--main-pink); box-shadow: inset 0 2px 4px 0 rgba(0, 0, 0, 0.06);">
                <h2 style="font-size: 1.25rem; text-align: center; margin-bottom: 1rem; font-weight: bold; color: var(--main-pink);">${t.rankingTitle}</h2>
                <ul style="list-style: none; padding: 0; margin: 0; margin-top: 0.25rem;">
                    ${rankingHtml}
                </ul>
            </div>
            
            <p style="text-align: center; font-size: 0.875rem; margin-top: 1.5rem; color: var(--text-color-light);">
                (원하는 언어를 선택하면 바로 게임이 시작됩니다!)
            </p>
        </div>
    `;
  document.getElementById('app').innerHTML = html;
}

/**
  * @brief 言語を設定してゲームを開始する
  * @param {string} lang - 選択された言語コード
  */
function setLanguage(lang) {
  gameState.selectedLanguage = lang;
  initializeGame();
}

/**
  * @brief クイズの単語部分をレンダリングする
  */
function renderQuizWord() {
  const wordContainerWrapper = document.getElementById('quiz-word-container-wrapper');
  if (!wordContainerWrapper) return;

  // コンテナがなければ作成（レスポンシブ対応のためラッパー構造を使用）
  let wordContainer = document.getElementById('quiz-word-container');
  if (!wordContainer) {
    wordContainer = document.createElement('div');
    wordContainer.id = 'quiz-word-container';
    wordContainerWrapper.appendChild(wordContainer);
  }

  const word = gameState.quizSet[gameState.currentQuizIndex].word.toUpperCase();

  let html = '';

  for (let i = 0; i < word.length; i++) {
    const char = word[i];
    if (char === ' ') {
      // スペースは空白として表示
      html += `<span style="display: inline-block; width: 1rem; margin-left: 0.5rem; margin-right: 0.5rem; flex-shrink: 0;"></span>`;
    } else {
      const displayChar = gameState.currentWord[i];
      const isMasked = displayChar === '_';

      if (isMasked) {
        // 未公開の文字
        html += `
                    <span class="masked-letter" data-index="${i}" 
                          onclick="handleLetterClick(${i})">
                        ${displayChar}
                    </span>`;
      } else {
        // 公開済みの文字
        html += `
                    <span class="filled-letter" data-index="${i}">
                        ${displayChar}
                    </span>`;
      }
    }
  }

  wordContainer.innerHTML = html;
}

/**
  * @brief ゲーム画面をレンダリングする
  */
function renderGameScreen() {
  const currentQuiz = gameState.quizSet[gameState.currentQuizIndex];
  const t = textMap[gameState.selectedLanguage] || textMap['ko'];

  // 選択された言語の説明を取得
  const description = currentQuiz[`description_${gameState.selectedLanguage}`] || currentQuiz.description_kr;

  const currentUserId = getUserId();

  // HTMLコンテンツを構築
  const html = `
        <div class="fade-in" style="margin-top: 0.5rem;">
            <!-- タイトル、スコア、状況表示エリア -->
            <header style="display: flex; flex-direction: column; justify-content: space-between; align-items: flex-start; margin-bottom: 1.5rem; border-bottom: 2px solid var(--main-pink); padding-bottom: 0.75rem;">
                <h1 style="font-size: 1.5rem; color: var(--main-pink); font-weight: bold; margin-bottom: 0.5rem;">${t.title}</h1>
                <div style="display: flex; flex-wrap: wrap; gap: 0 1.5rem; row-gap: 0.5rem; text-align: right; font-size: 0.875rem; color: var(--text-color-light); width: 100%; justify-content: space-between;">
                    <span>${t.user}: <span id="user-display" class="text-accent">${currentUserId}</span></span>
                    <span>${t.score}: <span id="score-display" class="text-accent font-bold">${gameState.score} ${t.point}</span></span>
                    <span>${t.status}: <span id="status-display" class="text-accent font-bold">${gameState.currentQuizIndex + 1} / ${gameState.quizSet.length}</span></span>
                </div>
            </header>
            <!-- デスクトップ用レイアウト調整 -->
            <style>
                @media (min-width: 640px) {
                    header {
                        flex-direction: row;
                        align-items: center;
                    }
                    header h1 {
                        font-size: 1.875rem;
                        margin-bottom: 0;
                    }
                    header div {
                        width: auto;
                    }
                }
            </style>

            <!-- ゲームルールボタンとタイマー -->
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                <button class="cute-button px-4 py-2 text-sm gray" style="width: auto;" onclick="showRules()">
                    ${t.rules}
                </button>
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="font-size: 1rem; color: var(--text-color-light);">Time:</span>
                    <div id="timer-display" style="font-size: 1.5rem; font-weight: bold; color: var(--main-blue);">
                        ${gameState.timeRemaining}${t.sec}
                    </div>
                </div>
            </div>

            <!-- クイズ表示エリア -->
            <div style="padding: 1rem; background-color: #f9fafb; border-radius: 0.75rem; border: 2px solid var(--main-blue); box-shadow: inset 0 2px 4px 0 rgba(0, 0, 0, 0.06);">
                <h2 style="text-align: center; font-size: 1rem; margin-bottom: 0.75rem; font-weight: bold; color: var(--main-pink);">${t.quizDescTitle}</h2>
                <p class="quiz-description-text" style="text-align: center; font-size: 1.125rem; margin-bottom: 1.5rem; color: var(--text-color-dark); min-height: 48px; display: flex; align-items: center; justify-content: center; border-bottom: 1px solid #e5e7eb; padding-bottom: 0.75rem; padding-top: 0.75rem;">
                    ${description}
                </p>

                <div id="quiz-word-container-wrapper" style="margin-top: 2rem; margin-bottom: 2rem; padding: 1rem; background-color: white; border-radius: 0.75rem; border: 1px solid #e5e7eb;">
                    <!-- クイズの単語がここに描画されます (renderQuizWord関数) -->
                </div>

                <!-- 힌트ボタンおよび正解確認ボタン -->
                <div style="display: flex; flex-direction: column; justify-content: center; gap: 1rem; margin-top: 1.5rem;">
                    <!-- ボタンの幅はデフォルトで 100% -->
                    <button class="cute-button" style="font-size: 1.125rem; background-color: var(--main-blue);" onclick="useHint()">
                        ${t.hint}
                    </button>
                    <button class="cute-button" style="font-size: 1.125rem; background-color: var(--main-pink);" onclick="checkAnswer()">
                        ${t.check}
                    </button>
                </div>
                <p style="text-align: center; font-size: 0.75rem; margin-top: 0.75rem; color: var(--text-color-light);">
                    ${t.placeholder}
                </p>
            </div>
        </div>
    `;
  document.getElementById('app').innerHTML = html;
  renderQuizWord(); // 単語部分をレンダリング
}

// ページロード時に初期画面をレンダリング
window.onload = () => {
  renderInitialScreen();
};

// グローバル公開関数
window.initializeGame = initializeGame;
window.renderInitialScreen = renderInitialScreen;
window.setLanguage = setLanguage;
window.handleLetterClick = handleLetterClick;
window.selectCandidate = selectCandidate;
window.useHint = useHint;
window.checkAnswer = checkAnswer;
window.showRules = showRules;
window.showDialog = showDialog;
window.closeDialog = closeDialog;
