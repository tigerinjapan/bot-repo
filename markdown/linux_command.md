## Linux Command for Koyeb

| コマンド            | 説明                  |
| ------------------- | --------------------- |
| printenv PYTHONPATH | 環境変数の確認        |
| python --version    | python バージョン確認 |

## Git のインデックスから削除する

### フォルダの場合

```
git rm --cached -r example_folder
```

### ファイルの場合

```
git rm --cached file.py
```

## ChromeDriver のパスをシステムの PATH に追加

```
export PATH=$PATH:/usr/local/bin/chromedriver
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
