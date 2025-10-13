// プロンプトに追加する共通の条件
const commonConditions_image = "高品質、詳細、フォトリアル、明るい色調、楽しい雰囲気";
const commonConditions_text = "明確、簡潔、丁寧、ポジティブ、想像力をかきたてる";

// ヘッダー設定
setElemContentsByTag(TAG_HEAD, CONTENTS_HEAD_1);

let geminiDataUrl = URL_GEMINI_ITEMS_SERVER;
let apiUrl = URL_GEMINI_SERVER;
let imgUrl = URL_GEMINI_IMG_SERVER;
if (isLocal()) {
    geminiDataUrl = URL_GEMINI_ITEMS_LOCAL;
    apiUrl = URL_GEMINI_LOCAL;
    // imgUrl = URL_GEMINI_IMG_LOCAL;
}

// DOM読み込み後の処理
document.addEventListener('DOMContentLoaded', init);

// 初期表示
function init() {
    changeLanguage('ja');

    const mode = getElem('generationMode').value;
    let outputImage = getElem('outputImageContainer');
    let outputText = getElem('outputTextContainer');
    let generatedImage = getElem('generatedImage');
    let generatedText = getElem('generatedText');

    if (mode === MODE_IMG) {
        outputImage.style.display = ATTR_BLOCK;
        generatedImage.style.display = ATTR_BLOCK;
        outputText.style.display = ATTR_NONE;
        generatedText.style.display = ATTR_NONE;
    } else {
        outputImage.style.display = ATTR_NONE;
        generatedImage.style.display = ATTR_NONE;
        outputText.style.display = ATTR_BLOCK;
        generatedText.style.display = ATTR_BLOCK;
    }

    generatedImage.src = '';
    generatedText.textContent = '';

    const copyButtons = document.querySelectorAll('.copy-button');
    copyButtons.forEach(button => button.style.display = ATTR_NONE);
}

// 言語設定
async function changeLanguage(lang) {
    document.documentElement.lang = lang;

    const geminiData = await getFetchApiData(geminiDataUrl, null);
    const texts = geminiData[lang];

    // data-keyを持つすべての要素のテキストを更新
    document.querySelectorAll('[data-key]').forEach(element => {
        const key = element.getAttribute('data-key');
        if (element.tagName === 'TITLE') {
            element.textContent = texts[key];
        } else if (element.tagName === 'TEXTAREA') {
            element.placeholder = texts[key];
        } else {
            element.textContent = texts[key];
        }
    });

    // SELECT要素を動的に生成
    const modeSelect = getElem('generationMode');
    createSelect(modeSelect, texts.modeOptions);

    const imageFormSection = getElem('imageFormSection');
    imageFormSection.innerHTML = '';

    SELECT_DATA.forEach(item => {
        const formGroup = document.createElement('div');
        formGroup.className = 'form-group';

        const label = document.createElement('label');
        label.setAttribute('for', item.selectId);
        label.textContent = texts[item.labelId];

        const select = document.createElement('select');
        select.id = item.selectId;

        createSelect(select, texts[item.options]);

        formGroup.appendChild(label);
        formGroup.appendChild(select);
        imageFormSection.appendChild(formGroup);
    });
}

// Selectデータ
const SELECT_DATA = [
    { labelId: 'subjectLabel', selectId: 'subject', options: 'subjectOptions' },
    { labelId: 'styleLabel', selectId: 'style', options: 'styleOptions' },
    { labelId: 'lightingLabel', selectId: 'lighting', options: 'lightingOptions' },
    { labelId: 'colorLabel', selectId: 'color', options: 'colorOptions' },
    { labelId: 'atmosphereLabel', selectId: 'atmosphere', options: 'atmosphereOptions' },
    { labelId: 'artistLabel', selectId: 'artist', options: 'artistOptions' },
    { labelId: 'qualityLabel', selectId: 'quality', options: 'qualityOptions' },
    { labelId: 'perspectiveLabel', selectId: 'perspective', options: 'perspectiveOptions' },
    { labelId: 'textureLabel', selectId: 'texture', options: 'textureOptions' },
    { labelId: 'seasonLabel', selectId: 'season', options: 'seasonOptions' }
];

// Selectタグ生成
function createSelect(selectElement, options) {
    selectElement.innerHTML = '';
    options.forEach(optionData => {
        const option = document.createElement('option');
        option.value = optionData.value;
        option.textContent = optionData.text;
        selectElement.appendChild(option);
    });
}

// コンテンツ生成
function generateContent() {
    const mode = getElem('generationMode').value;
    const subject = getElem('subject').value;
    const style = getElem('style').value;
    const lighting = getElem('lighting').value;
    const color = getElem('color').value;
    const atmosphere = getElem('atmosphere').value;
    const artist = getElem('artist').value;
    const quality = getElem('quality').value;
    const perspective = getElem('perspective').value;
    const texture = getElem('texture').value;
    const season = getElem('season').value;
    const additionalPrompt = getElem('additionalPrompt').value;

    let mode_ja = "テキスト";
    if (mode === MODE_IMG) {
        mode_ja = "イメージ";
    }

    let basePrompt = `${subject}、${style}、${lighting}、${color}、${atmosphere}、${artist}風、${quality}、${perspective}、${texture}、${season}`;
    if (additionalPrompt) {
        basePrompt += `、${additionalPrompt}`;
    }
    const prompt = `
        以下の内容に基づいて、「${mode_ja}」を生成してください。
        ${basePrompt}、${commonConditions_text}
    `;

    requestApi(mode, prompt);
}

// APIリクエスト
async function requestApi(mode, prompt) {
    const requestBody = { mode: mode, prompt: prompt };

    try {
        const data = await getFetchApiData(apiUrl, requestBody);
        console.log(data.message);
        alert(MSG_OK_SEND);

        const outputImageContainer = getElem('outputImageContainer');
        const generatedImage = getElem('generatedImage');
        const outputTextContainer = getElem('outputTextContainer');
        const generatedText = getElem('generatedText');
        const copyTextButton = getElem('copyTextButton');

        if (mode === MODE_IMG) {
            generatedImage.src = imgUrl;
            generatedImage.style.display = ATTR_BLOCK;
            outputImageContainer.style.display = ATTR_BLOCK;
            outputTextContainer.style.display = ATTR_NONE;

        } else {
            generatedText.textContent = msg;
            generatedText.style.display = ATTR_BLOCK;
            copyTextButton.style.display = ATTR_BLOCK;
            outputTextContainer.style.display = ATTR_BLOCK;
            outputImageContainer.style.display = ATTR_NONE;
        }

    } catch (error) {
        console.error('エラー:', error);
        alert('コンテンツ生成中にエラーが発生しました。');
    }
}

// テキストコピー
async function copyText() {
    const textElement = getElem('generatedText');
    if (!textElement.textContent) {
        alert('テキストがありません。');
        return;
    }

    try {
        await navigator.clipboard.writeText(textElement.textContent);
        alert('テキストをコピーしました！');
    } catch (err) {
        console.error('テキストのコピーに失敗しました:', err);
        alert('テキストのコピーに失敗しました。');
    }
}
