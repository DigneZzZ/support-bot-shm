import aiohttp
import asyncio
from typing import Dict, Any, Optional, List
from app.config import load_config

config = load_config()
API_URL = config.api.API_URL
timeout = aiohttp.ClientTimeout(total=5)

async def fetch_user_data(user_login: int) -> Optional[Dict[str, Any]]:
    """
    Получает данные пользователя из API.

    :param user_login: Логин пользователя (ID).
    :return: Данные пользователя или None, если произошла ошибка.
    """
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(API_URL, params={"login": f"@{user_login}", "format": "json"}) as response:
                if response.status == 200:
                    data = await response.json()
    
                    if data.get("response") == "No data":
                        print("Ошибка: Нет данных в ответе от API")
                        return None

                    # Извлекаем данные пользователя
                    user_data = data.get("user")
                    if user_data:
                        return user_data  # Возвращаем данные пользователя
                    else:
                        print("Ошибка: Данные пользователя отсутствуют в ответе")
                        return None
                else:
                    print(f"Ошибка при запросе к API: {response.status}")
                    return None
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None

async def fetch_services(user_login: int) -> Optional[List[Dict[str, Any]]]:
    """
    Получает список услуг пользователя из API.

    :param user_login: Логин пользователя (ID).
    :return: Список услуг или None, если произошла ошибка.
    """
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(API_URL, params={"login": f"@{user_login}", "format": "json"}) as response:

                if response.status == 200:
                    data = await response.json()
    
                    if data.get("response") == "No data":
                        print("Ошибка: Нет данных в ответе от API")
                        return None
                
                    return data.get("services", [])  

                else:
                    print(f"Ошибка при запросе к API: {response.status}")
                    return []  # Возвращаем пустой список в случае ошибки

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None

async def fetch_service(user_login: int, service_id: int) -> Optional[List[Dict[str, Any]]]:
    """
    Получает услугу пользовавтеля из API.

    :param user_login: Логин пользователя (ID).
    :param service_id: ID услуги.
    :return: Список услуг или None, если произошла ошибка.
    """
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(API_URL, params={"login": f"@{user_login}", "format": "json"}) as response:

                if response.status == 200:
                    data = await response.json()
                    services = data.get("services", [])
                    selected_service = next((s for s in services if str(s['user_service_id']) == service_id), None)

                    if selected_service:
                        return selected_service['name']
                    else:
                        print("Ошибка: Услуга не найдена")
                        return None

                else:
                    print(f"Ошибка при запросе к API: {response.status}")
                    return None
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        pass