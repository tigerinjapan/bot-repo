const SYM_BLANK = "";

const LANG_VAL_JA = "ja";
const LANG_VAL_KO = "ko";
const LANG_VAL_EN = "en";
const LIST_LANG_VAL = [LANG_VAL_JA, LANG_VAL_KO, LANG_VAL_EN];

const LANG_JA = "日本語";
const LANG_KO = "한국어";
const LANG_EN = "English";
const LIST_LANG = [LANG_JA, LANG_KO, LANG_EN];

const LIST_CITY_VAL = ["tokyo", "seoul", "taipei", "hanoi", "bangkok", "manila"];
const LIST_CITY_JA = ["東京", "ソウル", "台北", "ハノイ", "バンコク", "マニラ"];
const LIST_CITY_KO = ["도쿄", "서울", "타이베이", "하노이", "방콕", "마닐라"];
const LIST_CITY_EN = ["Tokyo", "Seoul", "Taipei", "Hanoi", "Bangkok", "Manila"];

document.addEventListener("DOMContentLoaded", () => {
  const langSelect = document.getElementById("lang-select");
  const regionSelect = document.getElementById("region-select");

  const pageTitle = document.getElementById("page-title");
  const pageSubtitle = document.getElementById("page-subtitle");

  const infoTitle = document.getElementById("info-title");
  const langTitle = document.getElementById("lang-title");
  const tourTitle = document.getElementById("tour-title");
  const foodTitle = document.getElementById("food-title");
  const usefulTitle = document.getElementById("useful-title");
  const siteTitle = document.getElementById("site-title");

  const infoContent = document.getElementById("info-content");
  const langContent = document.getElementById("lang-content");
  const tourContent = document.getElementById("tour-content");
  const foodContent = document.getElementById("food-content");
  const usefulContent = document.getElementById("useful-content");
  const siteContent = document.getElementById("site-content");

  const dialog = document.getElementById("dialog");
  const closeBtn = document.querySelector(".close-btn");
  const dialogTitle = document.getElementById("dialog-title");
  const dialogText = document.getElementById("dialog-text");

  createOptionVal(langSelect, LIST_LANG_VAL);
  createOptionVal(regionSelect, LIST_CITY_VAL);

  function updateContent() {
    const lang = langSelect.value;
    const region = regionSelect.value;
    const data = travelData[lang][region];
    const label = travelData[lang]["label"];
    const baseCountryCode = lang;

    pageTitle.textContent = data.title;
    pageSubtitle.textContent = data.subtitle;

    // Info Card
    infoTitle.textContent = data.info.name;
    let infoHtml = `
      <tr><th>${label.capital}</th><td>${data.info.capital}</td></tr>
    `;

    infoHtml += `<tr><th>${label.area}</th>
      <td>${data.info.area.toLocaleString()}km²</td></tr>
    `;

    infoHtml += `<tr><th>${label.population}</th><td>
      ${data.info.population.toLocaleString()}</td></tr>
    `;

    infoHtml += `
      <tr><th>${label.currency}</th><td>${data.info.currency}</td></tr>
    `;

    const rate = `${getExchangeRate(baseCountryCode, region)}`;
    if (rate != "") {
      infoHtml += `<tr><th>${label.exchangeRate}</th><td>${rate}</td></tr>`;
    }

    infoHtml += `
      <tr><th>${label.weather}</th><td>${data.info.weather}</td></tr>
    `;
    infoContent.innerHTML = infoHtml;

    // Lang Card
    langTitle.textContent = data.lang.name;
    langContent.innerHTML = `
      ${data.lang.basicConversation
        .map(
          (s) => `
          <tr>
              <th>${s.en}</th>
              <td>${s.local}</td>
          </tr>
      `
        )
        .join("")}
    `;

    // Tour Card
    tourTitle.textContent = data.tour.name;
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
        .join("")}
    `;

    // Food Card
    foodTitle.textContent = data.food.name;
    foodContent.innerHTML = `
      ${data.food.foods
        .map(
          (f) => `
          <tr>
              <th>${f.name}</th>
              <td>${f.price}</td>
              <td>${f.note}</td>
          </tr>
      `
        )
        .join("")}
    `;

    // Useful Info Card
    usefulTitle.textContent = data.useful.name;
    usefulContent.innerHTML = `
      <tr>
          <th>${label.exchange}</th>
          <td><a href="${data.useful.exchange.url}" target="_blank">${data.useful.exchange.name}</a></td>
          <td>${data.useful.exchange.note}</td>
      </tr>
      <tr>
          <th>${label.airportAccess}</th>
          <td>${data.useful.airportAccess.name}</td>
          <td>${data.useful.airportAccess.fare}</td>
      </tr>
      <tr>
          <th>${label.transportCard}</th>
          <td>${data.useful.transportCard.name}</td>
          <td>${data.useful.transportCard.fare} (${label.baseFare})</td>
      </tr>
  `;

    // Site Card
    siteTitle.textContent = data.site.name;
    let siteHtml = `
      <tr><th>${label.tourism}</th><td><a href="${data.site.tourism.url}" target="_blank">${data.site.tourism.name}</a></td></tr>
      <tr><th>${label.travel}</th><td><a href="${data.site.travel.url}" target="_blank">${data.site.travel.name}</a></td></tr>
      <tr><th>${label.youtube}</th><td><a href="${data.site.youtube.url}" target="_blank">${data.site.youtube.name}</a></td></tr>
  `;
    siteContent.innerHTML = siteHtml;

    addEventListeners();
  }

  function getExchangeRate(baseCountryCode, region) {
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
                : SYM_BLANK;
    if (targetCurrencyCode && exchangeRates[baseCountryCode]) {
      const baseAmount =
        baseCountryCode === "ja"
          ? 100
          : baseCountryCode === "ko"
            ? 1000
            : 1;
      const rate = exchangeRates[baseCountryCode][targetCurrencyCode];
      const resultAmount = (baseAmount * rate).toLocaleString();
      const baseCurrencySymbol = coreData[baseCountryCode].currency;
      const targetCurrencySymbol = travelData[baseCountryCode][region].info.currency;
      return `${baseAmount.toLocaleString()}${baseCurrencySymbol} = ${resultAmount}${targetCurrencySymbol}`;
    }
    return SYM_BLANK;
    // return `${label.error}`;
  }

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

  closeBtn.addEventListener("click", () => {
    dialog.style.display = "none";
  });
  window.addEventListener("click", (event) => {
    if (event.target == dialog) {
      dialog.style.display = "none";
    }
  });

  langSelect.addEventListener("change", updateContent);
  regionSelect.addEventListener("change", updateContent);

  // Initial load for Tokyo in Japanese
  updateContent();
});

// オプション値生成
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