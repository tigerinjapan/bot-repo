/**
 * 生年設定
 * 
 * @param {string} yearVal - 年度
 */
function setYear(yearVal) {
  const startYear = 1970;
  const endYear = 2020;
  const valList = Array.from({ length: endYear - startYear + 1 }, (_, i) => startYear + i);
  createOptVal("year", valList, STR_SELECT_JA, yearVal);
};

/**
 * オプション要素生成
 * 
 * @param {string} elemId - 要素id
 * @param {string[]} valList - 要素値リスト
 * @param {string} defaultVal - デフォルト値
 * @param {string} selectVal - 選択値
 */
function createOptVal(elemId, valList, defaultVal, selectVal) {
  const selectElem = getElem(elemId);
  selectElem.innerHTML = SYM_BLANK;

  // Option for "SELECT"
  const defaultOption = createElemOnly(TAG_OPTION);
  defaultOption.value = SYM_BLANK;
  defaultOption.textContent = defaultVal;
  selectElem.appendChild(defaultOption);

  for (let i = 0; i < valList.length; i++) {
    const option = createElemOnly(TAG_OPTION);
    option.value = valList[i];
    option.textContent = valList[i];
    selectElem.appendChild(option);
  }
  selectElem.value = selectVal;
};

/**
 * 性別設定
 * 
 * @param {string} sexVal - 性別
 */
function setSex(sexVal) {
  const sexRadioButton = document.querySelector('input[name="sex"][value="' + sexVal + '"]');
  if (sexRadioButton) {
    sexRadioButton.checked = true;
  }
}

/**
 * 住所取得
 */
function getAddress() {
  setAddress(SYM_BLANK, SYM_BLANK);
}

/**
 * 住所設定
 * 
 * @param {string} selectLineVal - 選択した沿線
 * @param {string} selectStationVal - 選択した駅
 */
function setAddress(selectLineVal, selectStationVal) {
  // 郵便番号より、住所取得
  const zipCd = getElem(ID_ZIP_CD);
  const zipCdUrl = `${ENDPOINT_ZIP_CD}/${zipCd.value}`;
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
          createOptVal(ID_LINE, valList, STR_LINE_JA, selectLineVal);

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

/**
 * 駅設定
 * 
 * @param {string} selectedLine - 沿線
 * @param {string} selectStationVal - 駅
 */
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
      createOptVal(ID_STATION, valList, STR_STATION_JA, selectStationVal);
    })
    .catch(error => {
      alert(STR_STATION_JA + MSG_VAL_NOT_EXIST);
      console.error(stationUrl, error);
    });
};

/**
 * 沿線変更時
 * 
 * @param {HTMLElement} elem - 要素
 */
function changeLine(elem) {
  const lineVal = elem.value;
  setStation(lineVal, SYM_BLANK);
}

/**
 * メニュー設定
 * 
 * @param {string} menuVal - メニュー値
 */
function setMenu(menuVal) {
  const container = getElem('checkBoxMenu');
  const labels = LIST_APP;

  for (let i = 0; i < labels.length; i++) {
    const label = createElemOnly(TAG_LABEL);

    const checkbox = createElemOnly(TAG_INPUT);
    checkbox.type = 'checkbox';
    checkbox.id = `menu${i}`;
    checkbox.name = `menu${i}`;
    checkbox.value = i;

    label.appendChild(checkbox);
    label.appendChild(document.createTextNode(labels[i]));
    container.appendChild(label);
    if ((i + 1) % 3 === 0) {
      // 改行追加
      container.appendChild(createElemOnly(TAG_BR));
    }
  }

  for (let i = 0; i < menuVal.length; i++) {
    const val = menuVal[i];
    const menuId = `menu${val}`
    const checkbox = getElem(menuId);

    // 指定された状態に設定
    checkbox.checked = true;
  }
}

/**
 * ユーザー情報チェック
 */
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
    document.querySelector("form").addEventListener(EVENT_SUBMIT, function (event) {
      event.preventDefault();
      msgElem.value = errMsg;
      alert(errMsg);
      location.reload();
    });
  }
};
