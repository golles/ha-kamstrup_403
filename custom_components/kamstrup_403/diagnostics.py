"""Diagnostics support for kamstrup_403."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import KamstrupUpdateCoordinator


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, config_entry: ConfigEntry
) -> dict:
    """Return diagnostics for a config entry."""
    coordinator: KamstrupUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    return {
        "config_entry": config_entry.as_dict(),
        "data": coordinator.data,
        "registered_commands": coordinator.commands,
    }
