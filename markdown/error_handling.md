# エラー対応

## パス設定

### 内容

`ModuleNotFoundError: No module named 'com'`

### 対応：環境変数の追加

| 変数名     | 変数値                |
| ---------- | --------------------- |
| PYTHONPATH | C:\workspace\bot-repo |

## 仮想環境 (.venv)

### 内容

フレームワークが未インストールされている状態で、実行できない

### 対応

仮想環境を削除し、再作成

## キャッシュ削除

### パス

C:\Users\(ユーザー名)\AppData\Roaming\Code\Cache

### 対応

定期的に削除 (今後バッチ化)

## 【Selenium, Playwright】Koyeb server

### エラー内容

無料プランのサーバーだと、性能の問題で、実行できない

### 対応

無料プランで実行できるまで、待ち

## 【Selenium】Chrome ドライバー・バージョン・エラー

### 内容

`selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable needs to be in PATH.`

### 対応

1. chrome ブラウザ・アップデート

```
chrome://settings/help
```

2. ライブラリ・アップグレード
