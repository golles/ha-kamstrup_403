"""
Custom integration to integrate kamstrup_403 with Home Assistant.

For more details about this integration, please refer to
https://github.com/custom-components/kamstrup_403
"""
import asyncio
from datetime import timedelta
import logging
import serial

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PORT
from homeassistant.core import Config, HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .kamstrup import Kamstrup

from .const import (
    DEFAULT_BAUDRATE,
    DEFAULT_TIMEOUT,
    DOMAIN,
    PLATFORMS,
    SENSORS,
)

SCAN_INTERVAL = timedelta(seconds=60)

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup(hass: HomeAssistant, config: Config):
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})

    port = entry.data.get(CONF_PORT)
    client = Kamstrup(port, DEFAULT_BAUDRATE, DEFAULT_TIMEOUT)

    coordinator = KamstrupUpdateCoordinator(hass, client=client)
    await coordinator.async_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    hass.data[DOMAIN][entry.entry_id] = coordinator

    for platform in PLATFORMS:
        if entry.options.get(platform, True):
            coordinator.platforms.append(platform)
            hass.async_add_job(
                hass.config_entries.async_forward_entry_setup(entry, platform)
            )

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    return True


class KamstrupUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the Kamstrup serial reader."""

    def __init__(self, hass: HomeAssistant, client: Kamstrup) -> None:
        """Initialize."""
        self.kamstrup = client
        self.platforms = []

        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL)

    async def _async_update_data(self):
        """Update data via library."""
        _LOGGER.debug('KamstrupUpdateCoordinator: _async_update_data start')

        data = {}
        for key in SENSORS:
            try:
                value, unit = self.kamstrup.readvar(SENSORS[key]["command"])
                data[SENSORS[key]["command"]] = {"value": value, "unit": unit}
            except (serial.SerialException):
                _LOGGER.error('Device disconnected or multiple access on port?')
        return data


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    unloaded = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
                if platform in coordinator.platforms
            ]
        )
    )
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
