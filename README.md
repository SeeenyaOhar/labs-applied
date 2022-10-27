# labs-applied
#### Репозиторій з виконаними лабораторними роботами 
#### Arsenii Ohar КН-215
# How to use
### Requirements:
- Python 3.7
- [Poetry Virtual Environment Package](https://python-poetry.org/docs/)
## Installing poetry
To install poetry virtual environment package, you should read the documentation first.<br>
https://python-poetry.org/docs/
## Installing poetry packages
```
cd labs-applied
```
Then, just use this command to install all required packages.
```
poetry install
```

## Розгортання сервера
Для розгортання потрібно виконати команду:
```
waitress-serve --host 127.0.0.1 hello:app
``` 
## Тести
Для тестування я виконував <b>cURL</b> запити.
Наприклад, ось цей запит видає status code запросу(200) при піднятому сервері.
```
curl -I http://127.0.0.1:8080/api/v1/hello-world-19
```
```
HTTP/1.1 200 OK
Content-Length: 15
Content-Type: text/html; charset=utf-8
Date: Thu, 29 Sep 2022 14:45:03 GMT
Server: waitress
```