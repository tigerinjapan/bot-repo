# ベースイメージ設定
FROM python:3.13

# 作業ディレクトリ設定
WORKDIR /bot

# 必要なパッケージ更新・インストールし、日本語ロケール設定
RUN apt-get update && apt-get -y install locales unzip && apt-get -y upgrade && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8

# 環境変数設定
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ Asia/Tokyo
ENV TERM xterm
ENV PYTHONPATH /bot
ENV CHROME_DRIVER_VERSION 114.0.5735.90
ENV PATH=$PATH:/root/.wdm/drivers/chromedriver/linux64/${CHROME_DRIVER_VERSION}/chromedriver

# chromedriverダウンロード、解凍し、適切な場所に移動
RUN wget https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip
RUN unzip /bot/chromedriver_linux64.zip
RUN mkdir -p /root/.wdm/drivers/chromedriver/linux64/${CHROME_DRIVER_VERSION}/
RUN mv /bot/chromedriver /root/.wdm/drivers/chromedriver/linux64/${CHROME_DRIVER_VERSION}/
RUN chmod +x /root/.wdm/drivers/chromedriver/linux64/${CHROME_DRIVER_VERSION}/chromedriver
RUN ls -la /root/.wdm/drivers/chromedriver/linux64/${CHROME_DRIVER_VERSION}/
RUN rm -r /bot/chromedriver_linux64.zip

# 必要なパッケージをpipでインストール
COPY requirements.txt /bot/
RUN pip install -r requirements.txt

# ソースコードをコンテナ内にコピー
COPY . /bot

# ポート開放（uvicornで指定したポート）
EXPOSE 8080

# アプリケーションを実行
CMD ["python", "apps/main.py"]
