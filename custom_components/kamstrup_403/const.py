"""Constants for Kamstrup 403."""

from homeassistant.const import (
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_TEMPERATURE,
)
from homeassistant.components.sensor import (
    ATTR_STATE_CLASS,
    STATE_CLASS_MEASUREMENT,
    SensorStateClass,
)

# Base component constants
NAME = "Kamstrup 403"
DOMAIN = "kamstrup_403"
MODEL = "403"
MANUFACTURER = "Kamstrup"
ATTRIBUTION = "Data provided by Kamstrup 403 meter"

# Defaults
DEFAULT_BAUDRATE = 1200
DEFAULT_SCAN_INTERVAL = 60
DEFAULT_TIMEOUT = 2.0

# Platforms
SENSOR = "sensor"
PLATFORMS = [SENSOR]

# Sensors
SENSORS = {
    0x003C: {
        "name": "Heat Energy (E1)",
        "icon": "mdi:radiator",
        "command": 60,
        "device_class": DEVICE_CLASS_ENERGY,
        # has unit GJ which is unsupported for device_class energy
        # "attributes": [
        #     {
        #         "name": ATTR_STATE_CLASS,
        #         "value": SensorStateClass.TOTAL_INCREASING,
        #     },
        # ],
    },
    0x0050: {
        "name": "Power",
        "icon": "mdi:flash",
        "command": 80,
        "device_class": DEVICE_CLASS_POWER,
        "state_class": STATE_CLASS_MEASUREMENT,
        "attributes": [
            {
                "name": ATTR_STATE_CLASS,
                "value": STATE_CLASS_MEASUREMENT,
            },
        ],
    },
    0x0056: {
        "name": "Temp1",
        "icon": "mdi:thermometer",
        "command": 86,
        "device_class": DEVICE_CLASS_TEMPERATURE,
        "attributes": [
            {
                "name": ATTR_STATE_CLASS,
                "value": STATE_CLASS_MEASUREMENT,
            },
        ],
    },
    0x0057: {
        "name": "Temp2",
        "icon": "mdi:thermometer",
        "command": 87,
        "device_class": DEVICE_CLASS_TEMPERATURE,
        "attributes": [
            {
                "name": ATTR_STATE_CLASS,
                "value": STATE_CLASS_MEASUREMENT,
            },
        ],
    },
    0x0059: {
        "name": "Tempdiff",
        "icon": "mdi:thermometer",
        "command": 89,
        "device_class": DEVICE_CLASS_TEMPERATURE,
        "attributes": [
            {
                "name": ATTR_STATE_CLASS,
                "value": STATE_CLASS_MEASUREMENT,
            },
        ],
    },
    0x004A: {
        "name": "Flow",
        "icon": "mdi:water",
        "command": 74,
        "attributes": [
            {
                "name": ATTR_STATE_CLASS,
                "value": STATE_CLASS_MEASUREMENT,
            },
        ],
    },
    0x0044: {
        "name": "Volume",
        "icon": "mdi:water",
        "command": 68,
        "attributes": [
            {
                "name": ATTR_STATE_CLASS,
                "value": SensorStateClass.TOTAL_INCREASING,
            },
        ],
    },
    # 0x008D: {
    #     "name": "MinFlow_M",
    #     "icon": "mdi:water",
    #     "command": 141,
    #     "attributes": [
    #         {
    #             "name": ATTR_STATE_CLASS,
    #             "value": STATE_CLASS_MEASUREMENT,
    #         },
    #     ],
    # },
    # 0x008B: {
    #     "name": "MaxFlow_M",
    #     "icon": "mdi:water",
    #     "command": 139,
    #     "attributes": [
    #         {
    #             "name": ATTR_STATE_CLASS,
    #             "value": STATE_CLASS_MEASUREMENT,
    #         },
    #     ],
    # },
    # 0x008C: {
    #     "name": "MinFlowDate_M",
    #     "icon": "mdi:calendar",
    #     "command": 140,
    # },
    # 0x008A: {
    #     "name": "MaxFlowDate_M",
    #     "icon": "mdi:calendar",
    #     "command": 138,
    # },
    # 0x0091: {
    #     "name": "MinPower_M",
    #     "icon": "mdi:flash",
    #     "command": 145,
    #     "device_class": DEVICE_CLASS_POWER,
    #     "attributes": [
    #         {
    #             "name": ATTR_STATE_CLASS,
    #             "value": STATE_CLASS_MEASUREMENT,
    #         },
    #     ],
    # },
    # 0x008F: {
    #     "name": "MaxPower_M",
    #     "icon": "mdi:flash",
    #     "command": 143,
    #     "device_class": DEVICE_CLASS_POWER,
    #     "attributes": [
    #         {
    #             "name": ATTR_STATE_CLASS,
    #             "value": STATE_CLASS_MEASUREMENT,
    #         },
    #     ],
    # },
    # 0x0095: {
    #     "name": "AvgTemp1_M",
    #     "icon": "mdi:thermometer",
    #     "command": 149,
    #     "device_class": DEVICE_CLASS_TEMPERATURE,
    #     "attributes": [
    #         {
    #             "name": ATTR_STATE_CLASS,
    #             "value": STATE_CLASS_MEASUREMENT,
    #         },
    #     ],
    # },
    # 0x0096: {
    #     "name": "AvgTemp2_M",
    #     "icon": "mdi:thermometer",
    #     "command": 150,
    #     "device_class": DEVICE_CLASS_TEMPERATURE,
    #     "attributes": [
    #         {
    #             "name": ATTR_STATE_CLASS,
    #             "value": STATE_CLASS_MEASUREMENT,
    #         },
    #     ],
    # },
    # 0x0090: {
    #     "name": "MinPowerDate_M",
    #     "icon": "mdi:calendar",
    #     "command": 144,
    # },
    # 0x008E: {
    #     "name": "MaxPowerDate_M",
    #     "icon": "mdi:calendar",
    #     "command": 142,
    # },
    # 0x007E: {
    #     "name": "MinFlow_Y",
    #     "icon": "mdi:water",
    #     "command": 126,
    #     "device_class": DEVICE_CLASS_TEMPERATURE,
    #     "attributes": [
    #         {
    #             "name": ATTR_STATE_CLASS,
    #             "value": STATE_CLASS_MEASUREMENT,
    #         },
    #     ],
    # },
    # 0x007C: {
    #     "name": "MaxFlow_Y",
    #     "icon": "mdi:water",
    #     "command": 124,
    # },
    # 0x007D: {
    #     "name": "MinFlowDate_Y",
    #     "icon": "mdi:calendar",
    #     "command": 125,
    # },
    # 0x007B: {
    #     "name": "MaxFlowDate_Y",
    #     "icon": "mdi:calendar",
    #     "command": 123,
    # },
    # 0x0082: {
    #     "name": "MinPower_Y",
    #     "icon": "mdi:flash",
    #     "command": 130,
    # },
    # 0x0080: {
    #     "name": "MaxPower_Y",
    #     "icon": "mdi:flash",
    #     "command": 128,
    # },
    # 0x0092: {
    #     "name": "AvgTemp1_Y",
    #     "icon": "mdi:thermometer",
    #     "command": 146,
    #     "device_class": DEVICE_CLASS_TEMPERATURE,
    #     "attributes": [
    #         {
    #             "name": ATTR_STATE_CLASS,
    #             "value": STATE_CLASS_MEASUREMENT,
    #         },
    #     ],
    # },
    # 0x0093: {
    #     "name": "AvgTemp2_Y",
    #     "icon": "mdi:thermometer",
    #     "command": 147,
    #     "device_class": DEVICE_CLASS_TEMPERATURE,
    #     "attributes": [
    #         {
    #             "name": ATTR_STATE_CLASS,
    #             "value": STATE_CLASS_MEASUREMENT,
    #         },
    #     ],
    # },
    # 0x0081: {
    #     "name": "MinPowerDate_Y",
    #     "icon": "mdi:calendar",
    #     "command": 129,
    # },
    # 0x007F: {
    #     "name": "MaxPowerDate_Y",
    #     "icon": "mdi:calendar",
    #     "command": 127,
    # },
    0x0061: {
        "name": "Temp1xm3",
        "icon": "mdi:thermometer",
        "command": 97,
        "device_class": DEVICE_CLASS_TEMPERATURE,
        # has unit m3xC which is unsupported for device_class temperature
        # "attributes": [
        #     {
        #         "name": ATTR_STATE_CLASS,
        #         "value": STATE_CLASS_MEASUREMENT,
        #     },
        # ],
    },
    0x006E: {
        "name": "Temp2xm3",
        "icon": "mdi:thermometer",
        "command": 110,
        "device_class": DEVICE_CLASS_TEMPERATURE,
        # has unit m3xC which is unsupported for device_class temperature
        # "attributes": [
        #     {
        #         "name": ATTR_STATE_CLASS,
        #         "value": STATE_CLASS_MEASUREMENT,
        #     },
        # ],
    },
    0x0071: {
        "name": "Infoevent",
        "icon": "mdi:eye",
        "command": 113,
    },
    0x03EC: {
        "name": "HourCounter",
        "icon": "mdi:timer-sand",
        "command": 1004,
        "state_class": STATE_CLASS_MEASUREMENT,
        "attributes": [
            {
                "name": ATTR_STATE_CLASS,
                "value": SensorStateClass.TOTAL_INCREASING,
            },
        ],
    },
}
