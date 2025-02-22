## Linux Command for Koyeb

| コマンド            | 説明                  |
| ------------------- | --------------------- |
| printenv PYTHONPATH | 環境変数の確認        |
| python --version    | python バージョン確認 |

## ChromeDriver のダウンロード

# wget https://chromedriver.storage.googleapis.com/最新バージョン/chromedriver_linux64.zip

## ダウンロードしたファイルを解凍

# unzip chromedriver_linux64.zip

## ChromeDriver を適切なディレクトリに配置

# sudo mv chromedriver /usr/local/bin

## 権限の設定

```
sudo chmod +x input/chromedriver
```

## ChromeDriver のパスをシステムの PATH に追加

```
export PYTHONPATH=$PYTHONPATH:/bot
```

## 確認用の Python スクリプトを実行

```
python3 -c "
from selenium import webdriver
driver = webdriver.Chrome()
driver.get('https://www.google.com')
print(driver.title)
driver.quit()
"
```
