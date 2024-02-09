"""
Custom integration to integrate kamstrup_403 with Home Assistant.

For more details about this integration, please refer to
https://github.com/custom-components/kamstrup_403
"""

from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PORT, CONF_SCAN_INTERVAL, CONF_TIMEOUT, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo

from .const import (
    DEFAULT_BAUDRATE,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_TIMEOUT,
    DOMAIN,
    NAME,
    VERSION,
)
from .coordinator import KamstrupUpdateCoordinator
from .pykamstrup.kamstrup import Kamstrup

_LOGGER: logging.Logger = logging.getLogger(__package__)


PLATFORMS: list[Platform] = [
    Platform.SENSOR,
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up this integration using UI."""
    hass.data.setdefault(DOMAIN, {})

    port = entry.data.get(CONF_PORT)
    scan_interval_seconds = entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
    scan_interval = timedelta(seconds=scan_interval_seconds)
    timeout_seconds = entry.options.get(CONF_TIMEOUT, DEFAULT_TIMEOUT)

    _LOGGER.debug(
        "Set up entry, with scan_interval of %s seconds and timeout of %s seconds",
        scan_interval_seconds,
        timeout_seconds,
    )

    try:
        client = Kamstrup(url=port, baudrate=DEFAULT_BAUDRATE, timeout=timeout_seconds)
    except Exception as exception:
        _LOGGER.error("Can't establish a connection to %s", port)
        raise ConfigEntryNotReady() from exception

    device_info = DeviceInfo(
        entry_type=DeviceEntryType.SERVICE,
        identifiers={(DOMAIN, port)},
        manufacturer=NAME,
        name=NAME,
        model=VERSION,
    )

    hass.data[DOMAIN][entry.entry_id] = coordinator = KamstrupUpdateCoordinator(
        hass=hass, client=client, scan_interval=scan_interval, device_info=device_info
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    await coordinator.async_config_entry_first_refresh()

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    if unloaded := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
