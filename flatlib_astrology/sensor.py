"""Platform for Natal Chart sensor integration."""
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN # Предполагаем, что DOMAIN определён в const.py

# Импорты PLANETS, ANGLES, HOUSES, ASPECTS, ZODIAC_SIGNS, SPECIAL_OBJECTS
# больше не нужны в этом файле, так как мы не будем создавать отдельные сенсоры для них.

class NatalChartRawSensor(CoordinatorEntity, SensorEntity):
    """Sensor to hold raw natal chart and transit data for LLM interpretation."""

    def __init__(self, coordinator, unique_prefix, person_name):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._person_name = person_name
        
        # Уникальный ID сенсора
        self._attr_unique_id = f"{unique_prefix}_natal_chart"
        # Отображаемое имя сенсора
        self._attr_name = f"{person_name} Natal Chart"
        # Иконка для сенсора
        self._attr_icon = "mdi:star-four-points" # Можно выбрать что-то более подходящее, если есть

        # Информация об устройстве для группировки в Home Assistant UI
        # Это создает "виртуальное устройство", к которому будет принадлежать ваш сенсор.
        # Это полезно для организации в UI.
        self._attr_device_info = {
            "identifiers": {(DOMAIN, unique_prefix)},
            "name": f"{person_name} Astrology Data", # Имя виртуального устройства
            "manufacturer": "Flatlib"
        }

    @property
    def state(self):
        """Return the state of the sensor. 
        It can be 'loaded', 'empty', or 'error' depending on data availability.
        """
        if self.coordinator.data:
            # Проверяем наличие ключевых секций для натальной карты, чтобы убедиться, что данные полные
            if "planets" in self.coordinator.data and "angles" in self.coordinator.data:
                return "loaded"
            else:
                return "incomplete" # Данные есть, но не полные
        return "empty" # Данных нет

    @property
    def extra_state_attributes(self):
        """Return the raw natal chart and transit data as attributes."""
        # Все данные из координатора (полученные от аддона) помещаем в атрибуты.
        # Это позволяет LLM-ассистентам легко получить доступ ко всей структуре JSON.
        return self.coordinator.data or {}

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the sensor platform from a config entry."""
    # Получаем координатор обновления данных, который был создан в __init__.py
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    # Получаем имя человека из данных конфигурации (из config_flow или configuration.yaml)
    person_name = config_entry.data["name"] 
    
    # Используем entry_id как уникальный префикс для всех сущностей, связанных с этой конфигурацией.
    unique_prefix = config_entry.entry_id

    # Создаем единственный сенсор для натальной карты
    sensors = [
        NatalChartRawSensor(coordinator, unique_prefix, person_name)
    ]
    
    # Добавляем сенсор в Home Assistant
    async_add_entities(sensors)