from contextlib import suppress
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.markdown import hbold
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.bot.manager import Manager
from app.bot.utils.texts import SUPPORTED_LANGUAGES
from app.bot.utils.api import fetch_services
from app.bot.utils.redis.models import UserData
from app.bot.manager import Form

from app.config import load_config

def select_language_markup() -> InlineKeyboardMarkup:
    """
    Generate an inline keyboard markup for selecting the language.

    :return: InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder().row(
        *[
            InlineKeyboardButton(text=text, callback_data=callback_data)
            for callback_data, text in SUPPORTED_LANGUAGES.items()
        ], width=2
    )
    return builder.as_markup()


async def create_menu_subscriptions(user_data) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру с кнопками на основе данных пользователя.

    :param user_data: Данные пользователя.
    :return: Объект клавиатуры.
    """
    try:
        services = await fetch_services(user_login=user_data.id) or []
    except RuntimeError:
        services = []

    # Создаем клавиатуру с выбором
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    # Добавляем кнопки для услуг (если они есть)
    for service in services:
        service_id = service['user_service_id']
        service_name = service['name']
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text=f"🔑 #{service_id} {service_name}",
                callback_data=f"service_{service_id}" 
            )
        ])
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(
            text="← Назад",
            callback_data="start" 
        )
    ])

    return keyboard


class Window:

    @staticmethod
    async def select_language(manager: Manager) -> None:
        """
        Display the window for selecting the language.

        :param manager: Manager object.
        :return: None
        """
        text = manager.text_message.get("select_language")
        with suppress(IndexError, KeyError):
            text = text.format(full_name=hbold(manager.user.full_name))
        reply_markup = select_language_markup()
        await manager.send_message(text, reply_markup=reply_markup)

    @staticmethod
    async def request(manager: Manager) -> None:
        """
        Display the window for request description

        :param manager: Manager object.
        :return: None
        """

        state = await manager.state.get_data()
        choice = state.get("choice")
        text = manager.text_message.get("request")
        with suppress(IndexError, KeyError):
            text = text.format(full_name=hbold(manager.user.full_name))

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="← Назад", callback_data="start")]
            ]
        )

        message = await manager.send_message(text, reply_markup=keyboard) # Костыль для удаления старого сообщения
        await manager.state.update_data(request_message=message.message_id)

    @staticmethod
    async def main_menu(manager: Manager, **_) -> None:
        """
        Display the main menu window.

        :param manager: Manager object.
        :return: None
        """
        text = manager.text_message.get("main_menu")
        getstate = await manager.state.get_state()

        config = load_config()
        bot_name = config.bot.BOT_NAME

        services = await fetch_services(user_login=manager.user.id)

        with suppress(IndexError, KeyError):
            text = text.format(full_name=hbold(manager.user.full_name), bot_name=hbold(bot_name))

        builder = InlineKeyboardBuilder()

        if services:
            builder.row(
                InlineKeyboardButton(text="🔑 Вопрос по подписке", callback_data="subscription_question"),
            )

        builder.row(
            InlineKeyboardButton(text="💸 Вопрос по оплате", callback_data="payment_question"),
        )
        builder.row(InlineKeyboardButton(text="Другой вопрос", callback_data="other_question"))

        keyboard = builder.as_markup()

        await manager.send_message(text, reply_markup=keyboard)
        await manager.state.set_state(None)

    @staticmethod
    async def select_subscription(manager: Manager, user_data: UserData) -> None:
        """
        Отображает окно выбора подписки.

        :param manager: Manager object.
        :param user_data: Данные пользователя.
        :return: None
        """

        text = manager.text_message.get("choose_subscription")
        keyboard = await create_menu_subscriptions(user_data)
        await manager.send_message(text, reply_markup=keyboard)


    @staticmethod
    async def change_language(manager: Manager) -> None:
        """
        Display the window for changing the language.

        :param manager: Manager object.
        :return: None
        """
        text = manager.text_message.get("change_language")
        reply_markup = select_language_markup()
        await manager.send_message(text, reply_markup=reply_markup)

    @staticmethod
    async def command_source(manager: Manager) -> None:
        """
        Display the window with information about the command source.

        :param manager: Manager object.
        :return: None
        """
        text = manager.text_message.get("command_source")
        await manager.send_message(text)