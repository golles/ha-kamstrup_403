"""Adds config flow for Kamstrup 403."""
import logging

from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PORT, CONF_SCAN_INTERVAL, CONF_TIMEOUT
from homeassistant.core import callback
import voluptuous as vol

from .const import DEFAULT_BAUDRATE, DEFAULT_SCAN_INTERVAL, DEFAULT_TIMEOUT, DOMAIN
from .pykamstrup.kamstrup import Kamstrup

_LOGGER: logging.Logger = logging.getLogger(__package__)


class KamstrupFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Kamstrup 403."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.FlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}

        if user_input is not None:
            try:
                Kamstrup(
                    port=user_input[CONF_PORT],
                    baudrate=DEFAULT_BAUDRATE,
                    timeout=DEFAULT_TIMEOUT,
                )
            except Exception as exception:  # pylint: disable=broad-exception-caught
                _LOGGER.error("Error accessing port \nException: %e", exception)
                _errors["base"] = "port"
            else:
                return self.async_create_entry(
                    title=user_input[CONF_PORT], data=user_input
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_PORT): str,
                }
            ),
            errors=_errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return KamstrupOptionsFlowHandler(config_entry)


class KamstrupOptionsFlowHandler(config_entries.OptionsFlow):
    """Kamstrup config flow options handler."""

    def __init__(self, config_entry: ConfigEntry):
        """Initialize options flow."""
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
                    vol.Required(
                        CONF_SCAN_INTERVAL,
                        default=self.config_entry.options.get(
                            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                        ),
                    ): vol.All(vol.Coerce(int), vol.Range(min=1, max=86400)),
                    vol.Required(
                        CONF_TIMEOUT,
                        default=self.config_entry.options.get(
                            CONF_TIMEOUT, DEFAULT_TIMEOUT
                        ),
                    ): vol.All(vol.Coerce(float), vol.Range(min=0.0, max=5.0)),
                }
            ),
        )

    async def _update_options(self):
        """Update config entry options."""
        return self.async_create_entry(
            title=self.config_entry.data.get(CONF_PORT), data=self.options
        )
