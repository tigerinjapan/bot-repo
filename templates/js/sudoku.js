// タイトル設定
document.title = TITLE_SUDOKU;

/**
 * ゲーム設定定数
 */
// ゲーム制限時間（秒）
const GAME_TIMEOUT_SECONDS = 1200;

// 不正解時のペナルティ時間（秒）
const PENALTY_SECONDS = 30;

// ヒント数
const INITIAL_HINTS = 5;

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

const RANKING_HEAD = ["NAME", "TIME", "DATE"];

// ランキングデータ // TODO: data_listにする
const RANKING_DATA = [
  { name: "Sun", time: "08:00", date: "2025/11/01" },
  { name: "Earth", time: "08:30", date: "2025/11/02" },
  { name: "Moon", time: "09:00", date: "2025/11/03" },
  { name: "Mars", time: "09:30", date: "2025/11/04" },
  { name: "Neptune", time: "10:00", date: "2025/11/05" },
];

// 言語別ルールテキスト
const GAME_RULES = {
  ja: {
    title: "ゲーム ルール",
    body: `
      ナンプレ（数独）は、9×9のマス目に1から9までの数字を入れるパズルです。\n
      1. 横（行）・縦（列）に1から9までの数字が一つずつ入る。
      2. 9つの3×3のブロックそれぞれに1から9までの数字が一つずつ入る。
      3. 空のマスをタップし、表示された数字を入力できる。
      4. 間違える度に残り時間が1分短縮される。
      5. 20分のタイムアウトまでに全てのマスを埋める。
    `
  },
  ko: {
    title: "게임 규칙",
    body: `
      스도쿠는 9x9 칸에 1부터 9까지의 숫자를 채워 넣는 퍼즐입니다.\n
      1. 가로줄・세로줄에 1부터 9까지의 숫자가 한 번씩만 들어갑니다.
      2. 9개의 3x3 블록 각각에 1부터 9까지의 숫자가 한 번씩만 들어갑니다.
      3. 빈 칸을 탭하고 나타나는 숫자 패드로 숫자를 입력하세요.
      4. 틀릴 때마다 남은 시간이 1분씩 줄어듭니다.
      5. 20분 시간 초과 전에 모든 칸을 채우세요.
    `
  },
  en: {
    title: "GAME RULES",
    body: `
      Sudoku is a puzzle where you must fill a 9x9 grid with 1 to 9.\n
      1. Every row＆column must contain the numbers 1-9 exactly once.
      2. Every 3x3 grid must contain the numbers 1-9 exactly once.
      3. Tap an empty cell and use the keypad to enter a number.
      4. Each incorrect entry deducts 1 minute from your remaining time.
      5. Complete the grid before the 20-minute timeout.
    `
  }
};

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

// DOM要素の取得
let startScreen, gameScreen, levelSelect, langSelect, userNameInput, startButton;
let rankThead, rankTbody, gameInfoHeader, timerText, progressBar, sudokuBoard, inputPanel;
let ruleButton, hintButton, homeButton, hintCounter, modalOverlay, modalTitle, modalBody, modalCloseButton;

// ページ読み込み時に初期化
document.addEventListener('DOMContentLoaded', initApp);


// 初期化（DOM 要素の取得）
function initApp() {
  let btnParentElemId = "start-controls";
  startButton = createElem(TAG_BUTTON, "start-button", btnParentElemId);
  startButton.textContent = BUTTON_START;
  startButton.disabled = true;

  btnParentElemId = "game-controls";
  ruleButton = createElem(TAG_BUTTON, "rule-button", btnParentElemId);
  hintButton = createElem(TAG_BUTTON, "hint-button", btnParentElemId);
  homeButton = createElem(TAG_BUTTON, "home-button", btnParentElemId);
  ruleButton.textContent = TITLE_GAME_RULES;
  hintButton.textContent = BUTTON_HINT;
  homeButton.textContent = BUTTON_HOME;

  startScreen = getElem('start-screen');
  gameScreen = getElem('game-screen');
  langSelect = getElem('lang-select');
  levelSelect = getElem('level-select');
  userNameInput = getElem('user-name-input');
  rankThead = getElem('rank-thead');
  rankTbody = getElem('rank-tbody');
  gameInfoHeader = getElem('game-info-header');
  timerText = getElem('timer-text');
  progressBar = getElem('progress-bar');
  sudokuBoard = getElem('sudoku-board');
  inputPanel = getElem('input-panel');
  hintCounter = getElem('hint-counter');
  modalOverlay = getElem('modal-overlay');
  modalTitle = getElem('modal-title');
  modalBody = getElem('modal-body');
  modalCloseButton = getElem('modal-close-button');
  setElemText("modal-close-button", "X");

  setElemText("title", TITLE_SUDOKU);

  createOptionVal(langSelect, LIST_LANG_CD, LIST_LANG_NM);
  createOptionVal(levelSelect, LIST_LEVEL, LIST_LEVEL_NM);

  for (let i = 1; i <= 10; i++) {
    const elem = createElemNoVal(TAG_DIV, "input-panel");
    elem.className = "input-button";
    elem.dataset.value = i;
    elem.textContent = i;
    if (i === 10) {
      elem.dataset.value = 0;
      elem.textContent = "x";
    }
  }

  // ランキング描画など
  renderRank();
  showScreen('start-screen');

  // ヒントボタン初期状態
  if (hintButton) {
    hintButton.disabled = (hintsLeft <= 0);
    if (hintsLeft <= 0) hintButton.classList.add('disabled-hint'); else hintButton.classList.remove('disabled-hint');
  }

  // スタートボタン登録
  if (startButton) startButton.addEventListener("click", startGame);

  // その他イベント登録
  if (userNameInput) userNameInput.addEventListener("input", checkStartButtonState);
  checkStartButtonState();

  if (ruleButton) ruleButton.addEventListener("click", () => {
    const lang = langSelect ? langSelect.value : 'en';
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

// ゲーム開始
function startGame() {
  if (!levelSelect || !langSelect || !userNameInput) return;

  const level = levelSelect.value;

  // ユーザー名保存
  userName = userNameInput.value.trim();

  // 状態リセット
  timeRemaining = GAME_TIMEOUT_SECONDS;
  hintsLeft = INITIAL_HINTS;
  if (hintCounter) hintCounter.textContent = hintsLeft;

  // ヒントボタンを有効化（リセット時）
  if (hintButton) {
    hintButton.disabled = false;
    hintButton.classList.remove('disabled-hint');
  }

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

// 生成ロジック: 常にランダムな完成盤を使う
function generatePuzzle(level) {
  // 解答をシャッフルコピーで作成（毎回ランダムに）
  solution = shuffleSolution(SUDOKU_SOLUTION).map(row => [...row]);
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

  sudokuBoard.innerHTML = SYM_BLANK;
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

/**
 * cloneGrid: 2D 配列を深いコピー
 */
function cloneGrid(grid) {
  return grid.map(row => row.slice());
}

/**
 * shuffleArray: 配列を破壊的にシャッフル（Fisher-Yates）
 */
function shuffleArray(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

/**
 * shuffleSolution(base)
 * - 固定の完成盤 base を受け取り、行/列の入れ替え・バンド/スタック入れ替え・数字置換を行い
 *   毎回異なる完成盤を返す（元の論理解は保持）。
 * - これにより同一パズルでも表示がランダム化される。
 */
function shuffleSolution(base) {
  // 1) コピー
  let grid = cloneGrid(base);

  // 2) 数字をランダムマップする（1..9 -> permuted 1..9）
  const digits = [1, 2, 3, 4, 5, 6, 7, 8, 9];
  const perm = shuffleArray(digits.slice());
  const mapDigit = (v) => perm[v - 1];

  // apply digit map
  for (let r = 0; r < 9; r++) {
    for (let c = 0; c < 9; c++) {
      grid[r][c] = mapDigit(grid[r][c]);
    }
  }

  // 3) 行内の順序をバンドごとにシャッフル
  const newGridRows = Array(9).fill(null).map(() => Array(9).fill(0));
  const bandOrder = shuffleArray([0, 1, 2]);
  for (let bi = 0; bi < 3; bi++) {
    // rows indices in original for this band
    const srcBand = bandOrder[bi];
    const rows = [0, 1, 2].map(x => srcBand * 3 + x);
    shuffleArray(rows); // local shuffle inside band
    for (let i = 0; i < 3; i++) {
      newGridRows[bi * 3 + i] = grid[rows[i]].slice();
    }
  }
  grid = newGridRows;

  // 4) 列（スタック）についても同様にシャッフル
  // transpose, operate like rows, then transpose back
  function transpose(g) {
    const t = Array(9).fill(null).map(() => Array(9).fill(0));
    for (let r = 0; r < 9; r++) for (let c = 0; c < 9; c++) t[c][r] = g[r][c];
    return t;
  }
  let tranGrid = transpose(grid);
  const newTRows = Array(9).fill(null).map(() => Array(9).fill(0));
  const stackOrder = shuffleArray([0, 1, 2]);
  for (let si = 0; si < 3; si++) {
    const srcStack = stackOrder[si];
    const cols = [0, 1, 2].map(x => srcStack * 3 + x);
    shuffleArray(cols);
    for (let i = 0; i < 3; i++) {
      newTRows[si * 3 + i] = tranGrid[cols[i]].slice();
    }
  }
  tranGrid = newTRows;
  grid = transpose(tranGrid);

  return grid;
}

// ゲーム情報ヘッダーを更新
function updateGameInfoHeader(level, currentUserName) {
  if (!gameInfoHeader) return;

  // ランキングデータの更新タイム
  const bestTime = RANKING_DATA[0].time;

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

  const target = emptyCells[Math.floor(Math.random() * emptyCells.length)];
  const correctValue = solution[target.r][target.c];

  puzzle[target.r][target.c] = correctValue;
  hintsLeft--;
  if (hintCounter) hintCounter.textContent = hintsLeft;

  // ヒントが使い切られたらボタンを無効化
  if (hintButton) {
    if (hintsLeft <= 0) {
      hintButton.disabled = true;
      hintButton.classList.add('disabled-hint');
    } else {
      hintButton.disabled = false;
      hintButton.classList.remove('disabled-hint');
    }
  }

  renderBoard();
  const cellElement = sudokuBoard ? sudokuBoard.querySelector(`[data-row="${target.r}"][data-col="${target.c}"]`) : null;
  if (cellElement) {
    cellElement.classList.add('fixed-cell');
    cellElement.textContent = correctValue;
    cellElement.style.boxShadow = '0 0 15px magenta';
    setTimeout(() => { cellElement.style.boxShadow = SYM_BLANK; }, 1000);
  }

  showModal("HINT USED", `HINT LEFT: ${hintsLeft}`);
  checkGameCompletion();
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
  selectedCell.textContent = num === 0 ? SYM_BLANK : num;
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

// ランキングデータを表示
function renderRank() {
  if (!rankTbody) return;

  setElemText("rank-title", TITLE_RANK_TOP);

  rankThead.innerHTML = SYM_BLANK;
  RANKING_HEAD.forEach(rankHead => {
    createElem(TAG_TH, rankHead, "rank-thead");
  });

  rankTbody.innerHTML = SYM_BLANK;
  RANKING_DATA.forEach(rank => {
    const row = rankTbody.insertRow();
    row.innerHTML = `
      <td>${rank.name}</td>
      <td class="rank-time">${rank.time}</td>
      <td>${rank.date}</td>
    `;
  });
}

// スタートボタンの有効/無効をチェック
function checkStartButtonState() {
  if (!userNameInput || !startButton) return;

  const name = userNameInput.value.trim();
  // ユーザー名が4文字以上10文字以下の場合のみ有効
  if (4 <= name.length && name.length <= 10) {
    startButton.disabled = false;
  } else {
    startButton.disabled = true;
    // alert(MSG_INPUT_USER_EN);
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
    timerText.style.color = COLOR_RED;
    progressBar.style.backgroundColor = COLOR_RED;
  } else {
    timerText.style.color = 'cyan';
    progressBar.style.backgroundColor = 'cyan';
  }
}

// 時間表示をMM:SS形式に変換
function formatTime(seconds) {
  const minutes = Math.floor(seconds / 60);
  const secs = seconds % 60;
  const timeDisplay = `${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`
  return timeDisplay;
}

// 画面切り替え関数
function showScreen(screenId) {
  if (startScreen) startScreen.style.display = 'none';
  if (gameScreen) gameScreen.style.display = 'none';
  // flexに設定することで中央揃えを維持
  const targetScreen = getElem(screenId);
  if (targetScreen) {
    targetScreen.style.display = 'flex';
    currentScreen = screenId.replace('-screen', SYM_BLANK);
    if (currentScreen === 'start') {
      clearInterval(timer);
    }
  }
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
