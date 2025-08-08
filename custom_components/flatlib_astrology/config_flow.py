import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.selector import (
    TextSelector,
    TextSelectorConfig,
    DateSelector,
    TimeSelector,
    LocationSelector,
    SelectSelector,
    SelectSelectorConfig,
)
from .const import DOMAIN
import pytz # <-- Новый импорт!

class FlatlibNatalConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Обработка начального шага."""
        errors = {}
        
        all_users = await self.hass.auth.async_get_users()
        excluded_names = ["Supervisor", "Home Assistant Content"]
        filtered_users = [user for user in all_users if user.name not in excluded_names]
        user_options = {user.id: user.name for user in filtered_users}
        
        # Получаем полный список часовых поясов
        timezones = pytz.all_timezones
        timezone_options = [{"value": tz, "label": tz} for tz in timezones]
        
        if user_input is not None:
            user_id = user_input["user_id"]
            user_name = user_options.get(user_id, "Unknown User")
            
            await self.async_set_unique_id(user_id)
            self._abort_if_unique_id_configured()
            
            data = {
                "user_id": user_id,
                "name": user_name,
                "birth_date": user_input["birth_date"],
                "birth_time": user_input["birth_time"],
                "location": user_input["location"],
                "time_zone": user_input["time_zone"],
            }
            
            return self.async_create_entry(
                title=user_name,
                data=data
            )

        data_schema={
            "user_id": SelectSelector(
                SelectSelectorConfig(
                    options=[
                        {"value": user_id, "label": user_name}
                        for user_id, user_name in user_options.items()
                    ],
                    mode="dropdown",
                )
            ),
            "birth_date": DateSelector(),
            "birth_time": TimeSelector(),
            "location": LocationSelector(),
            "time_zone": SelectSelector( # <-- Теперь это SelectSelector!
                SelectSelectorConfig(
                    options=timezone_options,
                    mode="dropdown",
                )
            ),
        }

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(data_schema),
            errors=errors
        )