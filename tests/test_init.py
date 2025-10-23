"""Test setup."""

from unittest.mock import patch

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.kamstrup_403 import async_setup_entry
from custom_components.kamstrup_403.const import DOMAIN
from custom_components.kamstrup_403.coordinator import KamstrupUpdateCoordinator

from . import get_mock_config_entry, setup_integration, unload_integration


async def test_setup_and_unload_entry(hass: HomeAssistant) -> None:
    """Test entry setup and unload."""
    config_entry = await setup_integration(hass)

    # Check that the client is stored as runtime_data
    assert isinstance(config_entry.runtime_data, KamstrupUpdateCoordinator)

    await unload_integration(hass, config_entry)


async def test_setup_entry_exception(hass: HomeAssistant) -> None:
    """Test setup entry raises ConfigEntryNotReady on connection error."""
    # Create config entry but don't set it up through HA's system
    config_entry = get_mock_config_entry()
    config_entry.add_to_hass(hass)

    # Mock the Kamstrup class to raise an exception during instantiation
    with patch("custom_components.kamstrup_403.Kamstrup") as mock_kamstrup_class:
        mock_kamstrup_class.side_effect = Exception("Connection failed")

        # This should raise ConfigEntryNotReady due to connection error
        with pytest.raises(ConfigEntryNotReady):
            await async_setup_entry(hass, config_entry)


async def test_setup_entry_no_port(hass: HomeAssistant) -> None:
    """Test setup entry raises ValueError on missing port."""
    # Create config entry but don't set it up through HA's system
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        entry_id="test_entry",
        data={},
    )
    config_entry.add_to_hass(hass)

    # This should raise ValueError due to missing port
    with pytest.raises(ValueError):  # noqa: PT011
        await async_setup_entry(hass, config_entry)


async def test_async_reload_entry(hass: HomeAssistant) -> None:
    """Test reloading the entry."""
    config_entry = await setup_integration(hass)

    with patch("custom_components.kamstrup_403.async_reload_entry") as mock_reload_entry:
        assert len(mock_reload_entry.mock_calls) == 0
        hass.config_entries.async_update_entry(config_entry, options={"something": "else"})
        assert len(mock_reload_entry.mock_calls) == 1
