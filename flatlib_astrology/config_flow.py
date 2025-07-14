import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.selector import (
    TextSelector,
    TextSelectorConfig,
    DateSelector,
    TimeSelector,
    LocationSelector,
)
from .const import DOMAIN

class FlatlibNatalConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        
        if user_input is not None:
            unique_id = user_input["name"].strip().lower().replace(" ", "_")
            await self.async_set_unique_id(unique_id)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=user_input["name"], 
                data=user_input
            )

        # Правильное создание схемы с использованием vol.Schema
        data_schema={
            "name": TextSelector(TextSelectorConfig(type="text")),
            "birth_date": DateSelector(),
            "birth_time": TimeSelector(),
            "location": LocationSelector(),
            "time_zone": TextSelector(TextSelectorConfig(type="text")),
        }

        return self.async_show_form(
            step_id="user", 
            data_schema=vol.Schema(data_schema),
            errors=errors
        )