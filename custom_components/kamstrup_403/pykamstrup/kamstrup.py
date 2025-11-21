"""Kamstrup Meter Protocol (KMP)."""

# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <phk@FreeBSD.ORG> wrote this file.  As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return.   Poul-Henning Kamp
# ----------------------------------------------------------------------------

import asyncio
import logging
import math

import serial_asyncio_fast as serial_asyncio

from .const import ESCAPES, UNITS

_LOGGER: logging.Logger = logging.getLogger(__package__)
MULTIPLE_NBR_MAX: int = 8


class Kamstrup:
    """Kamstrup Meter Protocol (KMP)."""

    reader: asyncio.StreamReader | None
    writer: asyncio.StreamWriter | None

    def __init__(self, url: str, baudrate: int, timeout: float) -> None:
        """Initialize."""
        self.url = url
        self.baudrate = baudrate
        self.timeout = timeout
        self.reader = None
        self.writer = None

    async def connect(self) -> None:
        """Connect to the serial device."""
        if self.reader is None or self.writer is None:
            self.reader, self.writer = await serial_asyncio.open_serial_connection(url=self.url, baudrate=self.baudrate)

    async def disconnect(self) -> None:
        """Disconnect from the serial device."""
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
            self.reader = None
            self.writer = None

    @classmethod
    def _crc_1021(cls, message: tuple[int, ...]) -> int:
        """Kamstrup uses the "true" CCITT CRC-16."""
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

    def _debug(self, msg: str, byte_array: bytearray) -> None:
        """Log a debug message with a byte array."""
        log = f"{msg}:"
        for byte in byte_array:
            log += f" {byte:02x}"
        _LOGGER.debug(log)

    async def _ensure_connected(self) -> None:
        """Make sure the connection is established."""
        if self.reader is None or self.writer is None:
            await self.connect()

    async def _write(self, data: tuple[int, ...]) -> None:
        """Write directly to the meter."""
        await self._ensure_connected()
        if self.writer is None:
            msg = "Writer not available"
            raise RuntimeError(msg)
        bytearray_data = bytearray(data)
        self._debug("Write", bytearray_data)
        self.writer.write(bytearray_data)
        await self.writer.drain()

    async def _read(self) -> int | None:
        """Read directly from the meter."""
        await self._ensure_connected()
        if self.reader is None:
            msg = "Reader not available"
            raise RuntimeError(msg)
        try:
            data = await asyncio.wait_for(self.reader.read(1), timeout=self.timeout)
            if len(data) == 0:
                _LOGGER.debug("Rx Timeout")
                return None
            bytearray_data = bytearray(data)
            self._debug("Read", bytearray(bytearray_data))
            return bytearray_data[0]
        except TimeoutError:
            _LOGGER.debug("Rx Timeout")
            return None

    async def _send(self, pfx: int, message: tuple[int, ...]) -> None:
        """Construct the message and send to the meter."""
        bytearray_data = bytearray(message)
        bytearray_data.append(0)
        bytearray_data.append(0)
        crc = self._crc_1021(tuple(bytearray_data))
        bytearray_data[-2] = crc >> 8
        bytearray_data[-1] = crc & 0xFF

        send_data = [pfx]
        for i in bytearray_data:
            if i in ESCAPES:
                send_data.append(0x1B)
                send_data.append(i ^ 0xFF)
            else:
                send_data.append(i)
        send_data.append(0x0D)
        await self._write(tuple(send_data))

    async def _receive(self) -> bytearray | None:
        """Receive data."""
        # Skip first response, which is repetition of initial command,
        # only break on 0x0d if it comes after 0x40.
        bytearray_data = None
        resp_start = 0x40
        resp_end = 0x0D
        while True:
            data = await self._read()
            if data is None:
                return None
            if data == resp_start:
                bytearray_data = bytearray()
            if bytearray_data is not None:
                bytearray_data.append(data)
                if data == resp_end:
                    break

        escape_byte = 0x1B
        response_data = bytearray()
        i = 1
        while i < len(bytearray_data) - 1:
            if bytearray_data[i] == escape_byte:
                value = bytearray_data[i + 1] ^ 0xFF
                if value not in ESCAPES:
                    _LOGGER.debug("Missing Escape %02x", value)
                response_data.append(value)
                i += 2
            else:
                response_data.append(bytearray_data[i])
                i += 1
        if self._crc_1021(tuple(response_data)):
            _LOGGER.debug("CRC error")
        return response_data[:-2]

    @classmethod
    def _process_response(cls, nbr: int, data: bytearray) -> tuple[float | None, str | None]:
        """Process a response."""
        if data[0] != nbr >> 8 or data[1] != nbr & 0xFF:
            _LOGGER.debug("NBR error")
            return (None, None)

        unit = UNITS.get(data[2], None)

        # Decode the mantissa.
        value: float = 0.0
        for i in range(data[3]):
            value = (value * 256) + data[i + 5]

        # Decode the exponent.
        exp_val = data[4] & 0x3F
        if data[4] & 0x40:
            exp_val = -exp_val
        exp = math.pow(10, exp_val)
        if data[4] & 0x80:
            exp = -exp
        value *= exp

        return value, unit

    async def get_value(self, nbr: int) -> tuple[None, None] | tuple[float | None, str | None]:
        """Get a value from the meter."""
        await self._send(0x80, (0x3F, 0x10, 0x01, nbr >> 8, nbr & 0xFF))

        bytearray_data = await self._receive()
        if bytearray_data is None:
            return (None, None)

        dest_addr = 0x3F
        cid = 0x10
        if bytearray_data[0] != dest_addr or bytearray_data[1] != cid:
            return (None, None)

        value, unit = self._process_response(nbr, bytearray_data[2:])

        return (value, unit)

    async def get_values(self, multiple_nbr: list[int]) -> dict[int, tuple[float | None, str | None]] | None:
        """Get values from the meter."""
        if len(multiple_nbr) > MULTIPLE_NBR_MAX:
            multiple_nbr = multiple_nbr[:MULTIPLE_NBR_MAX]
            _LOGGER.warning(
                "Can only get %i values at once, will only update %s",
                MULTIPLE_NBR_MAX,
                multiple_nbr,
            )

        # Construct the request.
        dest_addr = 0x3F
        cid = 0x10
        req = [dest_addr, cid, len(multiple_nbr)]
        for nbr in multiple_nbr:
            req.append(nbr >> 8)
            req.append(nbr & 0xFF)
        await self._send(0x80, tuple(req))

        # Process response.
        bytearray_data = await self._receive()
        if bytearray_data is None:
            return None

        # Check destination address and CID.
        if bytearray_data[0] != dest_addr or bytearray_data[1] != cid:
            return None

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
