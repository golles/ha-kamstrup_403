"""Tests sensor."""

from homeassistant.components.sensor import SensorEntityDescription
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.kamstrup_403 import async_setup_entry
from custom_components.kamstrup_403.const import DOMAIN
from custom_components.kamstrup_403.sensor import KamstrupGasSensor, KamstrupMeterSensor

from .const import MOCK_CONFIG


async def test_kamstrup_gas_sensor(hass, bypass_get_data):
    """Test is_on function on base class."""
    config_entry = MockConfigEntry(domain=DOMAIN, data=MOCK_CONFIG, entry_id="test")
    await async_setup_entry(hass, config_entry)

    sensor = KamstrupGasSensor(
        hass.data[DOMAIN][config_entry.entry_id],
        config_entry.entry_id,
        SensorEntityDescription(
            key="gas",
            name="Heat Energy to Gas",
        ),
    )

    # Mock data.
    sensor.coordinator.data[60] = {"value": 1234, "unit": "GJ"}

    assert sensor.state == 1234


async def test_kamstrup_meter_sensor(hass, bypass_get_data):
    """Test is_on function on base class."""
    config_entry = MockConfigEntry(domain=DOMAIN, data=MOCK_CONFIG, entry_id="test")
    await async_setup_entry(hass, config_entry)

    sensor = KamstrupMeterSensor(
        hass.data[DOMAIN][config_entry.entry_id],
        config_entry.entry_id,
        SensorEntityDescription(
            key="60",
            name="Heat Energy (E1)",
        ),
    )

    # Mock data.
    sensor.coordinator.data[60] = {"value": 1234, "unit": "GJ"}

    assert sensor.int_key == 60
    assert sensor.state == 1234
    assert sensor.native_unit_of_measurement == "GJ"
