from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery

from app.bot.handlers.private.windows import Window
from app.bot.manager import Manager
from app.bot.utils.redis import RedisStorage
from app.bot.utils.redis.models import UserData
from app.bot.utils.texts import SUPPORTED_LANGUAGES
from app.bot.utils.api import fetch_services, fetch_service
from aiogram.fsm.context import FSMContext
from app.bot.manager import Form
from aiogram_newsletter.utils.states import ANState

router = Router()
router.callback_query.filter(F.message.chat.type == "private", ~StateFilter(ANState))


@router.callback_query(F.data == "start")
async def handler(call: CallbackQuery, manager: Manager, redis: RedisStorage, user_data: UserData) -> None:
    """
    Handles callback queries for selecting the subscription

    :param call: CallbackQuery object.
    :param manager: Manager object.
    :param redis: RedisStorage object.
    :param user_data: UserData object.
    :return: None
    """
    
    await Window.main_menu(manager)
    await call.answer()

@router.callback_query(F.data.startswith("service_"))
async def handler(call: CallbackQuery, manager: Manager, redis: RedisStorage, user_data: UserData) -> None:
    """
    Handles callback queries for selecting the subscription

    :param call: CallbackQuery object.
    :param manager: Manager object.
    :param redis: RedisStorage object.
    :param user_data: UserData object.
    :return: None
    """

    choice = call.data
    await manager.state.update_data(choice=choice)

    if choice.startswith("service_"):
        service_id = choice.replace("service_", "")
        data = await fetch_service(user_login=user_data.id, service_id=service_id)

        await manager.state.update_data(choosed_service=data, service_id=service_id)

    
    await manager.state.set_state(Form.WAITING)
    await Window.request(manager)
    await call.answer()


@router.callback_query(F.data == "subscription_question")
async def handler(call: CallbackQuery, manager: Manager, redis: RedisStorage, user_data: UserData) -> None:
    """
    Handles callback queries for the subscription question.

    :param call: CallbackQuery object.
    :param manager: Manager object.
    :return: None
    """
    try:
        services = await fetch_services(user_login=user_data.id)

        if not services:
            await manager.show_alert(callback=call, text="☹️ У вас нет подписок", show_alert=True)
            return
        
        await Window.select_subscription(manager, user_data)
        await call.answer()

    except Exception as e:
        await manager.show_alert(callback=call, text=f"Произошла ошибка при загрузке подписок: {e}", show_alert=True)



@router.callback_query(F.data.endswith("_question"))
async def handler(call: CallbackQuery, manager: Manager, redis: RedisStorage, user_data: UserData) -> None:
    """
    Handles callback queries for the language question.


    :param call: CallbackQuery object.
    :param manager: Manager object.
    :param redis: RedisStorage object.
    :param user_data: UserData object.
    :return: None
    """
    choice = call.data.split("_question")[0]
    await manager.state.update_data(choice=choice)

    if choice == "payment":
        await manager.state.set_state(Form.PAYMENT)

    if choice == "other":
        await manager.state.set_state(Form.OTHER)

    await Window.request(manager)



@router.callback_query()
async def handler(call: CallbackQuery, manager: Manager, redis: RedisStorage, user_data: UserData) -> None:
    """
    Handles callback queries for selecting the language.

    If the callback data is 'ru' or 'en', updates the user's language code in Redis and sets
    the language for the manager's text messages. Then, displays the main menu window.

    :param call: CallbackQuery object.
    :param manager: Manager object.
    :param redis: RedisStorage object.
    :param user_data: UserData object.
    :return: None
    """
    if call.data in SUPPORTED_LANGUAGES.keys():
        user_data.language_code = call.data
        manager.text_message.language_code = call.data
        await redis.update_user(user_data.id, user_data)
        await manager.state.update_data(language_code=call.data)
        await Window.main_menu(manager)

    await call.answer()
