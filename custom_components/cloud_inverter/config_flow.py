import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import DOMAIN, CONF_USERNAME, CONF_PASSWORD, CONF_SIGN, CONF_GOODS_ID, CONF_DATASIGN
from .api import CloudInverterApiClient

class CloudInverterConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            session = async_get_clientsession(self.hass)
            client = CloudInverterApiClient(
                user_input[CONF_USERNAME],
                user_input[CONF_PASSWORD],
                user_input[CONF_SIGN],
                user_input[CONF_GOODS_ID],
                user_input[CONF_DATASIGN],
                session
            )
            try:
                await client.async_login()
                return self.async_create_entry(title=user_input[CONF_USERNAME], data=user_input)
            except Exception:
                errors["base"] = "invalid_auth"

        schema = vol.Schema({
            vol.Required(CONF_USERNAME): str,
            vol.Required(CONF_PASSWORD): str,
            vol.Required(CONF_SIGN): str,
            vol.Required(CONF_GOODS_ID): str,
            vol.Required(CONF_DATASIGN): str,
        })
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    async def async_step_import(self, import_input=None):
        """Handle import from configuration.yaml."""
        return await self.async_step_user(import_input)
