"""Tests for Kamstrup class."""

import math
from unittest.mock import MagicMock, Mock, patch

import pytest

from custom_components.kamstrup_403.pykamstrup.kamstrup import Kamstrup


@patch("serial.serial_for_url")
def test_init(mock_serial: Mock) -> None:
    """Test initialization."""
    mock_serial_instance = MagicMock()
    mock_serial.return_value = mock_serial_instance

    kamstrup = Kamstrup("test_url", 9600, 1.0)

    mock_serial.assert_called_once_with(url="test_url", baudrate=9600, timeout=1.0)
    assert kamstrup.ser == mock_serial_instance


def test_crc_1021() -> None:
    """Test CRC calculation."""
    # Test with empty message
    assert Kamstrup._crc_1021(()) == 0x0000  # pylint: disable=protected-access

    # Test with known values - use actual calculated values
    message = (0x3F, 0x10, 0x01, 0x00, 0x3C)
    actual_crc = Kamstrup._crc_1021(message)  # pylint: disable=protected-access
    assert actual_crc == 64250  # This is the actual CRC for this message

    # Test with single byte - use actual calculated value
    assert Kamstrup._crc_1021((0xFF,)) == 255  # pylint: disable=protected-access


def test_debug(caplog: pytest.LogCaptureFixture) -> None:
    """Test debug logging."""
    with patch("serial.serial_for_url"):
        kamstrup = Kamstrup("test_url", 9600, 1.0)

    with caplog.at_level("DEBUG"):
        kamstrup._debug("Test message", bytearray([0x01, 0x02, 0xFF]))  # pylint: disable=protected-access

    assert "Test message: 01 02 ff" in caplog.text


@patch("serial.serial_for_url")
def test_make_sure_port_is_opened_already_open(mock_serial: Mock) -> None:
    """Test port opening when already open."""
    mock_serial_instance = MagicMock()
    mock_serial_instance.is_open = True
    mock_serial.return_value = mock_serial_instance

    kamstrup = Kamstrup("test_url", 9600, 1.0)
    kamstrup._make_sure_port_is_opened()  # pylint: disable=protected-access

    mock_serial_instance.open.assert_not_called()


@patch("serial.serial_for_url")
def test_make_sure_port_is_opened_closed(mock_serial: Mock) -> None:
    """Test port opening when closed."""
    mock_serial_instance = MagicMock()
    mock_serial_instance.is_open = False
    mock_serial.return_value = mock_serial_instance

    kamstrup = Kamstrup("test_url", 9600, 1.0)
    kamstrup._make_sure_port_is_opened()  # pylint: disable=protected-access

    mock_serial_instance.open.assert_called_once()


@patch("serial.serial_for_url")
def test_write(mock_serial: Mock) -> None:
    """Test writing data."""
    mock_serial_instance = MagicMock()
    mock_serial_instance.is_open = True
    mock_serial.return_value = mock_serial_instance

    kamstrup = Kamstrup("test_url", 9600, 1.0)
    test_data = (0x01, 0x02, 0x03)

    kamstrup._write(test_data)  # pylint: disable=protected-access

    mock_serial_instance.write.assert_called_once_with(bytearray([0x01, 0x02, 0x03]))


@patch("serial.serial_for_url")
def test_read_success(mock_serial: Mock) -> None:
    """Test successful read."""
    mock_serial_instance = MagicMock()
    mock_serial_instance.is_open = True
    mock_serial_instance.read.return_value = b"\x42"
    mock_serial.return_value = mock_serial_instance

    kamstrup = Kamstrup("test_url", 9600, 1.0)
    result = kamstrup._read()  # pylint: disable=protected-access

    assert result == 0x42
    mock_serial_instance.read.assert_called_once_with(1)


@patch("serial.serial_for_url")
def test_read_timeout(mock_serial: Mock, caplog: pytest.LogCaptureFixture) -> None:
    """Test read timeout."""
    mock_serial_instance = MagicMock()
    mock_serial_instance.is_open = True
    mock_serial_instance.read.return_value = b""
    mock_serial.return_value = mock_serial_instance

    kamstrup = Kamstrup("test_url", 9600, 1.0)

    with caplog.at_level("DEBUG"):
        result = kamstrup._read()  # pylint: disable=protected-access

    assert result is None
    assert "Rx Timeout" in caplog.text


@patch("serial.serial_for_url")
def test_send_without_escapes(mock_serial: Mock) -> None:
    """Test sending data without escape characters."""
    mock_serial_instance = MagicMock()
    mock_serial_instance.is_open = True
    mock_serial.return_value = mock_serial_instance

    kamstrup = Kamstrup("test_url", 9600, 1.0)
    message = (0x3F, 0x10, 0x01)

    kamstrup._send(0x80, message)  # pylint: disable=protected-access

    # Verify the call was made (exact bytes depend on CRC calculation)
    mock_serial_instance.write.assert_called_once()
    written_data = mock_serial_instance.write.call_args[0][0]

    # Should start with prefix and end with 0x0D
    assert written_data[0] == 0x80
    assert written_data[-1] == 0x0D


@patch("serial.serial_for_url")
def test_send_with_escapes(mock_serial: Mock) -> None:
    """Test sending data with escape characters."""
    mock_serial_instance = MagicMock()
    mock_serial_instance.is_open = True
    mock_serial.return_value = mock_serial_instance

    kamstrup = Kamstrup("test_url", 9600, 1.0)
    # Use a message that will contain escape characters after CRC
    message = (0x40, 0x1B, 0x06)  # All escape characters

    kamstrup._send(0x80, message)  # pylint: disable=protected-access

    mock_serial_instance.write.assert_called_once()
    written_data = mock_serial_instance.write.call_args[0][0]

    # Should contain escape sequences
    assert 0x1B in written_data  # Escape byte should be present


@patch("serial.serial_for_url")
def test_receive_success(mock_serial: Mock) -> None:
    """Test successful receive."""
    mock_serial_instance = MagicMock()
    mock_serial_instance.is_open = True

    # Create valid response data with correct CRC
    message_data = bytearray([0x3F, 0x10, 0x00, 0x3C, 0x00])
    crc = Kamstrup._crc_1021(tuple(message_data))  # pylint: disable=protected-access
    message_data[-2] = crc >> 8
    message_data[-1] = crc & 0xFF

    response_data = [64, *list(message_data), 13]
    mock_serial_instance.read.side_effect = [bytes([b]) for b in response_data]
    mock_serial.return_value = mock_serial_instance

    kamstrup = Kamstrup("test_url", 9600, 1.0)
    result = kamstrup._receive()  # pylint: disable=protected-access

    # Should return data without start, end, and CRC bytes
    assert result is not None
    assert len(result) == 3  # Original data without CRC (0x3F, 0x10, 0x00)


@patch("serial.serial_for_url")
def test_receive_timeout(mock_serial: Mock) -> None:
    """Test receive timeout."""
    mock_serial_instance = MagicMock()
    mock_serial_instance.is_open = True
    mock_serial_instance.read.return_value = b""
    mock_serial.return_value = mock_serial_instance

    kamstrup = Kamstrup("test_url", 9600, 1.0)
    result = kamstrup._receive()  # pylint: disable=protected-access

    assert result is None


@patch("serial.serial_for_url")
def test_receive_with_escape_sequences(mock_serial: Mock) -> None:
    """Test receive with escape sequences."""
    mock_serial_instance = MagicMock()
    mock_serial_instance.is_open = True

    # Create valid message with escape character that needs escaping
    message_data = bytearray([0x40, 0x10, 0x00])  # 0x40 needs to be escaped
    crc = Kamstrup._crc_1021(tuple(message_data))  # pylint: disable=protected-access
    message_data[-2:] = [crc >> 8, crc & 0xFF]

    # Simulate response with escape sequences: 0x40 gets escaped as 0x1B 0xBF
    response_data = [0x40, 0x1B, 0xBF, 0x10, 0x00, crc >> 8, crc & 0xFF, 0x0D]
    mock_serial_instance.read.side_effect = [bytes([b]) for b in response_data]
    mock_serial.return_value = mock_serial_instance

    kamstrup = Kamstrup("test_url", 9600, 1.0)
    result = kamstrup._receive()  # pylint: disable=protected-access

    assert result is not None
    # Should contain unescaped 0x40
    assert 0x40 in result


@patch("serial.serial_for_url")
def test_receive_invalid_escape(mock_serial: Mock, caplog: pytest.LogCaptureFixture) -> None:
    """Test receive with invalid escape sequence."""
    mock_serial_instance = MagicMock()
    mock_serial_instance.is_open = True

    # Invalid escape: 0x1B followed by byte that's not in ESCAPES when XORed
    response_data = [0x40, 0x1B, 0x12, 0x0D]  # 0x12 ^ 0xFF = 0xED (not in ESCAPES)
    mock_serial_instance.read.side_effect = [bytes([b]) for b in response_data]
    mock_serial.return_value = mock_serial_instance

    kamstrup = Kamstrup("test_url", 9600, 1.0)

    with caplog.at_level("DEBUG"):
        kamstrup._receive()  # pylint: disable=protected-access

    assert "Missing Escape" in caplog.text


@patch("serial.serial_for_url")
def test_receive_crc_error(mock_serial: Mock, caplog: pytest.LogCaptureFixture) -> None:
    """Test receive with CRC error."""
    mock_serial_instance = MagicMock()
    mock_serial_instance.is_open = True

    # Invalid CRC
    response_data = [0x40, 0x3F, 0x10, 0xFF, 0xFF, 0x0D]  # Wrong CRC
    mock_serial_instance.read.side_effect = [bytes([b]) for b in response_data]
    mock_serial.return_value = mock_serial_instance

    kamstrup = Kamstrup("test_url", 9600, 1.0)

    with caplog.at_level("DEBUG"):
        kamstrup._receive()  # pylint: disable=protected-access

    assert "CRC error" in caplog.text


def test_process_response_success() -> None:
    """Test successful response processing."""
    nbr = 0x003C  # 60
    # Response format: nbr_high, nbr_low, unit, length, exp, value_bytes...
    data = bytearray([0x00, 0x3C, 0x08, 0x02, 0x00, 0x12, 0x34])  # GJ unit, 2 bytes value

    value, unit = Kamstrup._process_response(nbr, data)  # pylint: disable=protected-access

    assert value == 0x1234  # 4660
    assert unit == "GJ"


def test_process_response_nbr_error(caplog: pytest.LogCaptureFixture) -> None:
    """Test response processing with NBR error."""
    nbr = 0x003C
    # Wrong NBR in response
    data = bytearray([0x00, 0x3D, 0x08, 0x02, 0x00, 0x12, 0x34])

    with caplog.at_level("DEBUG"):
        value, unit = Kamstrup._process_response(nbr, data)  # pylint: disable=protected-access

    assert value is None
    assert unit is None
    assert "NBR error" in caplog.text


def test_process_response_unknown_unit() -> None:
    """Test response processing with unknown unit."""
    nbr = 0x003C
    data = bytearray([0x00, 0x3C, 0xFF, 0x01, 0x00, 0x42])  # Unknown unit 0xFF

    value, unit = Kamstrup._process_response(nbr, data)  # pylint: disable=protected-access

    assert value == 0x42
    assert unit is None


def test_process_response_negative_exponent() -> None:
    """Test response processing with negative exponent."""
    nbr = 0x003C
    # Exponent with bit 6 set (negative)
    data = bytearray([0x00, 0x3C, 0x08, 0x02, 0x42, 0x12, 0x34])  # exp = -2

    value, unit = Kamstrup._process_response(nbr, data)  # pylint: disable=protected-access
    assert value

    expected = 0x1234 * math.pow(10, -2)  # 46.6
    assert abs(value - expected) < 0.001
    assert unit == "GJ"


def test_process_response_negative_value() -> None:
    """Test response processing with negative value (bit 7 set)."""
    nbr = 0x003C
    # Exponent with bit 7 set (negative value)
    data = bytearray([0x00, 0x3C, 0x08, 0x02, 0x80, 0x12, 0x34])

    value, unit = Kamstrup._process_response(nbr, data)  # pylint: disable=protected-access
    assert value

    assert value < 0
    assert unit == "GJ"


def test_process_response_multi_byte_value() -> None:
    """Test response processing with multi-byte value."""
    nbr = 0x003C
    # 4-byte value
    data = bytearray([0x00, 0x3C, 0x08, 0x04, 0x00, 0x12, 0x34, 0x56, 0x78])

    value, unit = Kamstrup._process_response(nbr, data)  # pylint: disable=protected-access

    expected = 0x12345678
    assert value == expected
    assert unit == "GJ"


@patch("serial.serial_for_url")
def test_get_value_success(mock_serial: Mock) -> None:
    """Test successful get_value."""
    mock_serial_instance = MagicMock()
    mock_serial_instance.is_open = True
    mock_serial.return_value = mock_serial_instance

    kamstrup = Kamstrup("test_url", 9600, 1.0)

    # Mock the receive method to return valid data
    with patch.object(kamstrup, "_receive") as mock_receive:
        mock_receive.return_value = bytearray([0x3F, 0x10, 0x00, 0x3C, 0x08, 0x02, 0x00, 0x12, 0x34])

        value, unit = kamstrup.get_value(60)

    assert value == 0x1234
    assert unit == "GJ"


@patch("serial.serial_for_url")
def test_get_value_no_response(mock_serial: Mock) -> None:
    """Test get_value with no response."""
    mock_serial_instance = MagicMock()
    mock_serial_instance.is_open = True
    mock_serial.return_value = mock_serial_instance

    kamstrup = Kamstrup("test_url", 9600, 1.0)

    with patch.object(kamstrup, "_receive") as mock_receive:
        mock_receive.return_value = None

        value, unit = kamstrup.get_value(60)

    assert value is None
    assert unit is None


@patch("serial.serial_for_url")
def test_get_value_wrong_address_or_cid(mock_serial: Mock) -> None:
    """Test get_value with wrong destination address or CID."""
    mock_serial_instance = MagicMock()
    mock_serial_instance.is_open = True
    mock_serial.return_value = mock_serial_instance

    kamstrup = Kamstrup("test_url", 9600, 1.0)

    with patch.object(kamstrup, "_receive") as mock_receive:
        # Wrong destination address (should be 0x3F)
        mock_receive.return_value = bytearray([0x40, 0x10, 0x00, 0x3C, 0x08, 0x02, 0x00, 0x12, 0x34])

        value, unit = kamstrup.get_value(60)

    assert value is None
    assert unit is None


@patch("serial.serial_for_url")
def test_get_values_success(mock_serial: Mock) -> None:
    """Test successful get_values."""
    mock_serial_instance = MagicMock()
    mock_serial_instance.is_open = True
    mock_serial.return_value = mock_serial_instance

    kamstrup = Kamstrup("test_url", 9600, 1.0)

    with patch.object(kamstrup, "_receive") as mock_receive:
        # Response with two values
        response_data = bytearray(
            [
                0x3F,
                0x10,  # dest_addr, cid
                0x00,
                0x3C,
                0x08,
                0x02,
                0x00,
                0x12,
                0x34,  # First value (60)
                0x00,
                0x8C,
                0x30,
                0x03,
                0x00,
                0x23,
                0x01,
                0x23,  # Second value (140)
            ]
        )
        mock_receive.return_value = response_data

        result = kamstrup.get_values([60, 140])

    assert result is not None
    assert len(result) == 2
    assert result[60][0] == 0x1234
    assert result[60][1] == "GJ"
    assert result[140][0] == 0x230123
    assert result[140][1] == "yy:mm:dd"


@patch("serial.serial_for_url")
def test_get_values_too_many_values(mock_serial: Mock, caplog: pytest.LogCaptureFixture) -> None:
    """Test get_values with too many values."""
    mock_serial_instance = MagicMock()
    mock_serial_instance.is_open = True
    mock_serial.return_value = mock_serial_instance

    kamstrup = Kamstrup("test_url", 9600, 1.0)

    # Request more than MULTIPLE_NBR_MAX (8) values
    many_values = list(range(1, 12))  # 11 values

    with patch.object(kamstrup, "_receive") as mock_receive:
        # Create proper response for first 8 values
        response_data = bytearray([0x3F, 0x10])  # dest_addr, cid
        for i in range(8):  # Add 8 minimal response entries
            response_data.extend([0x00, 0x01 + i, 0x08, 0x01, 0x00, 0x42])  # nbr, unit, len, exp, value
        mock_receive.return_value = response_data

        with caplog.at_level("WARNING"):
            result = kamstrup.get_values(many_values)

    assert "Can only get" in caplog.text
    assert "values at once" in caplog.text
    assert result is not None  # Should still return data for first 8 values


@patch("serial.serial_for_url")
def test_get_values_no_response(mock_serial: Mock) -> None:
    """Test get_values with no response."""
    mock_serial_instance = MagicMock()
    mock_serial_instance.is_open = True
    mock_serial.return_value = mock_serial_instance

    kamstrup = Kamstrup("test_url", 9600, 1.0)

    with patch.object(kamstrup, "_receive") as mock_receive:
        mock_receive.return_value = None

        result = kamstrup.get_values([60])

    assert result is None


@patch("serial.serial_for_url")
def test_get_values_wrong_address_or_cid(mock_serial: Mock) -> None:
    """Test get_values with wrong destination address or CID."""
    mock_serial_instance = MagicMock()
    mock_serial_instance.is_open = True
    mock_serial.return_value = mock_serial_instance

    kamstrup = Kamstrup("test_url", 9600, 1.0)

    with patch.object(kamstrup, "_receive") as mock_receive:
        # Wrong CID (should be 0x10)
        mock_receive.return_value = bytearray([0x3F, 0x11])

        result = kamstrup.get_values([60])

    assert result is None
