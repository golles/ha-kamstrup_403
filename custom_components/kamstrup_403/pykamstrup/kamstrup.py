"""Kamstrup Meter Protocol (KMP)"""

# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <phk@FreeBSD.ORG> wrote this file.  As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return.   Poul-Henning Kamp
# ----------------------------------------------------------------------------

import logging
import math

import serial

from .const import ESCAPES, UNITS

_LOGGER: logging.Logger = logging.getLogger(__package__)
MULTIPLE_NBR_MAX: int = 8


class Kamstrup:
    """Kamstrup Meter Protocol (KMP)"""

    def __init__(self, url: str, baudrate: int, timeout: float):
        """Initialize"""
        self._url = url
        self._baudrate = baudrate
        self._timeout = timeout
        self.ser = serial.serial_for_url(url=self._url, baudrate=self._baudrate, timeout=self._timeout)

    @classmethod
    def _crc_1021(cls, message: tuple[int]) -> int:
        """Kamstrup uses the "true" CCITT CRC-16"""
        poly = 0x1021
        reg = 0x0000
        for byte in message:
            mask = 0x80
            while mask > 0:
                reg <<= 1
                if byte & mask:
                    reg |= 1
                mask >>= 1
                if reg & 0x10000:
                    reg &= 0xFFFF
                    reg ^= poly
        return reg

    def _debug(self, msg: str, byte_array: bytearray):
        log = f"{msg}:"
        for byte in byte_array:
            log += f" {byte:02x}"
        _LOGGER.debug(log)

    def _make_sure_port_is_opened(self):
        if not self.ser.is_open:
            self.ser.open()

    def _write(self, data: tuple[int]):
        """Write directly to the meter"""
        self._make_sure_port_is_opened()
        bytearray_data = bytearray(data)
        try:
            self._debug("Write", bytearray_data)
            self.ser.write(bytearray_data)
        except serial.SerialException:
            self.ser = serial.serial_for_url(url=self._url, baudrate=self._baudrate, timeout=self._timeout)

    def _read(self) -> int | None:
        """Read directly from the meter"""
        self._make_sure_port_is_opened()
        data = self.ser.read(1)
        if len(data) == 0:
            _LOGGER.debug("Rx Timeout")
            return None
        bytearray_data = bytearray(data)
        self._debug("Read", bytearray(bytearray_data))
        return bytearray_data[0]

    def _send(self, pfx: int, message: tuple[int]):
        """Construct the message and send to the meter"""
        bytearray_data = bytearray(message)

        bytearray_data.append(0)
        bytearray_data.append(0)
        data = self._crc_1021(bytearray_data)
        bytearray_data[-2] = data >> 8
        bytearray_data[-1] = data & 0xFF

        data = bytearray()
        data.append(pfx)
        for i in bytearray_data:
            if i in ESCAPES:
                data.append(0x1B)
                data.append(i ^ 0xFF)
            else:
                data.append(i)
        data.append(0x0D)
        self._write(data)

    def _receive(self) -> bytearray | None:
        """Receive data"""
        # Skip first response, which is repetition of initial command,
        # only break on 0x0d if it comes after 0x40.
        bytearray_data = None
        while True:
            data = self._read()
            if data is None:
                self.ser = serial.serial_for_url(url=self._url, baudrate=self._baudrate, timeout=self._timeout)
                return None
            if data == 0x40:
                bytearray_data = bytearray()
            if bytearray_data is not None:
                bytearray_data.append(data)
                if data == 0x0D:
                    break

        response_data = bytearray()
        i = 1
        while i < len(bytearray_data) - 1:
            if bytearray_data[i] == 0x1B:
                value = bytearray_data[i + 1] ^ 0xFF
                if value not in ESCAPES:
                    _LOGGER.debug("Missing Escape %02x", value)
                response_data.append(value)
                i += 2
            else:
                response_data.append(bytearray_data[i])
                i += 1
        if self._crc_1021(response_data):
            _LOGGER.debug("CRC error")
        return response_data[:-2]

    @classmethod
    def _process_response(cls, nbr: int, data):
        """Process a response"""
        if data[0] != nbr >> 8 or data[1] != nbr & 0xFF:
            _LOGGER.debug("NBR error")
            return (None, None)

        if data[2] in UNITS:
            unit = UNITS[data[2]]
        else:
            unit = None

        # Decode the mantissa.
        value = 0
        for i in range(0, data[3]):
            value <<= 8
            value |= data[i + 5]

        # Decode the exponent.
        i = data[4] & 0x3F
        if data[4] & 0x40:
            i = -i
        i = math.pow(10, i)
        if data[4] & 0x80:
            i = -i
        value *= i

        return value, unit

    def get_value(
        self, nbr: int
    ) -> tuple[None, None] | tuple[float | None, str | None]:
        """Get a value from the meter"""
        self._send(0x80, (0x3F, 0x10, 0x01, nbr >> 8, nbr & 0xFF))

        bytearray_data = self._receive()
        if bytearray_data is None:
            return (None, None)

        if bytearray_data[0] != 0x3F or bytearray_data[1] != 0x10:
            return (None, None)

        value, unit = self._process_response(nbr, bytearray_data[2:])

        return (value, unit)

    def get_values(
        self, multiple_nbr: list[int]
    ) -> tuple[None, None] | tuple[float | None, str | None] | dict:
        """Get values from the meter"""

        if len(multiple_nbr) > MULTIPLE_NBR_MAX:
            multiple_nbr = multiple_nbr[:MULTIPLE_NBR_MAX]
            _LOGGER.warning(
                "Can only get %i values at once, will only update %s",
                MULTIPLE_NBR_MAX,
                multiple_nbr,
            )

        # Construct the request.
        req = bytearray()
        req.append(0x3F)  # destination address.
        req.append(0x10)  # CID.
        req.append(len(multiple_nbr))  # number of nbrs.
        for nbr in multiple_nbr:
            req.append(nbr >> 8)
            req.append(nbr & 0xFF)

        self._send(0x80, req)

        # Process response.
        bytearray_data = self._receive()
        if bytearray_data is None:
            return (None, None)

        # Check destination address and CID.
        if bytearray_data[0] != 0x3F or bytearray_data[1] != 0x10:
            return (None, None)

        # Decode response data, containing multiple variables.
        result = {}
        remaining_data = bytearray_data[2:]
        counter = 0

        # Continue processing data until all variables have been processed.
        while counter < (len(multiple_nbr)):
            current_nbr = multiple_nbr[counter]
            value, unit = self._process_response(current_nbr, remaining_data)
            result[current_nbr] = (value, unit)
            # length of current variable response data =
            # nbr (2) + units (1) + length (1) + sigexp (1) (=5)
            # + length of actual value.
            len_current_nbr = 5 + remaining_data[3]
            remaining_data = remaining_data[len_current_nbr:]
            counter += 1

        return result
