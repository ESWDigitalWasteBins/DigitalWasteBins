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
#import time
import collections
from stopwatch import Stopwatch

sw = Stopwatch()

Reading = collections.namedtuple(
    'Reading', ['mode', 'stable', 'overflow', 'weight', 'units'])


class Scale:
    def __init__(self) -> None:
        # change from ttyUSB0 to SCALE after creating symlink
        self.ser = serial.Serial('/dev/SCALE', 9600)
        # scale supports 1200, 2400, 4800, 9600
        if (self.ser.isOpen()):
            self.close()
        self.open()
        self.last_value = 0
        self.raw = 0

    def check(self, raw: bytes) -> Reading:
        sw.reset()
        sw.start()
        # Handle first byte
        if len(raw) != 6 or raw[0] != 0xff:
            sw.stop()
            print("TIME (decode fail): ", sw.read())
            return -1
            # raise ValueError('Not a Global 240878 message')
        # preliminary check if the number are equal to each other to
        # avoid doing bitshifting and a lot of post processing
        if not(raw[2] == self.raw[2] and raw[3] == self.raw[3] and raw[1] == self.raw[1] and raw[4] == self.raw[4]):
            # Handle second byte
            decimal_point = raw[1] & 0b111
            #current_mode = (raw[1] & 0b11000) >> 3
            negative = (raw[1] & 0b100000)
            #>> 5
            #self.stable = (raw[1] & 0b1000000) >> 6
            #overflow = (raw[1] & 0b10000000) >> 7
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
            sw.stop()
            print("TIME (decode): ", sw.read())
            #result = result * 16 if unit else result * 35.274
            result = result * (-1.0) if negative else result
            # if negative:
            #    result *= (-1.0)
            sw.reset()
            sw.start()
            #reading = self.ser.read(6)
            sw.stop()
            print("TIME (scale reading): ", sw.read())
            sw.start()
        else:
            return 0
        # will record the last stable value and compare it to the next one
        # run the scale in STB mode
        # if self.stable == 1:
        # min 0.005 increments, unit is lbs
        # if (self.last_value + 0.0005) < result:
            # may need to add check so that people don't pick up thrown in trash and then called it recycled stuffs again
            #print("The weight increased")
        difference = float(result) - float(self.last_value)
        self.last_value = result
        sw.stop()
        self.raw = raw
        print("TIME (check stable): ", sw.read())
        # make it easier to see changed weight
        # print(difference)
        # time.sleep(3) #turn on for debugging
        sw.stop()
        print("TIME (check): ", sw.read())
        return difference  # return weight change between this and the last stable read in kg
        #print("the weight stays the same or decreased")

        #print("There is no data")
        # return 0  # weight haven't changed

    # def check(self):

    def open(self) -> None:
        self.ser.open()

    def close(self) -> None:
        self.ser.close()


# if __name__ == '__main__':
    # Test the examples from Khoi's screenshot
    # from binascii import unhexlify
    # print(decode(unhexlify('ff4487150000')))
    # print(decode(unhexlify('ff4406180000')))
    # print(decode(unhexlify('ff4910000000')))
    # print(decode(unhexlify('ff4407180000')))

#    s = Scale()

#    while(True):
#        print(s.check())  # 0:unusable, -1:error, others: difference in mass

#    s.close()
