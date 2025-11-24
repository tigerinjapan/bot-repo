# bot-repo

Messaging API Bot

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
| **スケジューリング**   | schedule            | タスクスケジューラ              |
| **データベース操作**   | pymongo             | MongoDB 操作                    |
| **環境変数管理**       | python-dotenv       | 環境変数の簡単な管理            |
| **ファイル管理**       | python-multipart    | マルチパートデータ処理          |
| **画像処理**           | Pillow              | 画像操作                        |
| **セキュリティ**       | itsdangerous        | 安全なデータ署名                |
| **AI と機械学習**      | google-genai        | Google の生成 AI ツール         |

## Koyeb サーバ

### 環境変数：Koyeb にて登録

| 変数                  | 値                  | 備考                                 |
| --------------------- | ------------------- | ------------------------------------ |
| PYTHONPATH            | bot                 | -                                    |
| GEMINI_API_KEY        | api_key             | -                                    |
| KAKAO_API_KEY         | kakao client id     | -                                    |
| KAKAO_API_SECRET      | kakao client secret | -                                    |
| LINE_CHANNEL_ID       | channel id          | -                                    |
| LINE_CHANNEL_SECRET   | channel secret      | -                                    |
| LINE_CHANNEL_ID_2     | channel id2         | -                                    |
| LINE_CHANNEL_SECRET_2 | channel secret2     | -                                    |
| GEMINI_MODEL          | latest model name   | -                                    |
| GEMINI_MODEL_IMG      | latest model name   | -                                    |
| LINE_IMG_DIV          | 1                   | -                                    |
| MIN_HOURLY_JOB        | :05                 | -                                    |
| NUM_SEC_NO_SLEEP      | 600                 | 1 時間トラフィックないとスリーブ状態 |
| TIME_DAILY_JOB_1      | 00:00               | -                                    |
| TIME_DAILY_JOB_2      | 07:10               | -                                    |
| TIME_DAILY_JOB_3      | 09:00               | -                                    |
| TIME_DAILY_JOB_4      | 18:30               | -                                    |
| TIME_WEEKLY_JOB       | 09:00               | -                                    |
| URL_KOYEB             | https://koyeb.app   | -                                    |

## 参考 URL

```
https://zenn.dev/amano_spica/articles/24c5f288cf9595/
```
