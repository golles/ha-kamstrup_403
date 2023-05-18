"""DataUpdateCoordinator for kamstrup_403."""
import logging
from typing import Any, List

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import serial

from .const import DOMAIN
from .pykamstrup.kamstrup import MULTIPLE_NBR_MAX, Kamstrup

_LOGGER: logging.Logger = logging.getLogger(__package__)


class KamstrupUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the Kamstrup serial reader."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: Kamstrup,
        scan_interval: int,
        device_info: DeviceInfo,
    ) -> None:
        """Initialize."""
        self.kamstrup = client
        self.device_info = device_info

        self._commands: List[int] = []

        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=scan_interval)

    def register_command(self, command: int) -> None:
        """Add a command to the commands list."""
        _LOGGER.debug("Register command %s", command)
        self._commands.append(command)

    def unregister_command(self, command: int) -> None:
        """Remove a command from the commands list."""
        _LOGGER.debug("Unregister command %s", command)
        self._commands.remove(command)

    @property
    def commands(self) -> List[int]:
        """List of registered commands"""
        return self._commands

    async def _async_update_data(self) -> dict[int, Any]:
        """Update data via library."""
        _LOGGER.debug("Start update")

        data = {}
        failed_counter = 0

        # The amount of values that can request at once is limited, do it in chunks.
        chunks: list[list[int]] = [
            self._commands[i : i + MULTIPLE_NBR_MAX]
            for i in range(0, len(self._commands), MULTIPLE_NBR_MAX)
        ]

        for chunk in chunks:
            _LOGGER.debug("Get values for %s", chunk)

            try:
                values = self.kamstrup.get_values(chunk)
            except serial.SerialException as exception:
                _LOGGER.error(
                    "Device disconnected or multiple access on port? \nException: %e",
                    exception,
                )
                raise UpdateFailed() from exception
            except Exception as exception:
                _LOGGER.error(
                    "Error reading multiple %s \nException: %s", chunk, exception
                )
                raise UpdateFailed() from exception

            for command in chunk:
                if command in values:
                    value, unit = values[command]
                    data[command] = {"value": value, "unit": unit}
                    _LOGGER.debug(
                        "New value for sensor %s, value: %s %s", command, value, unit
                    )

            failed_counter += len(chunk) - len(values)

        if failed_counter == len(data):
            _LOGGER.error(
                "Finished update, No readings from the meter. Please check the IR connection"
            )
        else:
            _LOGGER.debug(
                "Finished update, %s out of %s readings failed",
                failed_counter,
                len(data),
            )

        return data
