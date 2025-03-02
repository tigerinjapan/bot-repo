# bot-repo

LINE Messaging API Bot

## Python ライブラリ

| ライブラリ    | 説明                        |
| ------------- | --------------------------- |
| requests      | HTTP リクエスト処理         |
| fastapi       | 高速 API フレームワーク     |
| uvicorn       | 高速 ASGI(非同期処理)サーバ |
| bs4           | HTML/XML 解析ツール         |
| jinja2        | HTML テンプレートエンジン   |
| schedule      | タスク定期実行              |
| python-dotenv | 環境変数管理                |
| Pillow        | 画像処理ライブラリ          |
| google-genai  | Google の AI ツール         |

## Koyeb サーバ

### 環境変数：Koyeb にて、secret 登録

| 変数                | 値                |
| ------------------- | ----------------- |
| PYTHONPATH          | bot               |
| LINE_CHANNEL_ID     | channel_id        |
| LINE_CHANNEL_SECRET | channel_secret    |
| GEMINI_API_KEY      | api_key           |
| JOB_SCHEDULE_TIME   | 07:00             |
| URL_KOYEB           | https://koyeb.app |

### 公開サーバ

```
https://raspy-ranique-kobe-dev-abf65738.koyeb.app/
```

## 参考 URL

```
https://zenn.dev/amano_spica/articles/24c5f288cf9595/
```
