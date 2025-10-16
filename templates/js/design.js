// ヘッダー設定
setElemContentsByTag(TAG_HEAD, CONTENTS_HEAD_2);

// タイトル設定
document.title = TITLE_DESIGN;

// DOM読み込み後の初期化処理
document.addEventListener("DOMContentLoaded", init);

// 初期表示
function init() {
  // アプリ名
  const appName = getElemText("appName");

  // マークダウンファイルのパス
  const markdownFilePath = `/templates/${appName}.md`;

  // 表示先のDOM要素
  const markdownContainer = getElem('markdown-container');

  // fetch APIを使ってファイルを読み込む関数
  async function loadMarkdown() {
    try {
      // ファイルを取得
      const response = await fetch(markdownFilePath);

      // ネットワークエラーなどをチェック
      if (!response.ok) {
        const errMsg = `HTTP error! status: ${response.status}`
        alert(errMsg);
        throw new Error(errMsg);
      }

      // テキストとしてレスポンスを取得
      const markdownText = await response.text();

      // marked.jsを使ってマークダウンをHTMLに変換
      const htmlContent = marked.parse(markdownText);

      // 1. 文字列をDOM要素に変換するための「コンテナ」を作成
      const tempContainer = createElemOnly(TAG_DIV);
      tempContainer.innerHTML = htmlContent;

      // 2. コンテナの中から 全ての a タグを取得
      const anchorTags = tempContainer.querySelectorAll(TAG_A);

      // 3. a タグのリストを一つずつ取り出し、target="_blank"（別タブへ遷移）を追加
      if (0 < anchorTags.length) {
        anchorTags.forEach(anchorTag => {
          anchorTag.setAttribute('target', '_blank');
        });
      }

      // 4. 変更後のHTML文字列を取得
      const updatedHtmlContents = tempContainer.innerHTML.trim();

      // コンテナにHTMLを挿入
      markdownContainer.innerHTML = updatedHtmlContents;

    } catch (error) {
      // エラー処理
      console.error('Failed to load markdown file:', error);
      markdownContainer.innerHTML = '<p>ファイルの読み込みに失敗しました。</p>';
    }
  }

  // 関数を実行
  loadMarkdown();
}