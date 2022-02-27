# Проект анализатора опросников врачей

### Локальное развертывание

Развернуть виртуальное окружение python

Накатить миграции на чистую базу (для простоты тут используется SQLite)
Особенности запуска см. ниже

- HTTP API version with rabbitmq
    - **\<your venv\>/gunicorn questionnaire.composites.http_api.py:app \<other
      args\>** - запуск
    - Переменные окружения
        - **DATABASE_PATHNAME** - URL подключения к файлу БД SqLite
        - **RABBIT_USER** - имя пользователя для подключения к брокеру сообщений RabbitMQ
        - **RABBIT_PASS** - пароль пользователя RabbitMQ
        - **RABBIT_HOST** - адрес RabbitMQ
        - **RABBIT_PORT** - порт для подключения к брокеру сообщений
        - **LOGGING_LEVEL** [default=INFO] - уровень логгирования
        - **LOGGING_JSON [default=True]** - нужны ли логи в формате JSON
        - **SA_LOGS** [default=False] - нужны ли логи SqlAlchemy
        - **EMAIL_USER** - имя пользователя e-mail
        - **EMAIL_PASS** - пароль на e-mail
        - **EMAIL_ADDRESS** - адрес почтового ящика отправителя
        - **EMAIL_SMTP_PORT** - smtp стандартный порт
        - **EMAIL_SERVER** - адрес e-mail сервера отправителя
        - **STORAGE_PATH** - путь к папке с хранилищем отчетов
        - **LOCAL_TZ** - указание временной зоны приложения
        - **ALLOW_ORIGINS_LIST [default=()]** - CORS домены
        - **IS_DEV_MODE [default=False]** - пропускает запросы со всех доменов
- Worker
    - **python -m questionnaire.composites.worker** - запуск консьюмера
      сообщений
    - Переменные окружения
        - **DATABASE_PATHNAME** - URL подключения к файлу БД SqLite
        - **RABBIT_USER** - имя пользователя для подключения к брокеру сообщений RabbitMQ
        - **RABBIT_PASS** - пароль пользователя RabbitMQ
        - **RABBIT_HOST** - адрес RabbitMQ
        - **RABBIT_PORT** - порт для подключения к брокеру сообщений
        - **LOGGING_LEVEL** [default=INFO] - уровень логгирования
        - **LOGGING_JSON [default=True]** - нужны ли логи в формате JSON
        - **SA_LOGS** [default=False] - нужны ли логи SqlAlchemy
        - **EMAIL_USER** - имя пользователя e-mail
        - **EMAIL_PASS** - пароль на e-mail
        - **EMAIL_ADDRESS** - адрес почтового ящика отправителя
        - **EMAIL_SMTP_PORT** - smtp стандартный порт
        - **EMAIL_SERVER** - адрес e-mail сервера отправителя
        - **STORAGE_PATH** - путь к папке с хранилищем отчетов
        - **LOCAL_TZ** - указание временной зоны приложения
- Migrations
    - **python -m alembic \<other args\>** - запуск
    - Переменные окружения
        - **DATABASE_PATHNAME** - URL подключения к файлу БД SqLite
        - **LOGGING_LEVEL** [default=INFO] - уровень логгирования
        - **LOGGING_JSON [default=True]** - нужны ли логи в формате JSON
        - **SA_LOGS** [default=False] - нужны ли логи SqlAlchemy

### Развертывание в контейнере

Изучить Dockerfile в каталоге развертывания, собрать контейнер с необходимой
командой запуска (выбрать нужный entrypoint.sh)
Единицы запуска смотрите выше

### Логирование

По дефолту уровень логирования - INFO, формат - JSON

### Тесты

тестов пока нет 🤷