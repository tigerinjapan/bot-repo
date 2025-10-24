// ====================
// テキストコンテンツ定義
// ====================
const appTexts = {
  timePeriodLabel: "Term ",
  periodOptions: [
    { value: "day", text: "Day" },
    { value: "month", text: "Month" },
    { value: "year", text: "Year" }
  ]
};

// ====================
// KPI項目定義とHTML生成 (ループ処理)
// ====================
const kpiItems = [
  { id: "users", title: "👤 Users", type: "line", dataKey: "users" },
  { id: "category", title: "📄 Category", type: "bar", dataKey: "category" },
  { id: "app", title: "🌐 App", type: "doughnut", dataKey: "app" },
  { id: "device", title: "📱 Device", type: "doughnut", dataKey: "device" },
  { id: "os", title: "💻 OS", type: "doughnut", dataKey: "os" },
  { id: "browser", title: "🌐 Browser", type: "doughnut", dataKey: "browser" }
];

// グラフオブジェクトを保持するMap
const charts = new Map();

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
  selectElem.addEventListener('change', (event) => {
    updateDashboard(event.target.value);
  });
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
async function updateDashboard(period) {
  let dashboardDataUrl = URL_DASHBOARD_SERVER;
  if (isLocal()) {
    dashboardDataUrl = URL_DASHBOARD_LOCAL;
  }

  // 期間ごとのデータ
  const dashboardData = await getFetchApiData(dashboardDataUrl, null);

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

// ページロード時の初期化
window.onload = () => {
  initializeApp();
};
