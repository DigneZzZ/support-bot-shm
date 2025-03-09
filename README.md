

# 🤖 Support Bot SHM

## Описание
Бот поддержки пользователей с поддержкой топиков в группе

## Установка

1. В SHM создай новый шаблон [bot_api](https://github.com/alfirovich/marzban-bot/blob/dev/misc/bot_api.tt)

2. Скачай `docker-compose.yml` и `.env` с помощью `curl`:

    ```bash
    curl -o docker-compose.yml https://raw.githubusercontent.com/alfirovich/support-bot-shm/refs/heads/dev/docker-compose.yml
    curl -o .env https://raw.githubusercontent.com/alfirovich/support-bot-shm/refs/heads/dev/sample.env
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
| `REDIS_PORT`       | Порт Redis                                | `6377`                   |
| `REDIS_DB`         | Номер базы данных Redis                   | `0`                      |
| `BOT_TOKEN`        | Токен бота (получи у @BotFather)          | `***********`            |
| `BOT_GROUP_ID`     | ID группы, где работает бот               | `-100*******`            |
| `API_URL`          | Ссылка на шаблон SHM                         | `https://admin.example.com/shm/v1/public/bot_api` |
| `BOT_USERNAME`     | Юзернейм бота (без @)                     | `YOUR_BOT_USERNAME`      |



---

### Fork
**Based on [nessshon/support-bot](https://github.com/nessshon/support-bot)**