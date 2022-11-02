"""Constants for Kamstrup 403."""

from typing import Final
import logging

from homeassistant.const import (
    # ENERGY_GIGA_JOULE,
    VOLUME_CUBIC_METERS,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)

# Base component constants
NAME: Final = "Kamstrup 403"
DOMAIN: Final = "kamstrup_403"
VERSION: Final = "2.0.0"
MODEL: Final = "403"
MANUFACTURER: Final = "Kamstrup"
ATTRIBUTION: Final = "Data provided by Kamstrup 403 meter"

# Defaults
_LOGGER: logging.Logger = logging.getLogger(__package__)
DEFAULT_NAME: Final = NAME
DEFAULT_BAUDRATE: Final = 1200
DEFAULT_SCAN_INTERVAL: Final = 3600
DEFAULT_TIMEOUT: Final = 0.2

# Platforms
SENSOR = "sensor"
PLATFORMS = [SENSOR]

DESCRIPTIONS: list[SensorEntityDescription] = [
    SensorEntityDescription(
        # key="60",
        # native_unit_of_measurement=ENERGY_GIGA_JOULE, # TODO 2022.11
        # state_class=SensorStateClass.TOTAL_INCREASING, # TODO 2022.11
        key="0x003C",
        name="Heat Energy (E1)",
        native_unit_of_measurement="GJ",
        icon="mdi:radiator",
        device_class=SensorDeviceClass.ENERGY,
    ),
    SensorEntityDescription(
        # key="68",
        key="0x0044",
        name="Volume",
        native_unit_of_measurement=VOLUME_CUBIC_METERS,
        icon="mdi:water",
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
]