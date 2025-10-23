"""Diagnostics support for kamstrup_403."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .coordinator import KamstrupUpdateCoordinator


async def async_get_config_entry_diagnostics(_hass: HomeAssistant, config_entry: ConfigEntry[KamstrupUpdateCoordinator]) -> dict:
    """Return diagnostics for a config entry."""
    coordinator = config_entry.runtime_data

    return {
        "config_entry": config_entry.as_dict(),
        "data": coordinator.data,
        "registered_commands": coordinator.commands,
    }
