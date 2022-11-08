"""Sensor platform for kamstrup_403."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import (
    DOMAIN as SENSOR_DOMAIN,
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import KamstrupUpdateCoordinator
from .const import DEFAULT_NAME, DOMAIN

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
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="86",  # 0x0056
        name="Temp1",
        icon="mdi:thermometer",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="87",  # 0x0057
        name="Temp2",
        icon="mdi:thermometer",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="89",  # 0x0059
        name="Tempdiff",
        icon="mdi:thermometer",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="74",  # 0x004A
        name="Flow",
        icon="mdi:water",
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="68",  # 0x0044
        name="Volume",
        icon="mdi:water",
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="141",  # 0x008D
        name="MinFlow_M",
        icon="mdi:water",
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="139",  # 0x008B
        name="MaxFlow_M",
        icon="mdi:water",
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="140",  # 0x008C
        name="MinFlowDate_M",
        icon="mdi:calendar",
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="138",  # 0x008A
        name="MaxFlowDate_M",
        icon="mdi:calendar",
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="145",  # 0x0091
        name="MinPower_M",
        icon="mdi:flash",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="143",  # 0x008F
        name="MaxPower_M",
        icon="mdi:flash",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="149",  # 0x0095
        name="AvgTemp1_M",
        icon="mdi:thermometer",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="150",  # 0x0096
        name="AvgTemp2_M",
        icon="mdi:thermometer",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="144",  # 0x0090
        name="MinPowerDate_M",
        icon="mdi:calendar",
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="142",  # 0x008E
        name="MaxPowerDate_M",
        icon="mdi:calendar",
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="126",  # 0x007E
        name="MinFlow_Y",
        icon="mdi:water",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="124",  # 0x0096
        name="MaxFlow_Y",
        icon="mdi:water",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="125",  # 0x007D
        name="MinFlowDate_Y",
        icon="mdi:calendar",
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="123",  # 0x007B
        name="MaxFlowDate_Y",
        icon="mdi:calendar",
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="130",  # 0x0082
        name="MinPower_Y",
        icon="mdi:flash",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="128",  # 0x0080
        name="MaxPower_Y",
        icon="mdi:flash",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="146",  # 0x0092
        name="AvgTemp1_Y",
        icon="mdi:thermometer",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="147",  # 0x0093
        name="AvgTemp2_Y",
        icon="mdi:thermometer",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="129",  # 0x0081
        name="MinPowerDate_Y",
        icon="mdi:calendar",
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="127",  # 0x007F
        name="MaxPowerDate_Y",
        icon="mdi:calendar",
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="97",  # 0x0061
        name="Temp1xm3",
        icon="mdi:thermometer",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="110",  # 0x006E
        name="Temp2xm3",
        icon="mdi:thermometer",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
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


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Kamstrup sensors based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        KamstrupSensor(
            coordinator=coordinator,
            entry_id=entry.entry_id,
            description=description,
        )
        for description in DESCRIPTIONS
    )


class KamstrupSensor(CoordinatorEntity[KamstrupUpdateCoordinator], SensorEntity):
    """Defines a Kamstrup sensor."""

    def __init__(
        self,
        coordinator: KamstrupUpdateCoordinator,
        entry_id: str,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize Kamstrup sensor."""
        super().__init__(coordinator=coordinator)

        self.entity_id = f"{SENSOR_DOMAIN}.{DEFAULT_NAME}_{description.name}".lower()
        self.entity_description = description
        self._attr_unique_id = f"{entry_id}-{DEFAULT_NAME} {self.name}"
        self._attr_device_info = coordinator.device_info

    async def async_added_to_hass(self) -> None:
        """Run when entity about to be added to hass."""
        self.coordinator.register_command(self.entity_description.key)

    async def async_will_remove_from_hass(self) -> None:
        """Run when entity will be removed from hass."""
        self.coordinator.unregister_command(self.entity_description.key)

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        if self.coordinator.data and self.coordinator.data[self.entity_description.key]:
            return self.coordinator.data[self.entity_description.key].get("value")

        return None

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return the unit of measurement of the sensor, if any."""
        if self.coordinator.data and self.coordinator.data[self.entity_description.key]:
            return self.coordinator.data[self.entity_description.key].get("unit")

        return None
