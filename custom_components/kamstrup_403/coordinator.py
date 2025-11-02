"""DataUpdateCoordinator for kamstrup_403."""

import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from serial import SerialException

from .const import DOMAIN
from .pykamstrup.kamstrup import MULTIPLE_NBR_MAX, Kamstrup

_LOGGER: logging.Logger = logging.getLogger(__package__)


class KamstrupUpdateCoordinator(DataUpdateCoordinator[dict[int, Any]]):
    """Class to manage fetching data from the Kamstrup serial reader."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: Kamstrup,
        scan_interval: timedelta,
    ) -> None:
        """Initialize."""
        self.kamstrup = client

        self._commands: list[int] = []

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
    def commands(self) -> list[int]:
        """List of registered commands."""
        return self._commands

    async def _async_update_data(self) -> dict[int, Any]:
        """Update data via library."""
        _LOGGER.debug("Start update")

        data = {}
        failed_counter = 0

        # The amount of values that can request at once is limited, do it in chunks.
        chunks: list[list[int]] = [self._commands[i : i + MULTIPLE_NBR_MAX] for i in range(0, len(self._commands), MULTIPLE_NBR_MAX)]

        for chunk in chunks:
            _LOGGER.debug("Get values for %s", chunk)

            try:
                values = await self.kamstrup.get_values(chunk)
            except SerialException as exception:
                _LOGGER.warning("Device disconnected or multiple access on port?")
                raise UpdateFailed from exception
            except Exception as exception:
                _LOGGER.warning("Error reading multiple %s \nException: %s", chunk, exception)
                raise UpdateFailed from exception

            if values is None:
                _LOGGER.debug("No values returned for chunk %s", chunk)
                failed_counter += len(chunk)
                continue

            for command in chunk:
                if command in values:
                    value, unit = values[command]
                    data[command] = {"value": value, "unit": unit}
                    _LOGGER.debug("New value for sensor %s, value: %s %s", command, value, unit)
                else:
                    _LOGGER.debug("No value for sensor %s", command)
                    data[command] = {"value": None, "unit": None}
                    failed_counter += 1

        if failed_counter == len(self._commands):
            _LOGGER.error("Finished update, No readings from the meter. Please check the IR connection")
        else:
            _LOGGER.debug(
                "Finished update, %s out of %s readings failed",
                failed_counter,
                len(self._commands),
            )

        return data
