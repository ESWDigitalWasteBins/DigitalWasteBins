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
from stopwatch import Stopwatch

sw = Stopwatch()

Reading = collections.namedtuple(
    'Reading', ['mode', 'stable', 'overflow', 'weight', 'units'])


class Scale:
    def __init__(self) -> None:
        self.ser = serial.Serial('/dev/ttyUSB0', 9600)
        #scale supports 1200, 2400, 4800, 9600
        if (self.ser.isOpen()):
            self.close()
        self.open()
        self.last_value = 0
        self.stable = 0

    def decode(self, raw: bytes) -> Reading:
        sw.reset()
        sw.start()
        # Handle first byte
        if len(raw) != 6 or raw[0] != 0xff:
            sw.stop()
            print("TIME (decode fail): ", sw.read())
            return -1
            # raise ValueError('Not a Global 240878 message')
        # Handle second byte
        decimal_point = raw[1] & 0b111
        current_mode = (raw[1] & 0b11000) >> 3
        negative = (raw[1] & 0b100000) >> 5
        self.stable = (raw[1] & 0b1000000) >> 6
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
        sw.stop()
        print("TIME (decode): ", sw.read())
        return result

    def check(self):
        sw.reset()
        sw.start()

        if self.ser.in_waiting > 0:
            reading = self.ser.read(6)
            sw.stop()
            print("TIME (scale reading): ", sw.read())
            sw.start()
            a = Scale.decode(self, reading)
            #will record the last stable value and compare it to the next one
            #run the scale in STB mode 
            if self.stable == 1:
                # min 0.005 increments, unit is lbs
                if (self.last_value + 0.01) < a:
                    print("The weight increased")
                    difference = a - self.last_value
                    self.last_value = a
                    sw.stop()
                    print("TIME (check stable): ", sw.read())
                    return difference
                print("the weight stays the same or decreased")
                self.last_value = a
            sw.stop()
            print("TIME (check): ", sw.read())
            return 0  # value stays the same or decreases
        return -1 #there is no data from scale, meaning that it's not stable

    def open(self) -> None:
        self.ser.open()

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

    while(True):
        print(s.check())  # 0:unusable, -1:error, others: difference in mass

    s.close()
