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
| GEMINI_API_KEY      | api_key           |
| GEMINI_MODEL        | model_name        |
| LINE_CHANNEL_ID     | channel_id        |
| LINE_CHANNEL_SECRET | channel_secret    |
| LINE_IMG_DIV        | 1                 |
| NUM_HOUR_DAILY_JOB  | 7                 |
| NUM_MIN_HOURLY_JOB  | 55                |
| NUM_MIN_NO_SLEEP    | 30                |
| URL_KOYEB           | https://koyeb.app |

### 公開サーバ

```
https://kobe-dev.koyeb.app/
```

## 参考 URL

```
https://zenn.dev/amano_spica/articles/24c5f288cf9595/
```
