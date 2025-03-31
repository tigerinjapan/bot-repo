# エラー区分：パス設定

## エラー内容

`ModuleNotFoundError: No module named 'com'`

### 対応：環境変数の追加

| 変数名     | 変数値                |
| ---------- | --------------------- |
| PYTHONPATH | C:\workspace\bot-repo |

# エラー区分：仮想環境（.venv）

## エラー内容

フレームワークが未インストールされている状態で、実行できない

### 対応

仮想環境を削除し、再作成

# 【Selenium, Playwright】koyeb server

## エラー内容

無料プランのサーバーだと、性能の問題で、実行できない

### 対応

無料プランに可能になるまで、待ち

# 【Selenium】Chrome ドライバー・バージョン・エラー

## エラー内容

`selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable needs to be in PATH.`

### 対応

1. chrome ブラウザ・アップデート

```
chrome://settings/help
```

2. ライブラリ・アップグレード
