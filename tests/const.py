"""Constants for kamstrup_403 tests."""
from homeassistant.const import CONF_PORT, CONF_SCAN_INTERVAL

# Mock config data to be used across multiple tests
MOCK_CONFIG = {CONF_PORT: "/dev/ttyUSB0"}
MOCK_UPDATE_CONFIG = {CONF_SCAN_INTERVAL: 120}
