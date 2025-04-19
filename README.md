# bot-repo

LINE Messaging API Bot

## Python ライブラリ

| カテゴリー             | ライブラリ          | 説明                            |
| ---------------------- | ------------------- | ------------------------------- |
| **HTTP リクエスト**    | requests            | HTTP 通信                       |
| **Web フレームワーク** | fastapi             | 高速な Web フレームワーク       |
|                        | starlette           | 非同期 Web サーバー             |
|                        | uvicorn             | 高速 ASGI（非同期処理）サーバー |
| **データ解析**         | pandas              | データ解析と操作                |
| **Web スクレイピング** | bs4 (BeautifulSoup) | HTML スクレイピング             |
| **テンプレート**       | jinja2              | HTML テンプレートエンジン       |
| **画像処理**           | Pillow              | 画像操作                        |
| **セキュリティ**       | itsdangerous        | 安全なデータ署名                |
| **環境変数管理**       | python-dotenv       | 環境変数の簡単な管理            |
| **データベース操作**   | pymongo             | MongoDB 操作                    |
| **スケジューリング**   | schedule            | タスクスケジューラ              |
| **AI と機械学習**      | google-genai        | Google の生成 AI ツール         |
| **ファイル管理**       | python-multipart    | マルチパートデータ処理          |

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
| NUM_MIN_HOURLY_JOB  | 30                |
| NUM_SEC_NO_SLEEP    | 600               |
| URL_KOYEB           | https://koyeb.app |

### 公開サーバ

```
https://kobe-dev.koyeb.app/
```

## 参考 URL

```
https://zenn.dev/amano_spica/articles/24c5f288cf9595/
```
