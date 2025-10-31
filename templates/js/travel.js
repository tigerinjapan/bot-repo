// ヘッダー設定
setElemContentsByTag(TAG_HEAD, CONTENTS_HEAD_2);

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
  document.title = TITLE_TRAVEL;

  // セレクトボックス・各表示領域の取得
  const langSelect = getElem("lang-select");
  const regionSelect = getElem("region-select");

  // カードグリッド作成
  createCardGrid();

  // セレクトボックスの初期化
  createOptionVal(langSelect, LIST_LANG_CD);
  createOptionVal(regionSelect, LIST_CITY_VAL);

  // 画面内容の更新処理
  async function updateContent() {
    // アプリ名
    const appName = getElemText("appName");

    let lang = langSelect.value;

    // 言語コード
    const langCd = getElemText("langCd");
    if (langCd === LANG_CD_KO) {
      lang = LANG_CD_KO;
    }

    const region = regionSelect.value;

    travelData = await getFetchApiData(travelDataUrl, null);
    langData = await getFetchApiData(langDataUrl, null);

    travelData = travelData[lang];

    const label = travelData.label;
    const data = travelData[region];
    const exchangeRateData = travelData.exchangeRates;
    const currencyData = travelData.currency;
    const basicConversation = langData[region];

    const baseCountryCode = lang;
    const currencyCd = data.info.currency;

    // タイトル・サブタイトル表示
    setElemText("page-title", data.title);
    setElemText("page-subtitle", data.subtitle);

    // 基本情報
    setElemText("info-title", `ℹ️ ${data.info.name}`);

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
    setElemContents("info-content", infoHtml);

    // 言語（基本会話）
    setElemText("lang-title", `🌐 ${label.basicConversation}`);
    const langHtml = `
      ${basicConversation
        .map(
          (s) => `
          <tr>
              <th>${s.en}</th>
              <td>${s.local}
                <audio src="/templates/${s.mp3}" controls controlslist="nodownload"></audio>
              </td>
          </tr>
      `
        )
        .join(SYM_BLANK)}
    `;
    setElemContents("lang-content", langHtml);

    // 観光スポット
    setElemText("tour-title", `📸 ${label.tourInfo}`);
    const tourHtml = `
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
    setElemContents("tour-content", tourHtml);

    // グルメ
    setElemText("food-title", `🍽️ ${label.food}`);
    const foodHtml = `
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
    setElemContents("food-content", foodHtml);

    // 有用な情報
    setElemText("useful-title", `💡 ${label.usefulInfo}`);
    const usefulHtml = `
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
    setElemContents("useful-content", usefulHtml);

    // サイト情報
    setElemText("site-title", `🌐 ${label.site}`);
    const siteHtml = `
      <tr><th>${label.tourism}</th><td><a href="${data.site.tourism.url}" target="_blank">${data.site.tourism.name}</a></td></tr>
      <tr><th>${label.travel}</th><td><a href="${data.site.travel.url}" target="_blank">${data.site.travel.name}</a></td></tr>
      <tr><th>${label.youtube}</th><td><a href="${data.site.youtube.url}" target="_blank">${data.site.youtube.name}</a></td></tr>
  `;
    setElemContents("site-content", siteHtml);

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
        baseCountryCode === LANG_CD_JA
          ? 100
          : baseCountryCode === LANG_CD_KO
            ? 1000
            : 1;

      const resultAmount = (baseAmount * rate).toLocaleString();
      const baseCurrencySymbol = currencyData["base"];
      const targetCurrencySymbol = targetCurrencyCode.toUpperCase();
      return `${baseAmount.toLocaleString()}${baseCurrencySymbol} = ${resultAmount}${targetCurrencySymbol}`;
    }
    return SYM_BLANK;
  }

  // ダイアログ関連要素
  const dialog = getElem("dialog");
  const closeBtn = document.querySelector(".close-btn");

  // 観光スポットリンクのクリックイベントなどを設定
  function addEventListeners() {
    document.querySelectorAll(".spot-link").forEach((link) => {
      link.addEventListener("click", (e) => {
        e.preventDefault();

        setElemText("dialog-title", e.target.textContent);
        setElemText("dialog-text", e.target.dataset.map);
        dialog.style.display = "block";
      });
    });
  }

  // ダイアログの閉じる処理
  closeBtn.addEventListener("click", () => {
    dialog.style.display = ATTR_NONE;
  });
  window.addEventListener("click", (event) => {
    if (event.target === dialog) {
      dialog.style.display = ATTR_NONE;
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
  let gridHtml = SYM_BLANK;

  const grid_div_list = ['info', 'lang', 'tour', 'food', 'useful', 'site'];
  for (const grid_div of grid_div_list) {
    gridHtml += `
      <div class="card" id="${grid_div}-card">
        <h2>
          <span id="${grid_div}-title"></span>
        </h2>
        <table class="info-table">
          <tbody id="${grid_div}-content"></tbody>
        </table>
      </div>
  `};

  setElemContents("card-grid", gridHtml);
}

// セレクトボックスのオプション生成
function createOptionVal(selectElem, optValList) {
  selectElem.innerHTML = SYM_BLANK;

  if (optValList === LIST_LANG_CD) {
    textValList = LIST_LANG_NM;
  } else {
    textValList = LIST_CITY_EN;
  }

  for (let i = 0; i < optValList.length; i++) {
    const option = createElemOnly(TAG_OPTION);
    option.value = optValList[i];
    option.textContent = textValList[i];
    selectElem.appendChild(option);
  }
};