"""Config flow for Kamstrup 403 integration."""

from typing import Any

import voluptuous as vol
from homeassistant.config_entries import SOURCE_RECONFIGURE, ConfigEntry, ConfigFlow, ConfigFlowResult, OptionsFlow
from homeassistant.const import CONF_PORT, CONF_SCAN_INTERVAL, CONF_TIMEOUT
from homeassistant.core import callback
from homeassistant.helpers.selector import TextSelector, TextSelectorConfig, TextSelectorType

from .const import DEFAULT_BAUDRATE, DEFAULT_SCAN_INTERVAL, DEFAULT_TIMEOUT, DOMAIN
from .pykamstrup.kamstrup import Kamstrup

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_PORT): TextSelector(TextSelectorConfig(type=TextSelectorType.TEXT)),
    },
)


class KamstrupFlowHandler(ConfigFlow, domain=DOMAIN):
    """Config flow for Kamstrup 403."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}

        if user_input is not None:
            try:
                Kamstrup(url=user_input[CONF_PORT], baudrate=DEFAULT_BAUDRATE, timeout=DEFAULT_TIMEOUT)
            except Exception:  # pylint: disable=broad-exception-caught # noqa: BLE001
                _errors["base"] = "port"
            else:
                if self.source == SOURCE_RECONFIGURE:
                    return self.async_update_reload_and_abort(
                        self._get_reconfigure_entry(),
                        title=user_input[CONF_PORT],
                        data=user_input,
                    )
                return self.async_create_entry(title=user_input[CONF_PORT], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=CONFIG_SCHEMA,
            errors=_errors,
        )

    async def async_step_reconfigure(self, _: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Handle reconfiguration."""
        data = self._get_reconfigure_entry().data.copy()

        return self.async_show_form(
            step_id="user",
            data_schema=self.add_suggested_values_to_schema(CONFIG_SCHEMA, data),
        )

    @staticmethod
    @callback
    def async_get_options_flow(_config_entry: ConfigEntry) -> OptionsFlow:
        """Get the options flow for this handler."""
        return KamstrupOptionsFlowHandler()


class KamstrupOptionsFlowHandler(OptionsFlow):
    """Kamstrup config flow options handler."""

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title=self.config_entry.data.get(CONF_PORT), data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_SCAN_INTERVAL,
                        default=self.config_entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
                    ): vol.All(vol.Coerce(int), vol.Range(min=1, max=86400)),
                    vol.Required(
                        CONF_TIMEOUT,
                        default=self.config_entry.options.get(CONF_TIMEOUT, DEFAULT_TIMEOUT),
                    ): vol.All(vol.Coerce(float), vol.Range(min=0.0, max=5.0)),
                }
            ),
        )
