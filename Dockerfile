# ベースイメージ設定
FROM python:3.13

# 作業ディレクトリ設定
WORKDIR /bot

# 必要なパッケージ更新・インストールし、日本語ロケール設定
RUN apt-get update && apt-get -y install locales chromium && apt-get -y upgrade && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8

# 環境変数設定
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ Asia/Tokyo
ENV TERM xterm
ENV PYTHONPATH /bot

# 実行権限付与
RUN chmod +x /usr/bin/chromium

# 必要なパッケージをpipでインストール
COPY requirements.txt /bot/
RUN pip install -r requirements.txt

# ソースコードをコンテナ内にコピー
COPY . /bot

# ポート開放（uvicornで指定したポート）
EXPOSE 8000

# アプリケーションを実行
CMD ["python", "apps/main.py"]
