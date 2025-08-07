# __init__.py
import logging
from datetime import timedelta, datetime
import pytz

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, PLATFORMS
from .api import ApiClient, ApiError

_LOGGER = logging.getLogger(__name__)

DAILY_INTERVAL = timedelta(hours=24)
MONTHLY_INTERVAL = timedelta(hours=24)
YEARLY_INTERVAL = timedelta(hours=24)

def _convert_timezone_to_offset(tz_name: str) -> str:
    """Преобразует имя часового пояса в строковое смещение UTC в формате +HH:MM."""
    try:
        tz_object = pytz.timezone(tz_name)
        offset_seconds = tz_object.utcoffset(datetime.now()).total_seconds()
        
        offset_hours = int(offset_seconds / 3600)
        offset_minutes = int((offset_seconds % 3600) / 60)
        
        sign = "+" if offset_seconds >= 0 else "-"
        
        return f"{sign}{abs(offset_hours):02d}:{abs(offset_minutes):02d}"
    except (pytz.UnknownTimeZoneError, AttributeError):
        return "+00:00"

def _get_api_payload(entry: ConfigEntry) -> dict:
    """Создает полезную нагрузку для запроса API из данных конфигурации."""
    converted_tz = _convert_timezone_to_offset(entry.data.get("time_zone"))
    
    # Теперь отправляем дату в стандартном формате YYYY-MM-DD,
    # который Home Assistant возвращает и который, как показывает ошибка, ожидает сервер.
    birth_date_str = entry.data.get("birth_date")

    return {
        "date": birth_date_str, # Отправляем дату как есть (YYYY-MM-DD)
        "time": entry.data.get("birth_time"),
        "tz": converted_tz,
        "lat": entry.data.get("location", {}).get("latitude"),
        "lon": entry.data.get("location", {}).get("longitude"),
    }

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Настройка интеграции Flatlib из записи конфигурации."""
    session = async_get_clientsession(hass)
    api_client = ApiClient(session)

    async def async_update_natal_data():
        """Получить данные натальной карты."""
        payload = _get_api_payload(entry)
        try:
            return await api_client.get_natal_chart(payload)
        except ApiError as err:
            raise UpdateFailed(f"Ошибка получения натальной карты: {err}")

    natal_coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=f"flatlib_natal_{entry.data['name']}",
        update_method=async_update_natal_data,
        update_interval=DAILY_INTERVAL,
    )

    async def async_update_daily_data():
        """Получить данные ежедневного предсказания."""
        payload = _get_api_payload(entry)
        try:
            return await api_client.async_get_daily_prediction(payload)
        except ApiError as err:
            raise UpdateFailed(f"Ошибка получения ежедневного предсказания: {err}")

    daily_prediction_coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=f"flatlib_daily_prediction_{entry.data['name']}",
        update_method=async_update_daily_data,
        update_interval=DAILY_INTERVAL,
    )
    
    async def async_update_monthly_data():
        """Получить данные ежемесячного предсказания."""
        payload = _get_api_payload(entry)
        try:
            return await api_client.async_get_monthly_prediction(payload)
        except ApiError as err:
            raise UpdateFailed(f"Ошибка получения ежемесячного предсказания: {err}")

    monthly_prediction_coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=f"flatlib_monthly_prediction_{entry.data['name']}",
        update_method=async_update_monthly_data,
        update_interval=MONTHLY_INTERVAL,
    )

    async def async_update_yearly_data():
        """Получить данные ежегодного предсказания."""
        payload = _get_api_payload(entry)
        try:
            return await api_client.async_get_yearly_prediction(payload)
        except ApiError as err:
            raise UpdateFailed(f"Ошибка получения ежегодного предсказания: {err}")

    yearly_prediction_coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=f"flatlib_yearly_prediction_{entry.data['name']}",
        update_method=async_update_yearly_data,
        update_interval=YEARLY_INTERVAL,
    )

    await natal_coordinator.async_config_entry_first_refresh()
    await daily_prediction_coordinator.async_config_entry_first_refresh()
    await monthly_prediction_coordinator.async_config_entry_first_refresh()
    await yearly_prediction_coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "natal_coordinator": natal_coordinator,
        "daily_prediction_coordinator": daily_prediction_coordinator,
        "monthly_prediction_coordinator": monthly_prediction_coordinator,
        "yearly_prediction_coordinator": yearly_prediction_coordinator,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Выгрузить запись конфигурации."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok