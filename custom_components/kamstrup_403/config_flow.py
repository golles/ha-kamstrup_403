"""Adds config flow for Kamstrup 403."""
from homeassistant import config_entries
from homeassistant.const import CONF_PORT
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_create_clientsession
import voluptuous as vol
import serial

from .const import (
    DEFAULT_BAUDRATE,
    DEFAULT_TIMEOUT,
    DOMAIN,
    PLATFORMS,
)


class KamstrupFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Kamstrup 403."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        # Uncomment the next 2 lines if only a single instance of the integration is allowed:
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            if user_input[CONF_PORT] is not None:
                try:
                    s = serial.Serial(
                        port=user_input[CONF_PORT],
                        baudrate=DEFAULT_BAUDRATE,
                        timeout=DEFAULT_TIMEOUT,
                    )
                    s.close()

                    return self.async_create_entry(
                        title=user_input[CONF_PORT], data=user_input
                    )
                except (serial.SerialException):
                    self._errors["base"] = "port"
            else:
                self._errors["base"] = "port"

            return await self._show_config_form(user_input)

        user_input = {}
        # Provide defaults for form
        user_input[CONF_PORT] = ""

        return await self._show_config_form(user_input)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return KamstrupOptionsFlowHandler(config_entry)

    async def _show_config_form(self, user_input):  # pylint: disable=unused-argument
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_PORT, default=user_input[CONF_PORT]): str,
                }
            ),
            errors=self._errors,
        )


class KamstrupOptionsFlowHandler(config_entries.OptionsFlow):
    """Kamstrup config flow options handler."""

    def __init__(self, config_entry):
        """Initialize HACS options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(self, user_input=None):  # pylint: disable=unused-argument
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            self.options.update(user_input)
            return await self._update_options()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(x, default=self.options.get(x, True)): bool
                    for x in sorted(PLATFORMS)
                }
            ),
        )

    async def _update_options(self):
        """Update config entry options."""
        return self.async_create_entry(
            title=self.config_entry.data.get(CONF_PORT), data=self.options
        )
