"""
scale.py

Description: [DESCRIPTION]

Created on Apr 25, 2017

Data Format: Every message includes 6 bytes;
    a. No. 1: D0-D7 = 0FFH (Message Flag)
    b. No. 2: D0-D2 = Decimal point (0-5)
        D3-D4 = Current mode: 00-Weight; 01-Count; 10-Percent
        D5 = 1 means weight is negative, otherwise positive
        D6 = 1 means weight is stable, otherwise unstable
        D7 = 1 means weight is overflow, otherwise normal
    c. No. 3: D0-D7 = BCD1 (LSB)
    d. No. 4: D0-D7 = BCD2 (MSB)
    e. No. 5: D0-D7 = BCD3 (HSB)


Bytes 3-5 to Digits
D2: 0001 D1: 0000
D4: 0000 D3: 0000
D6: 0000 D5: 0000
"""

import serial
import collections

Reading = collections.namedtuple(
    'Reading', ['mode', 'stable', 'overflow', 'weight', 'units'])

Previous_Reading = 0  # store the last reading of the scale
Count_Stable = 0  # how many times have the scale values been stable


class Scale:
    @staticmethod
    def decode(raw: bytes) -> Reading:
        # Handle first byte
        if len(raw) != 6 or raw[0] != 0xff:
            raise ValueError('Not a Global 240878 message')
        # Handle second byte
        decimal_point = raw[1] & 0b111
        current_mode = (raw[1] & 0b11000) >> 3
        negative = (raw[1] & 0b100000) >> 5
        stable = (raw[1] & 0b1000000) >> 6
        overflow = (raw[1] & 0b10000000) >> 7
        # TODO: Handle third byte
        digit1 = raw[2] & 0b1111
        digit2 = (raw[2] & 0b11110000) >> 4
        # TODO: Handle fourth byte
        digit3 = raw[3] & 0b1111
        digit4 = (raw[3] & 0b11110000) >> 4
        # TODO: Handle fifth byte
        digit5 = raw[4] & 0b1111
        digit6 = (raw[4] & 0b11110000) >> 4
        # Put it all together
        result = digit1 + (digit2 * 10) + (digit3 * 100) + \
            (digit4 * 1000) + (digit5 * 10000) + (digit6 * 100000)
        result /= 10 ** (decimal_point - 1)
        # Handle sixth byte
        unit = raw[5] & 0b1
        return result

    def __init__(self) -> None:
        self.ser = serial.Serial('/dev/ttyUSB0')
        self.last_value = None

    def check(self) -> bool:
        self.last_value = Scale.decode(self.ser.read(6))
        if self.last_value.stable:
            return True  # Reading stored in scale.last_value
        return False  # Reading still unstable

    def check(self) -> Reading:  # check if the scale is having a stable value
        val = Scale.decode(self.ser.read(6))
        if abs(val - Previous_Reading) > 0.3:
            Count_Stable = 0
        else:
            ++Count_Stable
        Previous_Reading = val
        if Count_Stable > 5:
            return True  # scale is stable
        else:
            return False  # scale not stable

    def close(self) -> None:
        self.ser.close()


if __name__ == '__main__':
    # Test the examples from Khoi's screenshot
    # from binascii import unhexlify
    # print(decode(unhexlify('ff4487150000')))
    # print(decode(unhexlify('ff4406180000')))
    # print(decode(unhexlify('ff4910000000')))
    # print(decode(unhexlify('ff4407180000')))
    s = Scale()
    s.check()
