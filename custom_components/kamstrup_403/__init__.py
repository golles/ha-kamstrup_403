"""Custom integration to integrate kamstrup_403 with Home Assistant.

For more details about this integration, please refer to
https://github.com/custom-components/kamstrup_403
"""

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry, ConfigEntryState
from homeassistant.const import CONF_PORT, CONF_SCAN_INTERVAL, CONF_TIMEOUT, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DEFAULT_BAUDRATE, DEFAULT_SCAN_INTERVAL, DEFAULT_TIMEOUT, DOMAIN
from .coordinator import KamstrupUpdateCoordinator
from .pykamstrup.kamstrup import Kamstrup

_LOGGER: logging.Logger = logging.getLogger(__package__)


PLATFORMS: list[Platform] = [
    Platform.SENSOR,
]


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry[KamstrupUpdateCoordinator]) -> bool:
    """Set up this integration using UI."""
    hass.data.setdefault(DOMAIN, {})

    port = config_entry.data.get(CONF_PORT)
    scan_interval_seconds = config_entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
    scan_interval = timedelta(seconds=scan_interval_seconds)
    timeout_seconds = config_entry.options.get(CONF_TIMEOUT, DEFAULT_TIMEOUT)

    if not port:
        msg = "Missing required configuration options: port."
        raise ValueError(msg)

    _LOGGER.debug(
        "Set up entry, with scan_interval of %s seconds and timeout of %s seconds",
        scan_interval_seconds,
        timeout_seconds,
    )

    try:
        client = Kamstrup(url=port, baudrate=DEFAULT_BAUDRATE, timeout=timeout_seconds)
        await client.connect()
    except Exception as exception:
        _LOGGER.warning("Can't establish a connection to %s", port)
        raise ConfigEntryNotReady from exception

    config_entry.runtime_data = coordinator = KamstrupUpdateCoordinator(
        hass=hass,
        config_entry=config_entry,
        client=client,
        scan_interval=scan_interval,
    )

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)

    if config_entry.state is ConfigEntryState.LOADED:
        await coordinator.async_refresh()
    else:
        await coordinator.async_config_entry_first_refresh()

    config_entry.async_on_unload(config_entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry[KamstrupUpdateCoordinator]) -> bool:
    """Unload a config entry."""
    if hasattr(config_entry, "runtime_data") and config_entry.runtime_data:
        coordinator = config_entry.runtime_data
        if coordinator and coordinator.kamstrup:
            await coordinator.kamstrup.disconnect()
    return await hass.config_entries.async_unload_platforms(config_entry, PLATFORMS)


async def async_reload_entry(hass: HomeAssistant, config_entry: ConfigEntry[KamstrupUpdateCoordinator]) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, config_entry)
    await async_setup_entry(hass, config_entry)
