"""Tests for kamstrup_403 coordinator."""
from homeassistant.core import HomeAssistant

from custom_components.kamstrup_403.const import DOMAIN
from custom_components.kamstrup_403.coordinator import KamstrupUpdateCoordinator

from . import setup_component
from .const import DEFAULT_ENABLED_COMMANDS


async def test_command_list(hass: HomeAssistant, bypass_get_data):
    """Test command list and register/unregister methods."""
    config_entry = await setup_component(hass)

    coordinator: KamstrupUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    assert coordinator.commands == DEFAULT_ENABLED_COMMANDS

    coordinator.register_command(22)
    assert len(coordinator.commands) == len(DEFAULT_ENABLED_COMMANDS) + 1

    coordinator.unregister_command(22)
    assert len(coordinator.commands) == len(DEFAULT_ENABLED_COMMANDS)


async def test_failed_readings_log(hass: HomeAssistant, bypass_get_data, caplog):
    """Test logs from failed readings."""
    config_entry = await setup_component(hass)

    coordinator: KamstrupUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    assert coordinator.commands == DEFAULT_ENABLED_COMMANDS

    for command in DEFAULT_ENABLED_COMMANDS:
        assert "No value for sensor " + str(command) in caplog.text

    assert (
        "Finished update, No readings from the meter. Please check the IR connection"
        in caplog.text
    )
