// メッセージ
const MSG_VAL_NOT_EXIST = "が存在しません";
const MSG_ERR_PASSWORD_NOT_MATCH = "パスワードが一致しません"

// ID
const ID_SEX = "sex";
const ID_ZIP_CD = "zipCd";
const ID_PREF = "pref";
const ID_TOWN = "town";
const ID_LINE = "line";
const ID_STATION = "station";

// 文字列
const STR_LINES = "Lines";
const STR_STATIONS = "Stations";

const STR_SELECT_JA = "選択";
const STR_ZIP_CD_JA = "郵便番号";
const STR_LINE_JA = "沿線";
const STR_STATION_JA = "駅";

// URL
const URL_ZIP_API = "http://zipcloud.ibsnet.co.jp/api";
const URL_ADDR_INFO = "https://express.heartrails.com";
const URL_ADDR_API = `${URL_ADDR_INFO}/api/json?method=get`;
const URL_LINE_API = `${URL_ADDR_API}${STR_LINES}`;
const URL_STATION_API = `${URL_ADDR_API}${STR_STATIONS}`;

// 生年設定
function setYear(yearVal) {
  const startYear = 1970;
  const endYear = 2020;
  const valList = Array.from({ length: endYear - startYear + 1 }, (_, i) => startYear + i);
  createOptionVal("year", valList, STR_SELECT_JA, yearVal);
};

// オプション値生成
function createOptionVal(elemId, valList, defaultVal, selectVal) {
  const selectElem = document.getElementById(elemId);
  selectElem.innerHTML = SYM_BLANK;

  // Option for "SELECT"
  const defaultOption = document.createElement("option");
  defaultOption.value = SYM_BLANK;
  defaultOption.textContent = defaultVal;
  selectElem.appendChild(defaultOption);

  for (let i = 0; i < valList.length; i++) {
    const option = document.createElement("option");
    option.value = valList[i];
    option.textContent = valList[i];
    selectElem.appendChild(option);
  }
  selectElem.value = selectVal;
};

// 性別設定
function setSex(sexVal) {
  const sexRadioButton = document.querySelector('input[name="sex"][value="' + sexVal + '"]');
  if (sexRadioButton) {
    sexRadioButton.checked = true;
  }
}

// 住所取得
function getAddress() {
  setAddress(SYM_BLANK, SYM_BLANK);
}

// 住所設定
function setAddress(selectLineVal, selectStationVal) {
  // 郵便番号より、住所取得
  const zipCd = document.getElementById(ID_ZIP_CD);
  const zipCdUrl = `${URL_ZIP_API}/search?zipcode=${zipCd.value}`;

  fetch(zipCdUrl)
    .then(response => response.json())
    .then(data => {
      // 郵便番号より、住所設定
      const result = data.results[0];
      const prefVal = result.address1;
      const townVal = result.address2;
      document.getElementById(ID_PREF).value = prefVal;
      document.getElementById(ID_TOWN).value = townVal;

      const lineUrl = `${URL_LINE_API}&prefecture=${prefVal}`;
      fetch(lineUrl)
        .then(response => response.json())
        .then(data => {
          // 沿線設定
          const valList = data.response.line;
          if (selectLineVal == SYM_BLANK) {
            selectLineVal = valList[0];
          }
          createOptionVal(ID_LINE, valList, STR_LINE_JA, selectLineVal);

          // 駅設定
          setStation(selectLineVal, selectStationVal);
        })
        .catch(error => {
          alert(STR_LINE_JA + MSG_VAL_NOT_EXIST);
          console.error(lineUrl, error);
        });
    })
    .catch(error => {
      alert(STR_ZIP_CD_JA + MSG_VAL_NOT_EXIST);
      console.error(zipCdUrl, error);
    });
};

// 駅設定
function setStation(selectedLine, selectStationVal) {
  const stationUrl = `${URL_STATION_API}&line=${selectedLine}`;
  fetch(stationUrl)
    .then(response => response.json())
    .then(data => {
      const itemList = data.response.station;

      // nameの値を抽出してリスト化
      const valList = itemList.map(item => item.name);

      if (selectStationVal == SYM_BLANK) {
        selectStationVal = valList[0];
      }
      createOptionVal(ID_STATION, valList, STR_STATION_JA, selectStationVal);
    })
    .catch(error => {
      alert(STR_STATION_JA + MSG_VAL_NOT_EXIST);
      console.error(stationUrl, error);
    });
};

// 沿線変更時
function changeLine(elem) {
  const lineVal = elem.value;
  setStation(lineVal, SYM_BLANK);
}

// ユーザー情報チェック
function checkUserInfo() {
  const msgElem = document.getElementById("chkMsg");

  const pwVal = document.getElementById("userPw").value;
  const pwCheckVal = document.getElementById("pwCheck").value;
  if (pwVal != pwCheckVal) {
    msgElem.value = MSG_ERR_PASSWORD_NOT_MATCH;
    document.querySelector("form").addEventListener("submit", function (event) {
      event.preventDefault();
      alert(MSG_ERR_PASSWORD_NOT_MATCH);
      location.reload();
    });
  }
};
