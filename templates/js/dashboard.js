// ====================
// テキストコンテンツ定義
// ====================
const appTexts = {
  timePeriodLabel: "表示期間:",
  periodOptions: [
    { value: "day", text: "日 (直近1週間)" },
    { value: "week", text: "週 (直近4週)" },
    { value: "month", text: "月 (直近12か月)" },
    { value: "year", text: "年 (直近5年)" }
  ]
};

// ====================
// KPI項目定義とHTML生成 (ループ処理)
// ====================
const kpiItems = [
  { id: "users", title: "👤 アクセスしたユーザー数", type: "line", dataKey: "users" },
  { id: "pages", title: "📄 アクセスしたページ", type: "bar", dataKey: "pages" },
  { id: "device", title: "📱 使用したデバイス", type: "doughnut", dataKey: "devices" },
  { id: "os", title: "💻 デバイスのOS", type: "doughnut", dataKey: "os" }
];

// 期間ごとのデータ // TODO: 取得したログを分析し、データをDB保持
const dashboardData = {
  day: {
    label: "日",
    users: { total: "3,500", labels: ["10/8", "10/9", "10/10", "10/11", "10/12", "10/13", "10/14"], data: [500, 480, 520, 600, 450, 550, 400] },
    pages: { labels: ["トップ", "ニュース", "製品", "ブログ", "お問い合わせ"], data: [1200, 900, 600, 400, 300] },
    devices: [{ name: "モバイル", value: 55 }, { name: "デスクトップ", value: 40 }, { name: "タブレット", value: 5 }],
    os: [{ name: "iOS", value: 30 }, { name: "Android", value: 25 }, { name: "Windows", value: 35 }, { name: "macOS", value: 10 }]
  },
  week: {
    label: "週",
    users: { total: "12,800", labels: ["4週前", "3週前", "2週前", "1週前"], data: [2800, 3200, 3000, 3800] },
    pages: { labels: ["トップ", "製品", "ニュース", "ブログ", "お問い合わせ"], data: [4500, 3000, 2500, 1500, 800] },
    devices: [{ name: "モバイル", value: 60 }, { name: "デスクトップ", value: 35 }, { name: "タブレット", value: 5 }],
    os: [{ name: "Windows", value: 40 }, { name: "iOS", value: 20 }, { name: "Android", value: 25 }, { name: "macOS", value: 15 }]
  },
  month: {
    label: "月",
    users: { total: "150,000", labels: ["12ヶ月前", "9ヶ月前", "6ヶ月前", "3ヶ月前", "先月", "今月"], data: [10000, 12000, 15000, 14000, 18000, 20000] },
    pages: { labels: ["トップ", "製品", "ニュース", "採用", "お問い合わせ"], data: [50000, 35000, 30000, 20000, 15000] },
    devices: [{ name: "モバイル", value: 70 }, { name: "デスクトップ", value: 25 }, { name: "タブレット", value: 5 }],
    os: [{ name: "iOS", value: 35 }, { name: "Android", value: 30 }, { name: "Windows", value: 25 }, { name: "macOS", value: 10 }]
  },
  year: {
    label: "年",
    users: { total: "1,500,000", labels: ["5年前", "4年前", "3年前", "2年前", "去年", "今年"], data: [150000, 200000, 250000, 350000, 400000, 450000] },
    pages: { labels: ["トップ", "製品", "ニュース", "採用", "IR情報"], data: [500000, 400000, 300000, 200000, 100000] },
    devices: [{ name: "モバイル", value: 75 }, { name: "デスクトップ", value: 20 }, { name: "タブレット", value: 5 }],
    os: [{ name: "Android", value: 40 }, { name: "iOS", value: 30 }, { name: "Windows", value: 20 }, { name: "macOS", value: 10 }]
  }
};

// グラフオブジェクトを保持するMap
const charts = new Map();

// 棒グラフ/折れ線グラフを描画する共通関数
function updateLineBarChart(chartId, type, dataItems, title, color) {
  const canvas = getElem(chartId);
  if (charts.has(chartId)) charts.get(chartId).destroy();

  const newChart = new Chart(canvas, {
    type: type,
    data: {
      labels: dataItems.labels,
      datasets: [{
        label: title,
        data: dataItems.data,
        borderColor: (type === 'line' ? 'steelblue' : color),
        backgroundColor: (type === 'line' ? 'lightblue' : color),
        tension: (type === 'line' ? 0.3 : 0),
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: { y: { beginAtZero: true } }
    }
  });
  charts.set(chartId, newChart);
}

// 円グラフ（ドーナツ型）を描画する共通関数
function updateDoughnutChart(chartId, dataItems) {
  const canvas = getElem(chartId);
  if (charts.has(chartId)) charts.get(chartId).destroy();

  const labels = dataItems.map(d => `${d.name} (${d.value}%)`);
  const values = dataItems.map(d => d.value);

  const newChart = new Chart(canvas, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        data: values,
        backgroundColor: ['skyblue', 'salmon', 'lightgreen', 'gold', 'silver'],
        hoverOffset: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'right' },
        title: { display: false }
      }
    }
  });
  charts.set(chartId, newChart);
}

// KPIカードのHTMLを生成し、グリッドに追加する
function initializeKpiCards() {
  const grid = getElem('dashboard-grid');
  let html = '';

  kpiItems.forEach(item => {
    const isUsers = item.id === 'users';
    html += `
      <div class="kpi-card">
          <h2>${item.title}</h2>
          ${isUsers ? `<span id="${item.id}-count" class="current-value"></span>` : ''}
          <div class="chart-container">
              <canvas id="${item.id}Chart"></canvas>
          </div>
      </div>
    `;
  });

  grid.innerHTML = html;
}

// データをHTMLとグラフに反映させるメイン関数
function updateDashboard(period) {
  const data = dashboardData[period];
  if (!data) return;

  kpiItems.forEach(item => {
    const chartId = `${item.id}Chart`;
    const itemData = data[item.dataKey];

    if (item.type === 'line') {
      // ユーザー数
      setElemText(`${item.id}-count`, itemData.total.toLocaleString());
      updateLineBarChart(chartId, 'line', itemData, item.title.replace(/👤\s*/, ''), 'steelblue');
    } else if (item.type === 'bar') {
      // アクセスしたページ
      updateLineBarChart(chartId, 'bar', itemData, item.title.replace(/📄\s*/, ''), 'forestgreen');
    } else if (item.type === 'doughnut') {
      // デバイス/OS
      updateDoughnutChart(chartId, itemData);
    }
  });
}

// ページロード時の初期化処理
function initializeApp() {
  // テキスト定義の適用
  document.title = TITLE_DASH_BOARD;
  setElemText("header-title", TITLE_DASH_BOARD);
  setElemText('time-period-label', appTexts.timePeriodLabel);

  // プルダウンオプションの生成
  const selectElem = getElem('time-period');
  appTexts.periodOptions.forEach(option => {
    const opt = createElemOnly(TAG_OPTION);
    opt.value = option.value;
    opt.textContent = option.text;
    selectElem.appendChild(opt);
  });

  // KPIカードの生成
  initializeKpiCards();

  // 初期データ表示
  updateDashboard('day');

  // プルダウン変更時のイベントリスナー
  selectElement.addEventListener('change', (event) => {
    updateDashboard(event.target.value);
  });
}

// ページロード時の初期化
window.onload = () => {
  initializeApp();
};
