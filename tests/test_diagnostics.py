"""Test diagnostics."""

from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.components.diagnostics import get_diagnostics_for_config_entry
from pytest_homeassistant_custom_component.typing import ClientSessionGenerator

from custom_components.kamstrup_403.const import DOMAIN

from . import setup_integration


async def test_config_entry_diagnostics(hass: HomeAssistant, hass_client: ClientSessionGenerator) -> None:
    """Test config entry diagnostics."""
    config_entry = await setup_integration(hass)

    result = await get_diagnostics_for_config_entry(hass, hass_client, config_entry)

    assert result["config_entry"]["entry_id"] == "test_entry"
    assert result["config_entry"]["domain"] == DOMAIN
