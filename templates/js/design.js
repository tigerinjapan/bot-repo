// ヘッダー設定
getElemByTag(TAG_HEAD).innerHTML = CONTENTS_HEAD_2;

// DOM読み込み後の初期化処理
document.addEventListener("DOMContentLoaded", () => {
  // タイトル設定
  document.title = "📄設計書";

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
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // テキストとしてレスポンスを取得
      const markdownText = await response.text();

      // marked.jsを使ってマークダウンをHTMLに変換
      const htmlContent = marked.parse(markdownText);

      // コンテナにHTMLを挿入
      markdownContainer.innerHTML = htmlContent;

    } catch (error) {
      // エラー処理
      console.error('Failed to load markdown file:', error);
      markdownContainer.innerHTML = '<p>ファイルの読み込みに失敗しました。</p>';
    }
  }

  // 関数を実行
  loadMarkdown();
});