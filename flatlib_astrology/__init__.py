"""The Flatlib Natal Chart integration."""
import logging
from datetime import timedelta
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN
from .api import ApiClient, ApiError

_LOGGER = logging.getLogger(__name__)
PLATFORMS = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Flatlib Natal Chart from a config entry."""
    # Используем общую сессию aiohttp, управляемую Home Assistant
    session = async_get_clientsession(hass)
    api_client = ApiClient(session)
    
    # --- ИСПРАВЛЕНИЕ: Получаем данные напрямую, без сложной обработки ---
    entry_data = entry.data
    _LOGGER.debug("Setting up Flatlib Natal for: %s", entry_data["name"])

    async def async_update_data():
        """Fetch data from the flatlib-server API."""
        try:
            location_data = entry.data["location"]
            # --- ИСПРАВЛЕНИЕ: Корректно форматируем дату и время ---
            payload = {
                "date": entry_data["birth_date"],
                "time": entry_data["birth_time"],
                "tz": entry_data["time_zone"],
                "lat": str(location_data["latitude"]),
                "lon": str(location_data["longitude"]),
            }
            _LOGGER.debug("Sending payload to API: %s", payload)
            return await api_client.get_natal_chart(payload)
        except ApiError as err:
            raise UpdateFailed(f"Error communicating with API: {err}")
        except KeyError as err:
            raise UpdateFailed(f"Missing data in config entry: {err}")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=f"flatlib_natal_{entry_data['name']}",
        update_method=async_update_data,
        update_interval=timedelta(hours=24), # Обновляем раз в сутки
    )

    # Выполняем первое обновление при запуске
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok