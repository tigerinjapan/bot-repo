FROM python:3.13
WORKDIR /bot

# 更新・日本語化
RUN apt-get update && apt-get -y install locales unzip && apt-get -y upgrade && \
	localedef -f UTF-8 -i ja_JP ja_JP.UTF-8

# 環境変数
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ Asia/Tokyo
ENV TERM xterm
ENV PYTHONPATH /bot

RUN wget https://storage.googleapis.com/chrome-for-testing-public/133.0.6943.126/linux64/chromedriver-linux64.zip
CMD unzip /bot/chromedriver_linux64.zip
CMD mv /bot/chromedriver /usr/local/bin
CMD chmod +x /usr/local/bin/chromedriver
ENV PYTHONPATH /usr/local/bin/chromedriver

# pip install
COPY requirements.txt /bot/
RUN pip install -r requirements.txt
COPY . /bot

# ポート開放 (uvicornで指定したポート)
EXPOSE 8080

# 実行
CMD python apps/main.py