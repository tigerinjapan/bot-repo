// ヘッダー設定
getElemByTag(TAG_HEAD).innerHTML = CONTENTS_HEAD_2;

let travelDataUrl = URL_TRAVEL_SERVER;
let langDataUrl = URL_LANG_SERVER;

if (isLocal()) {
  travelDataUrl = URL_TRAVEL_LOCAL;
  langDataUrl = URL_LANG_LOCAL;
}

// DOM読み込み後の初期化処理
document.addEventListener("DOMContentLoaded", init);

// 初期表示
function init() {
  let travelData = null;
  let langData = null;

  // タイトル設定
  document.title = "🌏 Travel & Life";

  // セレクトボックス・各表示領域の取得
  const langSelect = getElem("lang-select");
  const regionSelect = getElem("region-select");

  const pageTitle = getElem("page-title");
  const pageSubtitle = getElem("page-subtitle");

  createCardGrid();

  const infoTitle = getElem("info-title");
  const langTitle = getElem("lang-title");
  const tourTitle = getElem("tour-title");
  const foodTitle = getElem("food-title");
  const usefulTitle = getElem("useful-title");
  const siteTitle = getElem("site-title");

  const infoContent = getElem("info-content");
  const langContent = getElem("lang-content");
  const tourContent = getElem("tour-content");
  const foodContent = getElem("food-content");
  const usefulContent = getElem("useful-content");
  const siteContent = getElem("site-content");

  // ダイアログ関連要素
  const dialog = getElem("dialog");
  const closeBtn = document.querySelector(".close-btn");
  const dialogTitle = getElem("dialog-title");
  const dialogText = getElem("dialog-text");

  // セレクトボックスの初期化
  createOptionVal(langSelect, LIST_LANG_VAL);
  createOptionVal(regionSelect, LIST_CITY_VAL);

  // 画面内容の更新処理
  async function updateContent() {

    const lang = langSelect.value;
    const region = regionSelect.value;

    travelData = await getFetchApiData(travelDataUrl);
    langData = await getFetchApiData(langDataUrl);

    travelData = travelData[lang];

    const label = travelData.label;
    const data = travelData[region];
    const exchangeRateData = travelData.exchangeRates;
    const currencyData = travelData.currency;
    const basicConversation = langData[region];

    const baseCountryCode = lang;
    const currencyCd = data.info.currency;

    // タイトル・サブタイトル表示
    pageTitle.textContent = data.title;
    pageSubtitle.textContent = data.subtitle;

    // 基本情報
    infoTitle.textContent = `ℹ️ ${data.info.name}`;

    let infoHtml = SYM_BLANK;
    const infoDataList = [
      [label.capital, data.info.capital],
      [label.area, data.info.area.toLocaleString() + "km²"],
      [label.population, data.info.population.toLocaleString()],
      [label.currency, data.info.currency],
      [label.exchangeRate, getExchangeRate(exchangeRateData, currencyData, baseCountryCode, region)],
      [label.weather, data.info.weather],
      [label.timezone, data.info.timezone],
      [label.flightTime, data.info.flightTime]
    ];

    // 基本情報テーブル生成
    for (const [labelText, value] of infoDataList) {
      if (value !== SYM_BLANK) {
        infoHtml += `
            <tr><th>${labelText}</th><td>${value}</td></tr>
          `;
      }
    }
    infoContent.innerHTML = infoHtml;

    // 言語（基本会話）
    langTitle.textContent = `🌐 ${label.basicConversation}`;
    langContent.innerHTML = `
      ${basicConversation
        .map(
          (s) => `
          <tr>
              <th>${s.en}</th>
              <td>${s.local}</td>
          </tr>
      `
        )
        .join(SYM_BLANK)}
    `;

    // 観光スポット
    tourTitle.textContent = `📸 ${label.tourInfo}`;
    tourContent.innerHTML = `
      <tr>
          <th>${label.category}</th>
          <th>${label.spot}</th>
          <th>${label.access}</th>
          <th>${label.remark}</th>
      </tr>
      ${data.tour.spots
        .map(
          (s) => `
          <tr>
              <td>${s.category}</td>
              <td><a href="#" class="spot-link" data-map="${s.map}">${s.name}</a></td>
              <td>${s.access}</td>
              <td>${s.note}</td>
          </tr>
      `
        )
        .join(SYM_BLANK)}
    `;

    // グルメ
    foodTitle.textContent = `🍽️ ${label.food}`;
    foodContent.innerHTML = `
      ${data.food.foods
        .map(
          (f) => `
          <tr>
              <th>${f.name}</th>
              <td>${f.price.toLocaleString()}${currencyCd}</td>
              <td>${f.note}</td>
          </tr>
      `
        )
        .join(SYM_BLANK)}
    `;

    // 有用な情報
    usefulTitle.textContent = `💡 ${label.usefulInfo}`;
    usefulContent.innerHTML = `
      <tr>
          <th>${label.exchange}</th>
          <td><a href="${data.useful.exchange.url}" target="_blank">${data.useful.exchange.name}</a></td>
          <td>${data.useful.exchange.note}</td>
      </tr>
      <tr>
          <th>${label.airportAccess}</th>
          <td>${data.useful.airportAccess.name}</td>
          <td>${data.useful.airportAccess.fare.toLocaleString()}${currencyCd}</td>
      </tr>
      <tr>
          <th>${label.transportCard}</th>
          <td>${data.useful.transportCard.name}</td>
          <td>${data.useful.transportCard.fare.toLocaleString()}${currencyCd} (${label.baseFare})</td>
      </tr>
  `;

    // サイト情報
    siteTitle.textContent = `🌐 ${label.site}`;
    let siteHtml = `
      <tr><th>${label.tourism}</th><td><a href="${data.site.tourism.url}" target="_blank">${data.site.tourism.name}</a></td></tr>
      <tr><th>${label.travel}</th><td><a href="${data.site.travel.url}" target="_blank">${data.site.travel.name}</a></td></tr>
      <tr><th>${label.youtube}</th><td><a href="${data.site.youtube.url}" target="_blank">${data.site.youtube.name}</a></td></tr>
  `;
    siteContent.innerHTML = siteHtml;

    // イベントリスナー追加
    addEventListeners();
  }

  // 為替レート表示用の計算関数
  function getExchangeRate(exchangeRateData, currencyData, baseCountryCode, region) {
    const targetCurrencyCode =
      region === "seoul"
        ? "krw"
        : region === "taipei"
          ? "twd"
          : region === "hanoi"
            ? "vnd"
            : region === "bangkok"
              ? "thb"
              : region === "manila"
                ? "php"
                : "jpy";

    const rate = exchangeRateData[targetCurrencyCode];
    if (rate) {
      const baseAmount =
        baseCountryCode === "ja"
          ? 100
          : baseCountryCode === "ko"
            ? 1000
            : 1;

      const resultAmount = (baseAmount * rate).toLocaleString();
      const baseCurrencySymbol = currencyData["base"];
      const targetCurrencySymbol = targetCurrencyCode.toUpperCase();
      return `${baseAmount.toLocaleString()}${baseCurrencySymbol} = ${resultAmount}${targetCurrencySymbol}`;
    }
    return SYM_BLANK;
  }

  // 観光スポットリンクのクリックイベントなどを設定
  function addEventListeners() {
    document.querySelectorAll(".spot-link").forEach((link) => {
      link.addEventListener("click", (e) => {
        e.preventDefault();
        dialogTitle.textContent = e.target.textContent;
        dialogText.textContent = e.target.dataset.map;
        dialog.style.display = "block";
      });
    });
  }

  // ダイアログの閉じる処理
  closeBtn.addEventListener("click", () => {
    dialog.style.display = "none";
  });
  window.addEventListener("click", (event) => {
    if (event.target === dialog) {
      dialog.style.display = "none";
    }
  });

  // 言語・都市選択時の内容更新
  langSelect.addEventListener("change", updateContent);
  regionSelect.addEventListener("change", updateContent);

  // 初期表示（東京・日本語）
  updateContent();
}

// カードグリッド作成
function createCardGrid() {
  let infoHtml = SYM_BLANK;

  const grid_div_list = ['info', 'lang', 'tour', 'food', 'useful', 'site'];
  for (const grid_div of grid_div_list) {
    infoHtml += `
      <div class="card" id="${grid_div}-card">
        <h2>
          <span id="${grid_div}-title"></span>
        </h2>
        <table class="info-table">
          <tbody id="${grid_div}-content"></tbody>
        </table>
      </div>
  `};

  const cardGrid = getElem("card-grid");
  cardGrid.innerHTML = infoHtml;
}

// セレクトボックスのオプション生成
function createOptionVal(selectElem, optValList) {
  selectElem.innerHTML = SYM_BLANK;

  if (optValList === LIST_LANG_VAL) {
    textValList = LIST_LANG;
  } else {
    textValList = LIST_CITY_EN;
  }

  for (let i = 0; i < optValList.length; i++) {
    const option = document.createElement("option");
    option.value = optValList[i];
    option.textContent = textValList[i];
    selectElem.appendChild(option);
  }
};