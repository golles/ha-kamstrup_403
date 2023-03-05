"""Constants for Kamstrup 403."""

from typing import Final

# Base component constants
NAME: Final = "Kamstrup 403"
DOMAIN: Final = "kamstrup_403"
VERSION: Final = "2.4.0"
MODEL: Final = "403"
MANUFACTURER: Final = "Kamstrup"
ATTRIBUTION: Final = "Data provided by Kamstrup 403 meter"

# Defaults
DEFAULT_NAME: Final = NAME
DEFAULT_BAUDRATE: Final = 1200
DEFAULT_SCAN_INTERVAL: Final = 3600
DEFAULT_TIMEOUT: Final = 1.0

# Platforms
SENSOR: Final = "sensor"
PLATFORMS: Final = [SENSOR]
