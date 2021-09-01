"""Sensor platform for kamstrup_403."""
from .const import DOMAIN, SENSOR, SENSORS, MANUFACTURER, MODEL
from .entity import KamstrupEntity


import logging
_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    _LOGGER.debug('async_setup_entry')

    for key in SENSORS:
        _LOGGER.debug('add sensor %s', SENSORS[key]["name"])
        async_add_devices(
            [
                KamstrupSensor(
                    coordinator,
                    entry,
                    SENSORS[key]["name"],
                    SENSORS[key]["icon"],
                    SENSORS[key]["command"],
                )
            ]
        )


class KamstrupSensor(KamstrupEntity):
    """Kamstrup Sensor class."""

    def __init__(self, coordinator, config_entry, name, icon, command):
        super().__init__(coordinator, config_entry)
        self.coordinator = coordinator
        self._name = "{} {} {}".format(MANUFACTURER, MODEL, name)
        self._icon = icon
        self._command = command

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data[self._command].get("value")

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return self.coordinator.data[self._command].get("unit")

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return self._icon
