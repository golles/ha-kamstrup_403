"""Global fixtures for the custom component."""

from collections.abc import Generator
from unittest.mock import AsyncMock, Mock, PropertyMock, patch

import pytest

from custom_components.kamstrup_403.pykamstrup.kamstrup import Kamstrup


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations: Generator) -> Generator[None]:
    """Enable custom integrations."""
    return enable_custom_integrations


@pytest.fixture(name="enable_all_entities", autouse=True)
def fixture_enable_all_entities() -> Generator[None]:
    """Make sure all entities are enabled."""
    with patch(
        "homeassistant.helpers.entity.Entity.entity_registry_enabled_default",
        PropertyMock(return_value=True),
    ):
        yield


@pytest.fixture(autouse=True, name="mock_kamstrup")
def fixture_mock_kamstrup() -> Generator[AsyncMock]:
    """Auto-patch Kamstrup in all tests and return the mock for configuration."""
    mock_client = AsyncMock(spec=Kamstrup)
    # Set up default behavior - tests can override this
    mock_client.get_values.return_value = {
        60: (1234.0, "GJ"),
        68: (5678.0, "m³"),
        99: (0, None),
        113: (1, None),
        140: (230123.0, "yy:mm:dd"),
        1001: (12345678, None),
        1004: (12345.0, "h"),
    }

    mock_client_class = Mock(return_value=mock_client)

    with (
        patch("custom_components.kamstrup_403.Kamstrup", mock_client_class),
        patch("custom_components.kamstrup_403.config_flow.Kamstrup", mock_client_class),
    ):
        yield mock_client
