"""Platform for Flatlib sensor integration."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

class NatalChartRawSensor(CoordinatorEntity, SensorEntity):
    """Sensor to hold raw natal chart data."""

    def __init__(self, coordinator, unique_prefix, person_name):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{unique_prefix}_natal_chart_raw"
        self._attr_name = f"{person_name} Natal Chart Raw Data"
        self._attr_icon = "mdi:star-four-points"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, unique_prefix)},
            "name": f"{person_name} Astrology Data",
            "manufacturer": "Flatlib",
        }

    @property
    def state(self):
        """Return the state of the sensor."""
        if self.coordinator.data:
            return "loaded"
        return "empty"

    @property
    def extra_state_attributes(self):
        """Return the raw natal chart data as attributes."""
        return self.coordinator.data or {}


class DailyPredictionRawSensor(CoordinatorEntity, SensorEntity):
    """Sensor to hold daily prediction data as raw attributes."""

    def __init__(self, coordinator, unique_prefix, person_name):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{unique_prefix}_daily_prediction_raw"
        self._attr_name = f"{person_name} Daily Prediction Raw Data"
        self._attr_icon = "mdi:calendar-today"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, unique_prefix)},
            "name": f"{person_name} Astrology Data",
            "manufacturer": "Flatlib",
        }

    @property
    def state(self):
        """Return the state of the sensor. It indicates data availability."""
        if self.coordinator.data:
            return "loaded"
        return "empty"

    @property
    def extra_state_attributes(self):
        """Return all data as attributes."""
        return self.coordinator.data or {}

# --- НОВЫЕ КЛАССЫ СЕНСОРОВ ---
class MonthlyPredictionRawSensor(CoordinatorEntity, SensorEntity):
    """Sensor to hold monthly prediction data as raw attributes."""

    def __init__(self, coordinator, unique_prefix, person_name):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{unique_prefix}_monthly_prediction_raw"
        self._attr_name = f"{person_name} Monthly Prediction Raw Data"
        self._attr_icon = "mdi:calendar-month"  # Новая иконка
        self._attr_device_info = {
            "identifiers": {(DOMAIN, unique_prefix)},
            "name": f"{person_name} Astrology Data",
            "manufacturer": "Flatlib",
        }

    @property
    def state(self):
        """Return the state of the sensor. It indicates data availability."""
        if self.coordinator.data:
            return "loaded"
        return "empty"

    @property
    def extra_state_attributes(self):
        """Return all data as attributes."""
        return self.coordinator.data or {}

class YearlyPredictionRawSensor(CoordinatorEntity, SensorEntity):
    """Sensor to hold yearly prediction data as raw attributes."""

    def __init__(self, coordinator, unique_prefix, person_name):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{unique_prefix}_yearly_prediction_raw"
        self._attr_name = f"{person_name} Yearly Prediction Raw Data"
        self._attr_icon = "mdi:calendar-star"  # Новая иконка
        self._attr_device_info = {
            "identifiers": {(DOMAIN, unique_prefix)},
            "name": f"{person_name} Astrology Data",
            "manufacturer": "Flatlib",
        }

    @property
    def state(self):
        """Return the state of the sensor. It indicates data availability."""
        if self.coordinator.data:
            return "loaded"
        return "empty"

    @property
    def extra_state_attributes(self):
        """Return all data as attributes."""
        return self.coordinator.data or {}

# --- ОБНОВЛЕННАЯ ФУНКЦИЯ НАСТРОЙКИ ---
async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the sensor platform from a config entry."""
    # Получаем все координаторы из словаря в hass.data
    coordinators = hass.data[DOMAIN][config_entry.entry_id]
    
    person_name = config_entry.data["name"]
    unique_prefix = config_entry.entry_id

    # Создаем все четыре сенсора, каждый со своим координатором
    sensors = [
        NatalChartRawSensor(coordinators["natal_coordinator"], unique_prefix, person_name),
        DailyPredictionRawSensor(coordinators["daily_prediction_coordinator"], unique_prefix, person_name),
        MonthlyPredictionRawSensor(coordinators["monthly_prediction_coordinator"], unique_prefix, person_name),
        YearlyPredictionRawSensor(coordinators["yearly_prediction_coordinator"], unique_prefix, person_name),
    ]
    
    async_add_entities(sensors)