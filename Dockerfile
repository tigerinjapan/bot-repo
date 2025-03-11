# ベースイメージ設定
FROM python:3.13

# 作業ディレクトリ設定
WORKDIR /bot

# 必要なパッケージ更新・インストールし、日本語ロケール設定
RUN apt-get update && apt-get -y install locales && apt-get -y upgrade && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8

# RUN apt-get update && apt-get -y install --only-upgrade chromium

# 環境変数設定
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ Asia/Tokyo
ENV TERM xterm
ENV PYTHONPATH /bot

# 実行ファイルの権限設定
RUN chmod +x /usr/local/bin/chromedriver
RUN chmod +x /usr/bin/chromium

# ソースコードをコンテナ内にコピー
COPY . /bot

# 必要なパッケージのインストール
RUN pip install -r requirements.txt

# ポート開放（uvicornで指定したポート）
EXPOSE 8000

# アプリケーションを実行
CMD ["python", "apps/main.py"]
