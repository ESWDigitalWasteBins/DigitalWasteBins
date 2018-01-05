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

IMPORTANT: Assumptions made on the hardware
Assuming that the scale runs in STB mode(send when stable)
Assuming that the units are in lbs
"""

import serial
# import time
import collections

Reading = collections.namedtuple(
    'Reading', ['mode', 'stable', 'overflow', 'weight', 'units'])
baud_rate = 9600  # scale supports 1200, 2400, 4800, 9600


class Scale:
    def __init__(self) -> None:
        # change from ttyUSB0 to SCALE after creating symlink
        self.ser = serial.Serial('/dev/SCALE', baud_rate)
        if (self.ser.isOpen()):
            self.close()
        self.open()
        self.last_value = 0
        self.raw = [0, 0, 0, 0, 0, 0]
        # minimum increase in weight to be counted as increased
        self.weight_threshold = 0.001

    def check(self, raw: bytes) -> Reading:

        # Handle first byte
        if len(raw) != 6 or raw[0] != 0xff:
            self.ser.close()
            self.ser.open()
            raw = self.ser.read(6)
            if len(raw) != 6 or raw[0] != 0xff:
                return -1
            # raise ValueError('Not a Global 240878 message')
        # preliminary check if the number are equal to each other to
        # avoid doing bitshifting and a lot of post processing

        self.ser.reset_input_buffer()  # flush all inputs in buffer to avoid cluttering
        if not(raw[2] == self.raw[2] and raw[3] == self.raw[3] and raw[1] == self.raw[1] and raw[4] == self.raw[4]):
            # Handle second byte
            self.raw = raw
            decimal_point = raw[1] & 0b111
            # current_mode = (raw[1] & 0b11000) >> 3
            negative = (raw[1] & 0b100000)
            #>> 5
            # self.stable = (raw[1] & 0b1000000) >> 6
            # overflow = (raw[1] & 0b10000000) >> 7
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
            result = float(digit1) + digit2 * 10 + digit3 * 100 + \
                digit4 * 1000 + digit5 * 10000 + digit6 * 100000
            result /= float(10 ** (decimal_point - 1))  # more precision
            # Convert from lbs to ounce
            result = result * 16
            # Handle sixth byte
            # unit = raw[5] & 0b1  # 1 for lbs and 0 for kg

            # result = result * 16 if unit else result * 35.274
            result = result * (-1.0) if negative else result
            # if negative:
            #    result *= (-1.0)

            # reading = self.ser.read(6)

        else:
            return 0  # means values stay the same

        if (self.last_value + self.weight_threshold) < result:

            difference = float(result) - float(self.last_value)
            self.last_value = result

            self.raw = raw
            return difference  # return weight change between this and the last stable read in lbs
        else:
            return 0  # weight decreased or stayed the same

    # def check(self):

    def open(self) -> None:
        self.ser.open()

    def close(self) -> None:
        self.ser.close()


"""
if __name__ == '__main__':
    # Test the examples from Khoi's screenshot

    s = Scale()

    while(True):
        # 0:unusable, -1:error, others: difference in mass
        print(s.check(s.ser.read(6)))

    s.close()
"""
