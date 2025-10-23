"""Integration tests."""

from homeassistant.const import CONF_PORT
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.kamstrup_403.const import DOMAIN


def get_mock_config_data() -> dict[str, str]:
    """Create a mock configuration for testing."""
    return {
        CONF_PORT: "/dev/ttyUSB0",
    }


def get_mock_config_entry() -> MockConfigEntry:
    """Create a mock config entry for testing."""
    return MockConfigEntry(
        domain=DOMAIN,
        entry_id="test_entry",
        data=get_mock_config_data(),
    )


async def setup_integration(hass: HomeAssistant) -> MockConfigEntry:
    """Set up the custom component for tests."""
    config_entry = get_mock_config_entry()
    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    return config_entry


async def unload_integration(hass: HomeAssistant, config_entry: MockConfigEntry) -> None:
    """Unload the custom component for tests."""
    assert await hass.config_entries.async_unload(config_entry.entry_id)
    await hass.async_block_till_done()
