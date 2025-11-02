// タイトル設定
document.title = TITLE_SUDOKU;

/**
 * ゲーム設定定数
 */
// ゲーム制限時間（秒）
const GAME_TIMEOUT_SECONDS = 1200;

// 不正解時のペナルティ時間（秒）
const PENALTY_SECONDS = 60;

// 初期ヒント数
const INITIAL_HINTS = 3;

// 空けるマス数（レベル）
const HOLES_MEDIUM = 50;

/**
 * グローバルな状態変数
 */
let currentScreen = 'start';
let timer;
let timeRemaining = GAME_TIMEOUT_SECONDS;
let hintsLeft = INITIAL_HINTS;
let selectedCell = null;

// ユーザー入力を含む現在の盤面
let puzzle = [];

// 正しい解答
let solution = [];

// 固定マス（変更不可）
let initialPuzzle = [];

// ユーザー名
let userName = SYM_BLANK;

// ランキングデータ // TODO: data_listに相当）
const RANKING_DATA = [
  { name: "Neo", time: "05:30", date: "2025/10/28" },
  { name: "Trinity", time: "07:15", date: "2025/10/29" },
  { name: "Morpheus", time: "08:00", date: "2025/10/29" },
  { name: "Agent Smith", time: "10:20", date: "2025/10/30" },
  { name: "Oracle", time: "12:45", date: "2025/10/31" },
];

// 言語別ルールテキスト
const GAME_RULES = {
  ja: {
    title: "ゲーム ルール",
    body: `ナンプレ（数独）は、9×9のマス目に1から9までの数字を入れるパズルです。\n
    \n1. 横（行）・縦（列）に1から9までの数字が一つずつ入る。
    \n2. 9つの3×3のブロックそれぞれに1から9までの数字が一つずつ入る。
    \n3. 空のマスをタップし、表示された数字を入力できる。
    \n4. 間違える度に残り時間が1分短縮される。
    \n5. 20分のタイムアウトまでに全てのマスを埋める。`
  },
  ko: {
    title: "게임 규칙",
    body: `스도쿠는 9x9 칸에 1부터 9까지의 숫자를 채워 넣는 퍼즐입니다.\n
    \n1. 가로줄・세로줄에 1부터 9까지의 숫자가 한 번씩만 들어갑니다.
    \n2. 9개의 3x3 블록 각각에 1부터 9까지의 숫자가 한 번씩만 들어갑니다。
    \n3. 빈 칸을 탭하고 나타나는 숫자 패드로 숫자를 입력하세요. 
    \n4. 틀릴 때마다 남은 시간이 1분씩 줄어듭니다.
    \n5. 20분 시간 초과 전에 모든 칸을 채우세요.`
  },
  en: {
    title: "GAME RULES",
    body: `Sudoku is a puzzle where you must fill a 9x9 grid with 1 to 9.\n
    \n1. Every row＆column must contain the numbers 1-9 exactly once.
    \n2. Every 3x3 grid must contain the numbers 1-9 exactly once.
    \n3. Tap an empty cell and use the keypad to enter a number. 
    \n4. Each incorrect entry deducts 1 minute from your remaining time.
    \n5. Complete the grid before the 20-minute timeout.`
  }
};

// DOM要素の取得
let startScreen, gameScreen, levelSelect, languageSelect, userNameInput, startButton;
let rankTbody, gameInfoHeader, timerText, progressBar, sudokuBoard, inputPanel;
let ruleButton, hintButton, homeButton, hintCounter, modalOverlay, modalTitle, modalBody, modalCloseButton;


// 画面切り替え関数
function showScreen(screenId) {
  if (startScreen) startScreen.style.display = 'none';
  if (gameScreen) gameScreen.style.display = 'none';
  // flexに設定することで中央揃えを維持
  const targetScreen = getElem(screenId);
  if (targetScreen) {
    targetScreen.style.display = 'flex';
    currentScreen = screenId.replace('-screen', '');
    if (currentScreen === 'start') {
      clearInterval(timer);
    }
  }
}

// 時間表示をMM:SS形式に変換
function formatTime(seconds) {
  const minutes = Math.floor(seconds / 60);
  const secs = seconds % 60;
  const timeDisplay = `${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`
  return timeDisplay;
}

// ランキングデータを表示
function renderRank() {
  if (!rankTbody) return;

  rankTbody.innerHTML = '';
  RANKING_DATA.forEach(rank => {
    const row = rankTbody.insertRow();
    row.innerHTML = `
      <td>${rank.name}</td>
      <td style="color: var(--color-neon-accent);">${rank.time}</td>
      <td>${rank.date}</td>
    `;
  });
}

// スタートボタンの有効/無効をチェック
function checkStartButtonState() {
  if (!userNameInput || !startButton) return;

  const name = userNameInput.value.trim();
  // ユーザー名が1文字以上10文字以下の場合のみ有効
  if (0 < name.length && name.length <= 10) {
    startButton.disabled = false;
  } else {
    startButton.disabled = true;
  }
}

// ゲームロジック（パズル生成・管理）
// 9x9の完成した数独の解
const SUDOKU_SOLUTION = [
  [5, 3, 4, 6, 7, 8, 9, 1, 2],
  [6, 7, 2, 1, 9, 5, 3, 4, 8],
  [1, 9, 8, 3, 4, 2, 5, 6, 7],
  [8, 5, 9, 7, 6, 1, 4, 2, 3],
  [4, 2, 6, 8, 5, 3, 7, 9, 1],
  [7, 1, 3, 9, 2, 4, 8, 5, 6],
  [9, 6, 1, 5, 3, 7, 2, 8, 4],
  [2, 8, 7, 4, 1, 9, 6, 3, 5],
  [3, 4, 5, 2, 8, 6, 1, 7, 9]
];

// 難易度に応じてマスを空ける（固定パズルから生成）
function generatePuzzle(level) {
  // 解答をコピー
  solution = SUDOKU_SOLUTION.map(row => [...row]);
  let initialBoard = solution.map(row => [...row]);

  let holes = 0;
  switch (level) {
    case LEVEL_EASY: holes = HOLES_MEDIUM - 10; break;
    case LEVEL_MEDIUM: holes = HOLES_MEDIUM; break;
    case LEVEL_HARD: holes = HOLES_MEDIUM + 10; break;
  }

  let attempts = 0;
  while (0 < holes && attempts < 200) {
    const r = Math.floor(Math.random() * 9);
    const c = Math.floor(Math.random() * 9);
    if (initialBoard[r][c] !== 0) {
      initialBoard[r][c] = 0;
      holes--;
    }
    attempts++;
  }

  // 初期設定
  puzzle = initialBoard.map(row => [...row]);
  initialPuzzle = initialBoard.map(row => [...row]);
}

// HTMLに描画
function renderBoard() {
  if (!sudokuBoard) return;

  sudokuBoard.innerHTML = '';
  for (let r = 0; r < 9; r++) {
    for (let c = 0; c < 9; c++) {
      const cell = document.createElement('div');
      cell.className = 'sudoku-cell';
      cell.dataset.row = r;
      cell.dataset.col = c;

      const value = puzzle[r][c];

      if (initialPuzzle[r][c] !== 0) {
        // 固定マス
        cell.classList.add('fixed-cell');
        cell.textContent = value;
      } else if (value !== 0) {
        // ユーザー入力マス
        cell.classList.add('user-input');
        cell.textContent = value;
        // エラーチェック
        if (!isValidInput(r, c, value)) {
          cell.classList.add('error');
        }
      }

      // クリックイベントリスナー
      cell.addEventListener("click", () => handleCellClick(cell));
      sudokuBoard.appendChild(cell);
    }
  }
}

// 特定のマスへの入力が有効かチェック (行、列、3x3ブロック)
function isValidInput(row, col, value) {
  // 行チェック
  for (let c = 0; c < 9; c++) {
    if (c !== col && puzzle[row][c] === value) return false;
  }

  // 列チェック
  for (let r = 0; r < 9; r++) {
    if (r !== row && puzzle[r][col] === value) return false;
  }

  // 3x3ブロックチェック
  const startRow = Math.floor(row / 3) * 3;
  const startCol = Math.floor(col / 3) * 3;
  for (let r = startRow; r < startRow + 3; r++) {
    for (let c = startCol; c < startCol + 3; c++) {
      if (r !== row && c !== col && puzzle[r][c] === value) return false;
    }
  }

  return true;
}

// 全てのマスが正しく埋まっているかチェック
function checkGameCompletion() {
  for (let r = 0; r < 9; r++) {
    for (let c = 0; c < 9; c++) {
      const value = puzzle[r][c];
      // 0（空き）がないか、または解と一致しないマスがある
      if (value === 0 || value !== solution[r][c]) {
        return false;
      }
    }
  }
  // 全てのマスが埋まり、全て解と一致した場合
  clearInterval(timer);
  const clearTime = "CLEAR TIME: \n" + formatTime(GAME_TIMEOUT_SECONDS - timeRemaining);
  showModal("COMPLETED！", clearTime);
  return true;
}

// セルがクリックされた時の処理
function handleCellClick(cell) {
  const r = parseInt(cell.dataset.row);
  const c = parseInt(cell.dataset.col);

  // 固定マスは操作不可
  if (initialPuzzle[r][c] !== 0) {
    if (inputPanel) inputPanel.style.display = 'none';
    return;
  }

  // 選択状態の更新
  if (selectedCell) {
    selectedCell.classList.remove('selected');
  }
  selectedCell = cell;
  selectedCell.classList.add('selected');

  // 入力パネルの表示
  if (inputPanel) inputPanel.style.display = 'grid';
}

// 入力パネルのボタンが押された時の処理
function handleInput(value) {
  if (!selectedCell) return;

  const r = parseInt(selectedCell.dataset.row);
  const c = parseInt(selectedCell.dataset.col);
  const num = parseInt(value);

  // 値の更新
  puzzle[r][c] = num;

  // 表示の更新
  selectedCell.textContent = num === 0 ? '' : num;
  selectedCell.classList.remove('user-input', 'error');

  if (num !== 0) {
    selectedCell.classList.add('user-input');

    // 正誤判定
    if (solution[r][c] === num) {
      // 正解
      selectedCell.classList.remove('error');
    } else {
      // 不正解 -> ペナルティ時間短縮
      selectedCell.classList.add('error');
      timeRemaining = Math.max(0, timeRemaining - PENALTY_SECONDS);
      updateTimer();
      showModal("INCORRECT", `INCORRECT！Minus ${PENALTY_SECONDS / 60}min.`);
    }
  }

  // 選択状態を解除し、入力パネルを非表示
  selectedCell.classList.remove('selected');
  selectedCell = null;
  if (inputPanel) inputPanel.style.display = 'none';

  // エラー状態をリセット/確認
  renderBoard();

  // ゲームクリアチェック
  checkGameCompletion();
}

// タイマーの開始
function startTimer() {
  // 既存のタイマーをクリア
  clearInterval(timer);
  timer = setInterval(updateTimer, 1000);
}

// タイマーを毎秒更新
function updateTimer() {
  if (!timerText || !progressBar) return;

  timeRemaining--;

  const timeDisplay = formatTime(timeRemaining);
  // GAME_TIMEOUT_SECONDS (MAX_TIME) を使用して進行状況を計算
  const progressPercentage = (timeRemaining / GAME_TIMEOUT_SECONDS) * 100;

  timerText.textContent = timeDisplay;
  progressBar.style.width = `${progressPercentage}%`;

  // タイムアウトチェック
  if (timeRemaining <= 0) {
    clearInterval(timer);
    timerText.textContent = "00:00 TIME OUT";
    showModal("TIME OUT", "TIME OVER !!");
    // すべての入力を無効化（固定マス化）
    initialPuzzle = solution.map(row => [...solution]);
    renderBoard();
  }

  // 時間残りわずかで警告色
  if (timeRemaining <= 60) {
    timerText.style.color = 'red';
    progressBar.style.backgroundColor = 'red';
  } else {
    timerText.style.color = 'cyan';
    progressBar.style.backgroundColor = 'cyan';
  }
}

// ベストタイムを取得
function getBestTime() {
  // ランキングデータの最も速いタイム
  return RANKING_DATA[0].time;
}

// ゲーム情報ヘッダーを更新
function updateGameInfoHeader(level, currentUserName) {
  if (!gameInfoHeader) return;

  const bestTime = getBestTime();

  const displayLevel = level.toUpperCase();

  gameInfoHeader.innerHTML = `
    <div>
      <span class="info-label">LEVEL:</span>
      <span class="info-value">${displayLevel}</span>
    </div>
    <div>
      <span class="info-label">BEST TIME:</span>
      <span class="info-value">${bestTime}</span>
    </div>
    <div>
      <span class="info-label">USER:</span>
      <span class="info-value">${currentUserName}</span>
    </div>
  `;
}

// ヒント処理
function useHint() {
  if (hintsLeft <= 0) {
    showModal("HINT FAILED", "NO HINT!!");
    return;
  }

  // まだ空いているマスをランダムに探す
  const emptyCells = [];
  for (let r = 0; r < 9; r++) {
    for (let c = 0; c < 9; c++) {
      if (puzzle[r][c] === 0) {
        emptyCells.push({ r, c });
      }
    }
  }

  if (emptyCells.length === 0) {
    showModal("HINT FAILED", "HINT FAILED！");
    return;
  }

  // ランダムに一つの空マスを選択
  const target = emptyCells[Math.floor(Math.random() * emptyCells.length)];
  const correctValue = solution[target.r][target.c];

  // 盤面を更新
  puzzle[target.r][target.c] = correctValue;
  hintsLeft--;
  if (hintCounter) hintCounter.textContent = hintsLeft;

  // 描画を更新し、ヒントとして入力されたセルをハイライト
  renderBoard();
  const cellElement = sudokuBoard ? sudokuBoard.querySelector(`[data-row="${target.r}"][data-col="${target.c}"]`) : null;
  if (cellElement) {
    cellElement.classList.add('fixed-cell');
    cellElement.textContent = correctValue;
    // 一時的なハイライト
    cellElement.style.boxShadow = '0 0 15px magenta';
    setTimeout(() => {
      cellElement.style.boxShadow = '';
    }, 1000);
  }

  showModal("HINT USED", `HINT LEFT: ${hintsLeft}`);

  // ゲームクリアチェック
  checkGameCompletion();
}

// モーダル表示
function showModal(title, body) {
  if (!modalOverlay || !modalTitle || !modalBody) return;

  modalTitle.textContent = title;
  modalBody.innerHTML = body.replace(/\n/g, '<br>');
  modalOverlay.style.display = 'flex';
}

// モーダル非表示
function hideModal() {
  if (modalOverlay) modalOverlay.style.display = 'none';
}

// ゲーム開始
function startGame() {
  if (!levelSelect || !languageSelect || !userNameInput) return;

  const level = levelSelect.value;

  // ユーザー名保存
  userName = userNameInput.value.trim();

  // 状態リセット
  timeRemaining = GAME_TIMEOUT_SECONDS;
  hintsLeft = INITIAL_HINTS;
  if (hintCounter) hintCounter.textContent = hintsLeft;

  // UIリセット
  if (timerText) timerText.textContent = formatTime(GAME_TIMEOUT_SECONDS);
  if (progressBar) {
    progressBar.style.width = '100%';
    progressBar.style.backgroundColor = 'cyan';
  }
  if (timerText) timerText.style.color = 'cyan';
  if (inputPanel) inputPanel.style.display = 'none';

  // パズル生成
  generatePuzzle(level);
  renderBoard();

  // ゲーム情報ヘッダーを更新
  updateGameInfoHeader(level, userName);

  // 画面遷移とタイマー開始
  showScreen('game-screen');
  startTimer();
}

// 初期化（DOM 要素の取得）
function initApp() {
  startScreen = getElem('start-screen');
  gameScreen = getElem('game-screen');
  levelSelect = getElem('level-select');
  languageSelect = getElem('language-select');
  userNameInput = getElem('user-name-input');
  startButton = getElem('start-button');
  rankTbody = getElem('rank-tbody');
  gameInfoHeader = getElem('game-info-header');
  timerText = getElem('timer-text');
  progressBar = getElem('progress-bar');
  sudokuBoard = getElem('sudoku-board');
  inputPanel = getElem('input-panel');
  ruleButton = getElem('rule-button');
  hintButton = getElem('hint-button');
  homeButton = getElem('home-button');
  hintCounter = getElem('hint-counter');
  modalOverlay = getElem('modal-overlay');
  modalTitle = getElem('modal-title');
  modalBody = getElem('modal-body');
  modalCloseButton = getElem('modal-close-button');

  // ランキング描画など
  renderRank();
  showScreen('start-screen');

  // スタートボタン登録
  if (startButton) startButton.addEventListener("click", startGame);

  // その他イベント登録
  if (userNameInput) userNameInput.addEventListener("input", checkStartButtonState);
  checkStartButtonState();

  if (ruleButton) ruleButton.addEventListener("click", () => {
    const lang = languageSelect ? languageSelect.value : 'en';
    const rule = GAME_RULES[lang];
    showModal(rule.title, rule.body);
  });
  if (hintButton) hintButton.addEventListener("click", useHint);
  if (homeButton) homeButton.addEventListener("click", () => showScreen('start-screen'));

  document.querySelectorAll('.input-button').forEach(button => {
    button.addEventListener("click", (e) => handleInput(e.target.dataset.value));
  });

  if (modalCloseButton) modalCloseButton.addEventListener("click", hideModal);
  if (modalOverlay) modalOverlay.addEventListener("click", (e) => {
    if (e.target.id === 'modal-overlay') hideModal();
  });
}

// ページ読み込み時に初期化
document.addEventListener('DOMContentLoaded', initApp);
