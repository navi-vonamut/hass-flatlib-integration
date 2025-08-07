# api.py
import aiohttp
import asyncio
from typing import Dict, Any
from datetime import datetime
from dateutil.relativedelta import relativedelta  # Новый импорт

class ApiClient:
    def __init__(self, session: aiohttp.ClientSession):
        self._session = session
        self._base_url = "http://localhost:8080"

    async def get_natal_chart(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self._base_url}/natal"
        try:
            async with self._session.post(url, json=payload) as response:
                response.raise_for_status()
                return await response.json()
        except asyncio.TimeoutError:
            raise ApiError("Timeout communicating with API")
        except aiohttp.ClientError as err:
            raise ApiError(f"Error communicating with API: {err}")

    async def async_get_daily_prediction(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self._base_url}/predict/daily"
        
        today_str = datetime.now().strftime('%Y/%m/%d')
        prediction_payload = {**payload, "target_date": today_str}

        try:
            async with self._session.post(url, json=prediction_payload) as response:
                response.raise_for_status()
                return await response.json()
        except asyncio.TimeoutError:
            raise ApiError("Timeout communicating with API for daily prediction")
        except aiohttp.ClientError as err:
            raise ApiError(f"Error communicating with API for daily prediction: {err}")

    # --- НОВЫЙ МЕТОД: Месячный прогноз ---
    async def async_get_monthly_prediction(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self._base_url}/predict/monthly"
        try:
            async with self._session.post(url, json=payload) as response:
                response.raise_for_status()
                return await response.json()
        except asyncio.TimeoutError:
            raise ApiError("Timeout communicating with API for monthly prediction")
        except aiohttp.ClientError as err:
            raise ApiError(f"Error communicating with API for monthly prediction: {err}")

    # --- НОВЫЙ МЕТОД: Годовой прогноз ---
    async def async_get_yearly_prediction(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self._base_url}/predict/yearly"
        try:
            async with self._session.post(url, json=payload) as response:
                response.raise_for_status()
                return await response.json()
        except asyncio.TimeoutError:
            raise ApiError("Timeout communicating with API for yearly prediction")
        except aiohttp.ClientError as err:
            raise ApiError(f"Error communicating with API for yearly prediction: {err}")

class ApiError(Exception):
    """Исключение для обозначения общей ошибки API."""