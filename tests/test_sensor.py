"""Tests sensor."""
import datetime

from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.core import HomeAssistant
from homeassistant.util import dt
from pytest_homeassistant_custom_component.common import async_fire_time_changed

from custom_components.kamstrup_403.const import DOMAIN
from custom_components.kamstrup_403.sensor import (
    KamstrupDateSensor,
    KamstrupGasSensor,
    KamstrupMeterSensor,
)

from . import setup_component


async def test_kamstrup_gas_sensor(hass: HomeAssistant, bypass_get_data):
    """Test for gas sensor."""
    config_entry = await setup_component(hass)

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

    async_fire_time_changed(
        hass,
        datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=1),
    )
    await hass.async_block_till_done()

    assert sensor.state == 1234


async def test_kamstrup_meter_sensor(hass: HomeAssistant, bypass_get_data):
    """Test for base sensor."""
    config_entry = await setup_component(hass)

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

    async_fire_time_changed(
        hass,
        datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=1),
    )
    await hass.async_block_till_done()

    assert sensor.int_key == 60
    assert sensor.state == 1234
    assert sensor.native_unit_of_measurement == "GJ"


async def test_kamstrup_date_sensor(hass: HomeAssistant, bypass_get_data):
    """Test for date sensor."""
    config_entry = await setup_component(hass)

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

    async_fire_time_changed(
        hass,
        datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=1),
    )
    await hass.async_block_till_done()

    assert sensor.int_key == 140
    assert sensor.state == dt.as_local(datetime.datetime(2023, 1, 23))
    assert sensor.native_unit_of_measurement is None
