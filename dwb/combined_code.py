import pygame
from frame import Frame
from frame_header import Header
from frame_body import Body


import serial
import collections

Reading = collections.namedtuple(
    'Reading', ['mode', 'stable', 'overflow', 'weight', 'units'])


class Scale:
    @staticmethod
    def decode(self, raw: bytes) -> Reading:
        # Handle first byte
        if len(raw) != 6 or raw[0] != 0xff:
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
        return result

    def __init__(self) -> None:
        self.ser = serial.Serial('/dev/ttyUSB0', 9600)
        self.last_value = 0
        self.stable = 0
        self.original_weight = 0
        self.still_increasing = 0
        self.originnal_value = 0

    def check(self):
        a = Scale.decode(self, self.ser.read(6))
        if self.stable == 1:
            # min 0.005 increments, unit is lbs
            if (self.last_value + 0.01) < a:
                print("The weight increased")
                difference = a - self.last_value
                self.last_value = a
                return difference
            '''
            if self.last_value == a and self.still_increasing == 1:
                self.still_increasing = 0
                difference = a - self.originnal_value
                return difference  # weight finished rising
            if self.last_value + 0.05 < a and self.still_increasing == 0:
                self.still_increasing = 1
                self.originnal_value = a  # weight start rising here
            if self.last_value + 0.05 < a and self.still_increasing == 1:
                self.still_increasing = 1  # weight is still rising
            self.last_value = a
            '''
            print("the weight stays the same or decreased")
            self.last_value = a
        return 0  # value stays the same or decreases

    def close(self) -> None:
        self.ser.close()

