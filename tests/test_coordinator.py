"""Test for data update coordinator."""

from datetime import timedelta
from unittest.mock import Mock

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import UpdateFailed
from serial import SerialException

from custom_components.kamstrup_403.const import DOMAIN
from custom_components.kamstrup_403.coordinator import KamstrupUpdateCoordinator


@pytest.fixture(name="coordinator")
def fixture_coordinator(hass: HomeAssistant, mock_kamstrup: Mock) -> KamstrupUpdateCoordinator:
    """Create a test coordinator."""
    scan_interval = timedelta(seconds=30)
    return KamstrupUpdateCoordinator(hass, mock_kamstrup, scan_interval)


def test_init(coordinator: KamstrupUpdateCoordinator, mock_kamstrup: Mock) -> None:
    """Test coordinator initialization."""
    assert coordinator.name == DOMAIN
    assert coordinator.kamstrup == mock_kamstrup
    assert coordinator.update_interval == timedelta(seconds=30)
    assert coordinator.commands == []


def test_register_command(coordinator: KamstrupUpdateCoordinator) -> None:
    """Test registering a command."""
    command = 60
    coordinator.register_command(command)
    assert command in coordinator.commands
    assert coordinator.commands == [60]


def test_register_multiple_commands(coordinator: KamstrupUpdateCoordinator) -> None:
    """Test registering multiple commands."""
    commands = [60, 68, 80]
    for command in commands:
        coordinator.register_command(command)

    assert coordinator.commands == commands


def test_unregister_command(coordinator: KamstrupUpdateCoordinator) -> None:
    """Test unregistering a command."""
    commands = [60, 68, 80]
    for command in commands:
        coordinator.register_command(command)

    coordinator.unregister_command(68)
    assert coordinator.commands == [60, 80]


def test_unregister_nonexistent_command_raises_error(coordinator: KamstrupUpdateCoordinator) -> None:
    """Test unregistering a command that doesn't exist raises ValueError."""
    with pytest.raises(ValueError, match=r"list\.remove\(x\): x not in list"):
        coordinator.unregister_command(999)


def test_commands_property(coordinator: KamstrupUpdateCoordinator) -> None:
    """Test the commands property."""
    assert coordinator.commands == []

    coordinator.register_command(60)
    coordinator.register_command(68)

    assert coordinator.commands == [60, 68]


async def test_async_update_data_successful(coordinator: KamstrupUpdateCoordinator, mock_kamstrup: Mock) -> None:
    """Test successful data update."""
    # Setup commands
    commands = [60, 68, 80]
    for command in commands:
        coordinator.register_command(command)

    # Mock successful response
    mock_values = {
        60: (1234.0, "GJ"),
        68: (5678.0, "m³"),
        80: (90.5, "kW"),
    }
    mock_kamstrup.get_values.return_value = mock_values

    # Execute update
    result = await coordinator._async_update_data()  # pylint: disable=protected-access

    # Verify results
    assert len(result) == 3
    assert result[60] == {"value": 1234.0, "unit": "GJ"}
    assert result[68] == {"value": 5678.0, "unit": "m³"}
    assert result[80] == {"value": 90.5, "unit": "kW"}

    # Verify kamstrup was called with correct commands
    mock_kamstrup.get_values.assert_called_once_with(commands)


async def test_async_update_data_with_chunking(coordinator: KamstrupUpdateCoordinator, mock_kamstrup: Mock) -> None:
    """Test data update with command chunking (more than 8 commands)."""
    # Setup more than 8 commands to trigger chunking
    commands = [60, 63, 68, 74, 80, 86, 87, 89, 97, 99, 110, 113]
    for command in commands:
        coordinator.register_command(command)

    # Mock successful responses for both chunks
    def mock_get_values(chunk: list[int]) -> dict[int, tuple[float, str]]:
        # Return values for each command in the chunk
        return {cmd: (float(cmd), "unit") for cmd in chunk}

    mock_kamstrup.get_values.side_effect = mock_get_values

    # Execute update
    result = await coordinator._async_update_data()  # pylint: disable=protected-access

    # Verify results
    assert len(result) == 12
    for command in commands:
        assert result[command] == {"value": float(command), "unit": "unit"}

    # Verify kamstrup was called twice (two chunks)
    assert mock_kamstrup.get_values.call_count == 2


async def test_async_update_data_partial_success(coordinator: KamstrupUpdateCoordinator, mock_kamstrup: Mock) -> None:
    """Test data update with partial success (some commands missing from response)."""
    commands = [60, 68, 80]
    for command in commands:
        coordinator.register_command(command)

    # Mock response missing some commands
    mock_values = {
        60: (1234.0, "GJ"),
        # 68 is missing
        80: (90.5, "kW"),
    }
    mock_kamstrup.get_values.return_value = mock_values

    result = await coordinator._async_update_data()  # pylint: disable=protected-access

    # Verify results
    assert len(result) == 3
    assert result[60] == {"value": 1234.0, "unit": "GJ"}
    assert result[68] == {"value": None, "unit": None}  # Missing command
    assert result[80] == {"value": 90.5, "unit": "kW"}


async def test_async_update_data_serial_exception(coordinator: KamstrupUpdateCoordinator, mock_kamstrup: Mock) -> None:
    """Test data update with serial exception."""
    commands = [60, 68]
    for command in commands:
        coordinator.register_command(command)

    # Mock serial exception
    exception_msg = "Connection failed"
    mock_kamstrup.get_values.side_effect = SerialException(exception_msg)

    # Execute update and expect UpdateFailed
    with pytest.raises(UpdateFailed):
        await coordinator._async_update_data()  # pylint: disable=protected-access

    mock_kamstrup.get_values.assert_called_once_with(commands)


async def test_async_update_data_general_exception(coordinator: KamstrupUpdateCoordinator, mock_kamstrup: Mock) -> None:
    """Test data update with general exception."""
    commands = [60, 68]
    for command in commands:
        coordinator.register_command(command)

    # Mock general exception
    exception_msg = "Unexpected error"
    mock_kamstrup.get_values.side_effect = Exception(exception_msg)

    # Execute update and expect UpdateFailed
    with pytest.raises(UpdateFailed):
        await coordinator._async_update_data()  # pylint: disable=protected-access

    mock_kamstrup.get_values.assert_called_once_with(commands)


async def test_async_update_data_returns_none(coordinator: KamstrupUpdateCoordinator, mock_kamstrup: Mock) -> None:
    """Test data update when kamstrup returns None."""
    commands = [60, 68, 80]
    for command in commands:
        coordinator.register_command(command)

    # Mock None response
    mock_kamstrup.get_values.return_value = None

    result = await coordinator._async_update_data()  # pylint: disable=protected-access

    # When values is None, the chunk is skipped with continue, so no entries are added
    assert result == {}


async def test_async_update_data_chunk_returns_none_but_adds_entries(coordinator: KamstrupUpdateCoordinator, mock_kamstrup: Mock) -> None:
    """Test data update when some commands are processed as None values."""
    commands = [60, 68, 80]
    for command in commands:
        coordinator.register_command(command)

    # Mock successful response but missing some commands
    mock_values = {
        60: (1234.0, "GJ"),
        # 68 and 80 missing from response
    }
    mock_kamstrup.get_values.return_value = mock_values

    result = await coordinator._async_update_data()  # pylint: disable=protected-access

    # All commands should have entries, missing ones get None values
    assert len(result) == 3
    assert result[60] == {"value": 1234.0, "unit": "GJ"}
    assert result[68] == {"value": None, "unit": None}
    assert result[80] == {"value": None, "unit": None}


async def test_async_update_data_mixed_chunks_with_failures(coordinator: KamstrupUpdateCoordinator, mock_kamstrup: Mock) -> None:
    """Test data update with mixed success/failure across chunks."""
    # Setup commands to create multiple chunks
    commands = [60, 63, 68, 74, 80, 86, 87, 89, 97]  # 9 commands = 2 chunks
    for command in commands:
        coordinator.register_command(command)

    # Mock responses: first chunk succeeds, second returns None
    responses = [
        {
            60: (1234.0, "GJ"),
            63: (5678.0, "MJ"),
            68: (90.0, "m³"),
            74: (12.5, "m³/h"),
            80: (45.0, "kW"),
            86: (25.0, "°C"),
            87: (30.0, "°C"),
            89: (5.0, "°C"),
        },  # First chunk success
        None,  # Second chunk returns None
    ]
    mock_kamstrup.get_values.side_effect = responses

    result = await coordinator._async_update_data()  # pylint: disable=protected-access

    # Verify results - only first chunk commands get entries (second chunk is skipped)
    assert len(result) == 8

    # First chunk commands should have values
    expected_first_chunk = [60, 63, 68, 74, 80, 86, 87, 89]
    for command in expected_first_chunk:
        assert result[command]["value"] is not None
        assert result[command]["unit"] is not None

    # Second chunk command (97) should not be in result due to None response
    assert 97 not in result


async def test_async_update_data_no_commands(coordinator: KamstrupUpdateCoordinator, mock_kamstrup: Mock) -> None:
    """Test data update with no registered commands."""
    # Don't register any commands
    result = await coordinator._async_update_data()  # pylint: disable=protected-access

    # Should return empty dict
    assert result == {}

    # Kamstrup should not be called
    mock_kamstrup.get_values.assert_not_called()


async def test_async_update_data_exception_in_middle_chunk(coordinator: KamstrupUpdateCoordinator, mock_kamstrup: Mock) -> None:
    """Test data update where exception occurs in middle chunk."""
    # Setup commands to create multiple chunks
    commands = list(range(60, 77))  # 17 commands = 3 chunks
    for command in commands:
        coordinator.register_command(command)

    # Mock responses: first succeeds, second fails, third never reached
    def side_effect(chunk: list[int]) -> dict[int, tuple[float, str]]:
        if chunk[0] == 60:  # First chunk
            return {cmd: (float(cmd), "unit") for cmd in chunk}
        if chunk[0] == 68:  # Second chunk
            exception_msg = "Connection lost"
            raise SerialException(exception_msg)
        # Should not reach third chunk
        pytest.fail("Should not reach third chunk after exception")
        return {}

    mock_kamstrup.get_values.side_effect = side_effect

    # Execute update and expect UpdateFailed
    with pytest.raises(UpdateFailed):
        await coordinator._async_update_data()  # pylint: disable=protected-access

    # Should only be called twice (first chunk success, second chunk fails)
    assert mock_kamstrup.get_values.call_count == 2


async def test_async_update_data_all_commands_fail(coordinator: KamstrupUpdateCoordinator, mock_kamstrup: Mock) -> None:
    """Test data update where all commands fail."""
    commands = [60, 68, 80]
    for command in commands:
        coordinator.register_command(command)

    # Mock empty response (no matching commands)
    mock_kamstrup.get_values.return_value = {}

    result = await coordinator._async_update_data()  # pylint: disable=protected-access

    # All commands should have None values
    assert len(result) == 3
    for command in commands:
        assert result[command] == {"value": None, "unit": None}
