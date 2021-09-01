#!/usr/bin/python
#
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <phk@FreeBSD.ORG> wrote this file.  As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return.   Poul-Henning Kamp
# ----------------------------------------------------------------------------
#
# Modified for Domotics and single request.
#
# Modified by Frank Reijn and Paul Bonnemaijers for Kamstrup Multical 402
#
# Modified by Sander Gols to integrate in HA component

from __future__ import print_function

import serial
import math

#######################################################################
# Units, provided by Erik Jensen

units = {
    0: "",
    1: "Wh",
    2: "kWh",
    3: "MWh",
    4: "GWh",
    5: "J",
    6: "kj",
    7: "MJ",
    8: "GJ",
    9: "Cal",
    10: "kCal",
    11: "Mcal",
    12: "Gcal",
    13: "varh",
    14: "kvarh",
    15: "Mvarh",
    16: "Gvarh",
    17: "VAh",
    18: "kVAh",
    19: "MVAh",
    20: "GVAh",
    21: "kW",
    22: "kW",
    23: "MW",
    24: "GW",
    25: "kvar",
    26: "kvar",
    27: "Mvar",
    28: "Gvar",
    29: "VA",
    30: "kVA",
    31: "MVA",
    32: "GVA",
    33: "V",
    34: "A",
    35: "kV",
    36: "kA",
    37: "°C",
    38: "K",
    39: "l",
    40: "m3",
    41: "l/h",
    42: "m3/h",
    43: "m3xC",
    44: "ton",
    45: "ton/h",
    46: "h",
    47: "hh:mm:ss",
    48: "yy:mm:dd",
    49: "yyyy:mm:dd",
    50: "mm:dd",
    51: "",
    52: "bar",
    53: "RTC",
    54: "ASCII",
    55: "m3 x 10",
    56: "ton x 10",
    57: "GJ x 10",
    58: "minutes",
    59: "Bitfield",
    60: "s",
    61: "ms",
    62: "days",
    63: "RTC-Q",
    64: "Datetime",
}

#######################################################################
# Kamstrup uses the "true" CCITT CRC-16
#


def crc_1021(message):
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


#######################################################################
# Byte values which must be escaped before transmission
#

escapes = {
    0x06: True,
    0x0D: True,
    0x1B: True,
    0x40: True,
    0x80: True,
}

#######################################################################
# And here we go....
#


class Kamstrup(object):
    def __init__(self, serial_port, baudrate, timeout):

        self.ser = serial.Serial(port=serial_port, baudrate=baudrate, timeout=timeout)

    def wr(self, b):
        b = bytearray(b)
        self.ser.write(b)

    def rd(self):
        a = self.ser.read(1)
        if len(a) == 0:
            return None
        b = bytearray(a)[0]
        return b

    def send(self, pfx, msg):
        b = bytearray(msg)

        b.append(0)
        b.append(0)
        c = crc_1021(b)
        b[-2] = c >> 8
        b[-1] = c & 0xFF

        c = bytearray()
        c.append(pfx)
        for i in b:
            if i in escapes:
                c.append(0x1B)
                c.append(i ^ 0xFF)
            else:
                c.append(i)
        c.append(0x0D)
        self.wr(c)

    def recv(self):
        b = bytearray()
        while True:
            d = self.rd()
            if d == None:
                return None
            if d == 0x40:
                b = bytearray()
            b.append(d)
            if d == 0x0D:
                break
        c = bytearray()
        i = 1
        while i < len(b) - 1:
            if b[i] == 0x1B:
                v = b[i + 1] ^ 0xFF
                c.append(v)
                i += 2
            else:
                c.append(b[i])
                i += 1
        return c[:-2]

    def readvar(self, nbr):
        # I wouldn't be surprised if you can ask for more than
        # one variable at the time, given that the length is
        # encoded in the response.  Havn't tried.

        self.send(0x80, (0x3F, 0x10, 0x01, nbr >> 8, nbr & 0xFF))

        b = self.recv()
        if b == None:
            return (None, None)

        if b[0] != 0x3F or b[1] != 0x10:
            return (None, None)

        if b[2] != nbr >> 8 or b[3] != nbr & 0xFF:
            return (None, None)

        if b[4] in units:
            u = units[b[4]]
        else:
            u = None

        # Decode the mantissa
        x = 0
        for i in range(0, b[5]):
            x <<= 8
            x |= b[i + 7]

        # Decode the exponent
        i = b[6] & 0x3F
        if b[6] & 0x40:
            i = -i
        i = math.pow(10, i)
        if b[6] & 0x80:
            i = -i
        x *= i

        return (x, u)
