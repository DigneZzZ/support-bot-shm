from contextlib import suppress
from typing import Any, Dict, Optional

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

from app.bot.utils.redis import RedisStorage
from app.bot.utils.redis.models import UserData


class TopicManager:
    """
    Класс для управления топиками.
    """

    def __init__(self, bot: Bot, redis: RedisStorage, config: Any) -> None:
        """
        Инициализация TopicManager.

        :param bot: Объект бота.
        :param redis: RedisStorage.
        :param config: Конфигурация бота.
        """
        self.bot = bot
        self.redis = redis
        self.config = config

    async def close_topic(self, message: Message, user_data: UserData) -> None:
        """
        Закрывает топик.

        :param message: Объект сообщения.
        :param user_data: Данные пользователя.
        :return: None
        """

        new_name = f"⭕️ {user_data.full_name}"
        try:
            user_data.topic_status = "closed"
            await self.redis.update_user(user_data.id, user_data)

            await self.bot.edit_forum_topic(
                chat_id=self.config.bot.GROUP_ID,
                message_thread_id=user_data.message_thread_id,
                name=new_name,
            )

            await self.bot.close_forum_topic(
                chat_id=self.config.bot.GROUP_ID,
                message_thread_id=user_data.message_thread_id
            )


        except TelegramBadRequest as ex:
            if "TOPIC_NOT_MODIFIED" in ex.message:
                print(f"{ex}")
                pass

    async def open_topic(self, message: Message, user_data: UserData) -> None:
        """
        Открывает топик.

        :param message: Объект сообщения.
        :param user_data: Данные пользователя.
        :return: None
        """

        new_name = f"🟢 {user_data.full_name}"
        try:
            await self.bot.edit_forum_topic(
                chat_id=self.config.bot.GROUP_ID,
                message_thread_id=user_data.message_thread_id,
                name=new_name,
            )
            
            await self.bot.reopen_forum_topic(
                chat_id=self.config.bot.GROUP_ID,
                message_thread_id=user_data.message_thread_id
            )

            user_data.topic_status = "open"
            await self.redis.update_user(user_data.id, user_data)
        except TelegramBadRequest as ex:
            if "TOPIC_NOT_MODIFIED" in ex.message:
                pass

    async def new_topic(self, message: Message, user_data: UserData) -> None:
        """
        Новый топик.

        :param message: Объект сообщения.
        :param user_data: Данные пользователя.
        :return: None
        """

        new_name = f"🆕 {user_data.full_name}"
        try:
            user_data.topic_status = "new"
            await self.redis.update_user(user_data.id, user_data)
            await self.bot.edit_forum_topic(
                chat_id=self.config.bot.GROUP_ID,
                message_thread_id=user_data.message_thread_id,
                name=new_name,
            )

            await self.bot.close_forum_topic(
                chat_id=self.config.bot.GROUP_ID,
                message_thread_id=user_data.message_thread_id
            )
        except TelegramBadRequest as ex:
            if "TOPIC_NOT_MODIFIED" in ex.message:
                pass