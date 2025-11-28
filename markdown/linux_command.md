# Linux Command

## Basic

| command  | description                     |
| -------- | ------------------------------- |
| date     | print or set the system date    |
| id       | print user identity information |
| uname -a | print all system information    |
| whoami   | print current username          |
| hostname | print system host name          |
| w        | print active users              |
| pwd      | print current directory path    |

## ls options

| command | description |
| ------- | ----------- |
| ls -l   | details     |
| ls -a   | all         |
| ls -t   | time        |
| ls -S   | size        |
| ls -X   | extension   |
| ls -r   | reverse     |

## curl options

### auth

```
curl -user <USER_ID>:<PASSWORD> <URL>
```

### print log

```
curl -v <URL>
```

### ignore SSL error

```
curl -k <URL>
```

### print data to file

```
curl -o <OUTPUT_PATH> <URL>
```

### download file

```
curl -O <URL>/<FILE_PATH>
```

## Linux Command for Koyeb

| command             | description          |
| ------------------- | -------------------- |
| printenv PYTHONPATH | print python path    |
| python --version    | print python version |

## Remove git index

### remove from folder

```
git rm --cached -r example_folder
```

### remove from file

```
git rm --cached file.py
```

## Add ChromeDriver Path

```
export PATH=$PATH:/usr/local/bin/chromedriver
```

## Python Script

```
python3 -c "
from selenium import webdriver
driver = webdriver.Chrome()
driver.get('https://www.google.com')
print(driver.title)
driver.quit()
"
```
