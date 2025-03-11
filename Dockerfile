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
ENV CHROME_DRIVER_FILE chromedriver-linux64
ENV CHROME_DRIVER_ZIP ${CHROME_DRIVER_FILE}.zip
ENV CHROME_DRIVER_VERSION 133.0.6943.126
ENV CHROME_DRIVER_PATH /usr/bin/
ENV PATH=$PATH:${CHROME_DRIVER_PATH}chromium:${CHROME_DRIVER_PATH}chromedriver

# ChromeDriverダウンロード、解凍し、適切な場所に移動
RUN wget https://storage.googleapis.com/chrome-for-testing-public/${CHROME_DRIVER_VERSION}/linux64/${CHROME_DRIVER_ZIP}
RUN unzip /bot/${CHROME_DRIVER_ZIP}
# RUN mkdir -p ${CHROME_DRIVER_PATH}

RUN mv /bot/${CHROME_DRIVER_FILE}/chromedriver ${CHROME_DRIVER_PATH}

# zipファイル削除
RUN rm -r /bot/${CHROME_DRIVER_ZIP}

# 実行ファイルの権限設定
RUN chmod +x ${CHROME_DRIVER_PATH}chromedriver
RUN chmod +x ${CHROME_DRIVER_PATH}chromium

# ソースコードをコンテナ内にコピー
COPY . /bot

# 必要なパッケージのインストール
RUN pip install -r requirements.txt

# ポート開放（uvicornで指定したポート）
EXPOSE 8000

# アプリケーションを実行
CMD ["python", "apps/main.py"]
