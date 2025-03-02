from contextlib import suppress
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.markdown import hbold
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from app.bot.manager import Manager
from app.bot.utils.texts import SUPPORTED_LANGUAGES
from app.bot.utils.api import fetch_services, fetch_user_data
from app.bot.utils.redis.models import UserData
from app.bot.manager import Form
import base64
from app.bot.utils.redis import RedisStorage


class Window:
    """
    Window class.
    """

    @staticmethod
    async def menu_of_user(manager: Manager, message: Message, redis: RedisStorage) -> None:
        """
        Main of user
        :param manager: Manager object.
        :return: None
        """
        user_data = await redis.get_by_message_thread_id(message.message_thread_id)
        api_data = await fetch_user_data(user_login=user_data.id)
        services = await fetch_services(user_login=user_data.id)

        builder = InlineKeyboardBuilder()
        user_id = base64.b64encode(f"userID={api_data['user_id']}".encode()).decode()

        if api_data is None:
            api_data = []

        if services is None:
            services = [] 


        builder.row(
            InlineKeyboardButton(text="ℹ️ Информация о пользователе", url=f"https://t.me/{manager.config.api.BOT_USERNAME}?start={user_id}"),
        )

        for service in services:
            encoded_url = base64.b64encode(f"userID={api_data['user_id']}&serviceID={service['user_service_id']}".encode()).decode()
            builder.row(
                InlineKeyboardButton(text=f"🔑 #{service['user_service_id']} {service['name']}", url=f"https://t.me/{manager.config.api.BOT_USERNAME}?start={encoded_url}"),
            )

        message_text = (f"<b>Информация о пользователе</b>\n"
                    f"🆔 ID: {api_data['user_id']}\n"
                    f"💸 Баланс: {api_data['balance']}\n"
                    f"🏷️ Скидка: {api_data['discount']}%\n"
                    f"🗓️ Зарегистрирован: {api_data['created']}\n"
                    f"⏱️ Последнее пользование: {api_data['last_login']}\n"
                    f"🏷️ Партнерская скидка: {api_data.get('settings', {}).get('partner', {}).get('discount', 0)}%"
                    )

        await message.reply(
            text=message_text,
            reply_markup=builder.as_markup(),
        )