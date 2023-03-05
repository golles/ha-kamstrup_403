"""Tests sensor."""

from datetime import datetime

from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.util import dt
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.kamstrup_403 import async_setup_entry
from custom_components.kamstrup_403.const import DOMAIN
from custom_components.kamstrup_403.sensor import (
    KamstrupDateSensor,
    KamstrupGasSensor,
    KamstrupMeterSensor,
)

from .const import MOCK_CONFIG


async def test_kamstrup_gas_sensor(hass, bypass_get_data):
    """Test for gas sensor."""
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
    """Test for base sensor."""
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


async def test_kamstrup_date_sensor(hass, bypass_get_data):
    """Test for date sensor."""
    config_entry = MockConfigEntry(domain=DOMAIN, data=MOCK_CONFIG, entry_id="test")
    await async_setup_entry(hass, config_entry)

    sensor = KamstrupDateSensor(
        hass.data[DOMAIN][config_entry.entry_id],
        config_entry.entry_id,
        SensorEntityDescription(
            key="140",  # 0x008C
            name="MinFlowDate_M",
        ),
    )

    # Mock data.
    sensor.coordinator.data[140] = {"value": 230123.0, "unit": "yy:mm:dd"}

    assert sensor.int_key == 140
    assert sensor.state == dt.as_local(datetime(2023, 1, 23))
    assert sensor.native_unit_of_measurement is None
