"""Tests for sensor."""

from unittest.mock import AsyncMock

import pytest
from homeassistant.core import HomeAssistant

from custom_components.kamstrup_403.sensor import DESCRIPTIONS, KamstrupSensor

from . import get_mock_config_entry, setup_integration, unload_integration


@pytest.mark.parametrize(
    ("entity", "value", "unit_of_measurement"),
    [
        ("sensor.kamstrup_403_heat_energy_e1", "1234.0", "GJ"),
        ("sensor.kamstrup_403_heat_energy_to_gas", "1234.0", "m³"),
        ("sensor.kamstrup_403_volume", "5678.0", "m³"),
        ("sensor.kamstrup_403_infoevent", "0", None),
        ("sensor.kamstrup_403_infoevent_counter", "1", None),
        ("sensor.kamstrup_403_serial_number", "12345678", None),
        ("sensor.kamstrup_403_hourcounter", "12345.0", None),
        ("sensor.kamstrup_403_minflowdate_m", "2023-01-23T00:00:00+00:00", None),
    ],
)
async def test_state(hass: HomeAssistant, entity: str, value: str, unit_of_measurement: str | None) -> None:
    """Test sensor states."""
    config_entry = await setup_integration(hass)

    state = hass.states.get(entity)
    assert state
    assert state.state == value
    if unit_of_measurement is not None:
        assert state.attributes.get("unit_of_measurement") == unit_of_measurement

    await unload_integration(hass, config_entry)


async def test_native_value_returns_none_when_no_data(hass: HomeAssistant, mock_kamstrup: AsyncMock) -> None:
    """Test that native_value returns None when coordinator.data is None."""
    # Configure the mock to return no data
    mock_kamstrup.get_values.return_value = {}

    config_entry = await setup_integration(hass)

    # Test a sensor that should exist but have no data
    state = hass.states.get("sensor.kamstrup_403_heat_energy_e1")
    assert state
    assert state.state == "unavailable"  # Entity should be unavailable when data is None

    await unload_integration(hass, config_entry)


async def test_native_value_returns_none_when_data_key_missing(hass: HomeAssistant, mock_kamstrup: AsyncMock) -> None:
    """Test that native_value returns None when data_key is not in coordinator.data."""
    # Configure the mock to return data but without the specific key we're testing
    mock_kamstrup.get_values.return_value = {
        99: (0, None),  # Some other key but not the one we want to test
    }

    config_entry = await setup_integration(hass)

    # Test a sensor whose data key (60) is not in the returned data
    state = hass.states.get("sensor.kamstrup_403_heat_energy_e1")
    assert state
    assert state.state == "unavailable"  # Entity should be unavailable when key is missing

    await unload_integration(hass, config_entry)


def test_native_value_method_directly_when_no_data() -> None:
    """Test native_value method directly returns None when coordinator.data is None."""
    # Set up a mock coordinator with no data
    mock_coordinator = AsyncMock()
    mock_coordinator.data = None

    # Create sensor instance directly (not through integration)
    sensor = KamstrupSensor(mock_coordinator, get_mock_config_entry(), DESCRIPTIONS[0])

    # Test native_value directly - this should hit line 364: return None
    result = sensor.native_value
    assert result is None


async def test_date_sensor_returns_none_for_invalid_value(hass: HomeAssistant, mock_kamstrup: AsyncMock) -> None:
    """Test that KamstrupDateSensor.native_value returns None for None or non-numeric values."""
    # Configure the mock to return None value for the date sensor
    mock_kamstrup.get_values.return_value = {
        140: (None, "yy:mm:dd"),  # MinFlowDate_M with None value
    }

    config_entry = await setup_integration(hass)

    # Test the date sensor
    state = hass.states.get("sensor.kamstrup_403_minflowdate_m")
    assert state
    assert state.state == "unavailable"  # Entity should be unavailable when value is None

    await unload_integration(hass, config_entry)


async def test_date_sensor_returns_none_for_string_value(hass: HomeAssistant, mock_kamstrup: AsyncMock) -> None:
    """Test that KamstrupDateSensor.native_value returns None for string values."""
    # Configure the mock to return a string value (not float/int)
    mock_kamstrup.get_values.return_value = {
        140: ("invalid_date", "yy:mm:dd"),  # MinFlowDate_M with string value
    }

    config_entry = await setup_integration(hass)

    # Test the date sensor
    state = hass.states.get("sensor.kamstrup_403_minflowdate_m")
    assert state
    assert state.state == "unknown"  # Entity should be unknown when value is not numeric

    await unload_integration(hass, config_entry)
