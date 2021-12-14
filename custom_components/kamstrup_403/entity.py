"""KamstrupEntity class"""
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, NAME, ATTRIBUTION, MANUFACTURER, MODEL, CONF_PORT


class KamstrupEntity(CoordinatorEntity):
    def __init__(self, coordinator, config_entry):
        super().__init__(coordinator)
        self.config_entry = config_entry

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return f"{self.config_entry.entry_id}-{self.name}"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.config_entry.data.get(CONF_PORT))},
            "name": NAME,
            "model": MODEL,
            "manufacturer": MANUFACTURER,
        }

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            "attribution": ATTRIBUTION,
            "integration": DOMAIN,
        }
