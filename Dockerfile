# ベースイメージ設定
FROM python:3.13

# 作業ディレクトリ設定
WORKDIR /bot

# 環境変数設定
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ Asia/Tokyo
ENV TERM xterm
ENV PYTHONPATH /bot

# ソースコードをコンテナ内にコピー
COPY . /bot

# pipアップグレード
RUN pip install --upgrade pip

# 必要なパッケージのインストール
RUN pip install -r requirements.txt

# ポート開放（uvicornで指定したポート）
EXPOSE 8000

# アプリケーションを実行
CMD ["python", "apps/main.py"]
