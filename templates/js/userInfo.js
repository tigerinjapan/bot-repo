// 生年設定
function setYear(yearVal) {
  const startYear = 1970;
  const endYear = 2020;
  const valList = Array.from({ length: endYear - startYear + 1 }, (_, i) => startYear + i);
  createOptionVal("year", valList, STR_SELECT_JA, yearVal);
};

// オプション値生成
function createOptionVal(elemId, valList, defaultVal, selectVal) {
  const selectElem = getElem(elemId);
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
  let zipUrl = URL_ZIP_SERVER;
  if (isLocal()) {
    zipUrl = URL_ZIP_LOCAL;
  }

  const zipCd = getElem(ID_ZIP_CD);
  const zipCdUrl = `${zipUrl}/${zipCd.value}`;
  const api_header = {
    method: "GET",
    headers: {
      "Content-Type": "application/json"
    },
  };

  fetch(zipCdUrl, api_header)
    .then(response => response.json())
    .then(data => {
      // 郵便番号より、住所設定
      const prefVal = data.pref;
      const townVal = data.city;
      getElem(ID_PREF).value = prefVal;
      getElem(ID_TOWN).value = townVal;

      const lineUrl = `${URL_LINE_API}&prefecture=${prefVal}`;
      fetch(lineUrl)
        .then(response => response.json())
        .then(data => {
          // 沿線設定
          const valList = data.response.line;
          if (selectLineVal === SYM_BLANK) {
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

      if (selectStationVal === SYM_BLANK) {
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

// メニュー設定
function setMenu(menuVal) {
  const container = getElem('checkBoxMenu');
  const labels = LIST_APP;

  for (let i = 0; i < labels.length; i++) {
    const label = document.createElement('label');

    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.id = `menu${i}`;
    checkbox.name = `menu${i}`;
    checkbox.value = i;

    label.appendChild(checkbox);
    label.appendChild(document.createTextNode(labels[i]));
    container.appendChild(label);
    if ((i + 1) % 3 === 0) {
      container.appendChild(document.createElement('br')); // 改行追加
    }
  }

  for (let i = 0; i < menuVal.length; i++) {
    const val = menuVal[i];
    const menuId = `menu${val}`
    const checkbox = getElem(menuId);
    checkbox.checked = true; // 指定された状態に設定
  }
}

// ユーザー情報チェック
function checkUserInfo() {
  let checkFlg = true;
  let errMsg = SYM_BLANK;
  const msgElem = getElem("chkMsg");

  const pwVal = getElem("userPw").value;
  const pwCheckVal = getElem("pwCheck").value;
  if (pwVal !== pwCheckVal) {
    checkFlg = false;
    errMsg = MSG_ERR_PASSWORD_NOT_MATCH;
  }

  const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
  const selectedValues = Array.from(checkboxes).map(cb => cb.value);
  if (selectedValues.length === 0) {
    checkFlg = false;
    errMsg = MSG_ERR_MENU_NO_CHECKED_ELEMENTS;
  } else if (5 < selectedValues.length) {
    checkFlg = false;
    errMsg = MSG_ERR_MENU_CHECKED_MAX;
  }

  if (!checkFlg) {
    document.querySelector("form").addEventListener("submit", function (event) {
      event.preventDefault();
      msgElem.value = errMsg;
      alert(errMsg);
      location.reload();
    });
  }
};
