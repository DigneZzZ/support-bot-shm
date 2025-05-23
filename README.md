

# 🤖 Support Bot SHM

## Описание
Бот поддержки пользователей с поддержкой топиков в группе


<details><summary><b>Возможности</b></summary>
1. Поддержка топиков

2. Управление обращениями
    >`/close - закрыть обращение`
    >`/open - открыть обращение`

3. Информация о пользователе и его услугах из SHM (нужен шаблон bot_api, см. ниже)
    >`/information - информация`

4. Каждые 3 часа в general топик группы отправляется сводка по новым обращениям
    >`/summary - получить сводку (работает только в general)`

5. BUMP топика каждые 2 часа
    >Каждые 2 часа в новые и открытые топики отправляется BUMP
    >Сделано это для того, чтобы не потерять обращение
</details>

---

## Установка

1. В SHM создай новый шаблон [bot_api](https://github.com/alfirovich/marzban-bot/blob/dev/misc/bot_api.tt)

2. Скачай `docker-compose.yml` и `.env` с помощью `curl`:

    ```bash
    curl -o docker-compose.yml https://raw.githubusercontent.com/DigneZzZ/support-bot-shm/refs/heads/dev/docker-compose.yml
    curl -o .env https://raw.githubusercontent.com/DigneZzZ/support-bot-shm/refs/heads/dev/sample.env
    ```

3. Настрой переменные в `.env`:

    ```bash
    nano .env
    ```

    Заполни `BOT_TOKEN`, `GROUP_CHAT_ID` и другие параметры.

4. Запусти бота:

    ```bash
    docker compose pull
    docker compose up -d
    ```

## Переменные окружения

| Переменная         | Описание                                  | Пример значения          |
|--------------------|-------------------------------------------|--------------------------|
| `BOT_DEV_ID`       | ID администратора бота                    | `1927996831`             |
| `BOT_EMOJI_ID`     | Кастомный emoji (опционально)             | (пусто или ID эмодзи)    |
| `REDIS_HOST`       | Хост Redis                                | `redis`                  |
| `REDIS_PORT`       | Порт Redis                                | `6379`                   |
| `REDIS_DB`         | БД Redis                                  | `0`                      |
| `BOT_TOKEN`        | Токен бота (получи у @BotFather)          | `***********`            |
| `BOT_GROUP_ID`     | ID группы                                 | `-100*******`            |
| `API_URL`          | Ссылка на шаблон SHM                         | `https://admin.example.com/shm/v1/public/bot_api` |
| `BOT_USERNAME`     | Юзернейм бота (без @)                     | `YOUR_BOT_USERNAME`      |
| `BOT_NAME`         | Название проекта / бота                     | `My Project name`      |



---

### Fork
**Based on [nessshon/support-bot](https://github.com/nessshon/support-bot)**
