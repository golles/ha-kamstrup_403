"""Constants for kamstrup_403 tests."""
from homeassistant.const import CONF_PORT, CONF_SCAN_INTERVAL, CONF_TIMEOUT

# Mock config data to be used across multiple tests
MOCK_CONFIG = {CONF_PORT: "/dev/ttyUSB0"}
MOCK_UPDATE_CONFIG = {CONF_SCAN_INTERVAL: 120, CONF_TIMEOUT: 1.0}
