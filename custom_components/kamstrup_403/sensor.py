"""Sensor platform for kamstrup_403."""
from homeassistant.components.sensor import SensorEntity

from .const import DOMAIN, SENSOR, SENSORS, MANUFACTURER, MODEL
from .entity import KamstrupEntity


import logging

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    _LOGGER.debug("async_setup_entry")

    for key in SENSORS:
        _LOGGER.debug("add sensor %s", SENSORS[key]["name"])
        async_add_devices(
            [
                KamstrupSensor(
                    coordinator,
                    entry,
                    SENSORS[key].get("name", None),
                    SENSORS[key].get("icon", None),
                    SENSORS[key].get("device_class", None),
                    SENSORS[key].get("attributes", []),
                    SENSORS[key].get("command", None),
                )
            ]
        )


class KamstrupSensor(KamstrupEntity, SensorEntity):
    """Kamstrup Sensor class."""

    def __init__(
        self,
        coordinator,
        config_entry,
        name,
        icon,
        device_class,
        attributes,
        command,
    ):
        super().__init__(coordinator, config_entry)
        self.coordinator = coordinator
        self._name = "{} {} {}".format(MANUFACTURER, MODEL, name)
        self._icon = icon
        self._device_class = device_class
        self._attributes = attributes
        self._command = command

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def native_value(self):
        """Return the native_value of the sensor."""
        return self.coordinator.data[self._command].get("value")

    @property
    def native_unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return self.coordinator.data[self._command].get("unit")

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return self._icon

    @property
    def device_class(self):
        """Return the device class."""
        return self._device_class

    @property
    def extra_state_attributes(self):
        """Return the device state attributes."""
        attributes = super().extra_state_attributes
        for attribute in self._attributes:
            attributes[attribute.get("name", None)] = attribute.get("value", None)

        return attributes
