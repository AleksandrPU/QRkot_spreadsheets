# Приложение QRkot_spreadseets для благотворительного фонда поддержки котиков

## Описание:

Учебный проект по изучению фреймворка [FastAPI](https://fastapi.tiangolo.com/) и 
асинхронного клиента Google API [Aiogoogle](https://aiogoogle.readthedocs.io/).

Приложение позволяет создавать и отслеживать целевые проекты. Для каждого проекта можно задать название, описание и 
требуемую сумму пожертвований. Создавать проекты могут только суперпользователи.
После сбора требуемой суммы проект закрывается.

Зарегистрированные пользователи могут создавать пожертвования. При создании пожертвования можно оставить комментарий.

Проекты и пожертвования распределяются по принципу First In, First Out.

Суперпользователям доступно формирование отчёта о завершённых проектах в Google 
Docs Spreadsheet (необходимо заполнить параметры для Google API в .env).

## Использование:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:AleksandrPU/cat_charity_fund.git
```

```
cd cat_charity_fund
```

Создать и активировать виртуальное окружение:

```
python3.9 -m venv venv
```

**ВНИМАНИЕ!** Необходимо использовать Python версии 3.9.

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Создать базу данных для приложения:

```
alembic upgrade head                                                                                                                         [shadow:mynote]
```

Скопировать файл ```env.example``` в файли ```.env```. Задать в файле ```.env``` секретный ключ ```SECRET```, а также 
логин и пароль для суперпользователя.
Значение ```SECRET``` можно сгенерировать командой:

```
python -c 'import secrets; print(secrets.token_hex())'
```

Запустить проект:

```
uvicorn app.main:app
```

По умолчанию приложение запустится по адресу [http://localhost:8000](http://localhost:8000).

При первом запуске приложение создаст суперпользователя с логином и паролем, указанными в файле ```.env```.

Посмотреть эндпойнты приложения можно по адресу [https://localhost:8000/api/docs/](https://localhost:8000/api/docs/) 
или [https://localhost:8000/api/redoc/](https://localhost:8000/api/redoc/).

## Автор:

Проект создан Паутовым Александром на основе репозитория 
[yandex-praktikum/QRkot_spreadsheets](https://github.com/yandex-praktikum/QRkot_spreadsheets).
