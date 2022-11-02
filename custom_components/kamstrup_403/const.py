"""Constants for Kamstrup 403."""

from typing import Final
import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.helpers.entity import EntityCategory

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
        key="60",  # 0x003C
        name="Heat Energy (E1)",
        icon="mdi:radiator",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="80",  # 0x0050
        name="Power",
        icon="mdi:flash",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        # entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="86",  # 0x0056
        name="Temp1",
        icon="mdi:thermometer",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="87",  # 0x0057
        name="Temp2",
        icon="mdi:thermometer",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="89",  # 0x0059
        name="Tempdiff",
        icon="mdi:thermometer",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        # entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="74",  # 0x004A
        name="Flow",
        icon="mdi:water",
        state_class=SensorStateClass.MEASUREMENT,
        # entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="68",  # 0x0044
        name="Volume",
        icon="mdi:water",
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    # SensorEntityDescription(
    #     key="141",  # 0x008D
    #     name="MinFlow_M",
    #     icon="mdi:water",
    #     state_class=SensorStateClass.MEASUREMENT,
    #     entity_registry_enabled_default=False,
    # ),
    # SensorEntityDescription(
    #     key="139",  # 0x008B
    #     name="MaxFlow_M",
    #     icon="mdi:water",
    #     state_class=SensorStateClass.MEASUREMENT,
    #     entity_registry_enabled_default=False,
    # ),
    # SensorEntityDescription(
    #     key="140",  # 0x008C
    #     name="MinFlowDate_M",
    #     icon="mdi:calendar",
    #     entity_registry_enabled_default=False,
    # ),
    # SensorEntityDescription(
    #     key="138",  # 0x008A
    #     name="MaxFlowDate_M",
    #     icon="mdi:calendar",
    #     entity_registry_enabled_default=False,
    # ),
    # SensorEntityDescription(
    #     key="145",  # 0x0091
    #     name="MinPower_M",
    #     icon="mdi:flash",
    #     device_class=SensorDeviceClass.POWER,
    #     state_class=SensorStateClass.MEASUREMENT,
    #     entity_registry_enabled_default=False,
    # ),
    # SensorEntityDescription(
    #     key="143",  # 0x008F
    #     name="MaxPower_M",
    #     icon="mdi:flash",
    #     device_class=SensorDeviceClass.POWER,
    #     state_class=SensorStateClass.MEASUREMENT,
    #     entity_registry_enabled_default=False,
    # ),
    # SensorEntityDescription(
    #     key="149",  # 0x0095
    #     name="AvgTemp1_M",
    #     icon="mdi:thermometer",
    #     device_class=SensorDeviceClass.TEMPERATURE,
    #     state_class=SensorStateClass.MEASUREMENT,
    #     entity_registry_enabled_default=False,
    # ),
    # SensorEntityDescription(
    #     key="150",  # 0x0096
    #     name="AvgTemp2_M",
    #     icon="mdi:thermometer",
    #     device_class=SensorDeviceClass.TEMPERATURE,
    #     state_class=SensorStateClass.MEASUREMENT,
    #     entity_registry_enabled_default=False,
    # ),
    # SensorEntityDescription(
    #     key="144",  # 0x0090
    #     name="MinPowerDate_M",
    #     icon="mdi:calendar",
    #     entity_registry_enabled_default=False,
    # ),
    # SensorEntityDescription(
    #     key="142",  # 0x008E
    #     name="MaxPowerDate_M",
    #     icon="mdi:calendar",
    #     entity_registry_enabled_default=False,
    # ),
    # SensorEntityDescription(
    #     key="126",  # 0x007E
    #     name="MinFlow_Y",
    #     icon="mdi:water",
    #     device_class=SensorDeviceClass.TEMPERATURE,
    #     state_class=SensorStateClass.MEASUREMENT,
    #     entity_registry_enabled_default=False,
    # ),
    # SensorEntityDescription(
    #     key="124",  # 0x0096
    #     name="MaxFlow_Y",
    #     icon="mdi:water",
    #     device_class=SensorDeviceClass.TEMPERATURE,
    #     state_class=SensorStateClass.MEASUREMENT,
    #     entity_registry_enabled_default=False,
    # ),
    # SensorEntityDescription(
    #     key="125",  # 0x007D
    #     name="MinFlowDate_Y",
    #     icon="mdi:calendar",
    #     entity_registry_enabled_default=False,
    # ),
    # SensorEntityDescription(
    #     key="123",  # 0x007B
    #     name="MaxFlowDate_Y",
    #     icon="mdi:calendar",
    #     entity_registry_enabled_default=False,
    # ),
    # SensorEntityDescription(
    #     key="130",  # 0x0082
    #     name="MinPower_Y",
    #     icon="mdi:flash",
    #     device_class=SensorDeviceClass.POWER,
    #     state_class=SensorStateClass.MEASUREMENT,
    #     entity_registry_enabled_default=False,
    # ),
    # SensorEntityDescription(
    #     key="128",  # 0x0080
    #     name="MaxPower_Y",
    #     icon="mdi:flash",
    #     device_class=SensorDeviceClass.POWER,
    #     state_class=SensorStateClass.MEASUREMENT,
    #     entity_registry_enabled_default=False,
    # ),
    # SensorEntityDescription(
    #     key="146",  # 0x0092
    #     name="AvgTemp1_Y",
    #     icon="mdi:thermometer",
    #     device_class=SensorDeviceClass.TEMPERATURE,
    #     state_class=SensorStateClass.MEASUREMENT,
    #     entity_registry_enabled_default=False,
    # ),
    # SensorEntityDescription(
    #     key="147",  # 0x0093
    #     name="AvgTemp2_Y",
    #     icon="mdi:thermometer",
    #     device_class=SensorDeviceClass.TEMPERATURE,
    #     state_class=SensorStateClass.MEASUREMENT,
    #     entity_registry_enabled_default=False,
    # ),
    # SensorEntityDescription(
    #     key="129",  # 0x0081
    #     name="MinPowerDate_Y",
    #     icon="mdi:calendar",
    #     entity_registry_enabled_default=False,
    # ),
    # SensorEntityDescription(
    #     key="127",  # 0x007F
    #     name="MaxPowerDate_Y",
    #     icon="mdi:calendar",
    #     entity_registry_enabled_default=False,
    # ),
    SensorEntityDescription(
        key="97",  # 0x0061
        name="Temp1xm3",
        icon="mdi:thermometer",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        # entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="110",  # 0x006E
        name="Temp2xm3",
        icon="mdi:thermometer",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        # entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="113",  # 0x0071
        name="Infoevent",
        icon="mdi:eye",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="1004",  # 0x03EC
        name="HourCounter",
        icon="mdi:timer-sand",
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
]
