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
import threading
import serial
# import time
import collections
import sector_draw
import pygame
import time
Reading = collections.namedtuple(
    'Reading', ['mode', 'stable', 'overflow', 'weight', 'units'])
baud_rate = 9600  # scale supports 1200, 2400, 4800, 9600

white = (255, 255, 255)
black = (0, 0, 0)


class Scale_Thread(threading.Thread):
    def __init__(self, screen, scale_lock: threading.RLock=None, text_box: sector_draw.text_surface=None, header: sector_draw.text_surface=None, header_text=None, im_list=None, top_rect_list=None, mid_rect_list=None, bot_rect_list=None, top_rect=None, mid_rect=None, bot_rect=None):
        self._Scale = Scale()
        super(Scale_Thread, self).__init__()
        self.daemon = True
        self._lock = scale_lock
        self._text_bubble = text_box
        self._header = header
        self._screen = screen
        self._header_text = header_text
        self._im_list = im_list
        self._top_rect_list = top_rect_list
        self._mid_rect_list = mid_rect_list
        self._bot_rect_list = bot_rect_list
        self._top_rect = top_rect
        self._mid_rect = mid_rect
        self._bot_rect = bot_rect

    def run(self):
        weight = 0
        while(True):
            if self._Scale.ser.in_waiting >= 6:
                reading = self._Scale.ser.read(6)
                while((len(reading) != 6 or reading[0] != 0xff)):
                    self._Scale.ser.close()
                    self._Scale.ser.open()
                    reading = self._Scale.ser.read(6)
                if not(reading[2] == self._Scale.raw[2] and reading[3] == self._Scale.raw[3] and reading[1] == self._Scale.raw[1] and reading[4] == self._Scale.raw[4]):
                    weight = self._Scale.check(reading)
                    if(weight):
                        while(not(self._lock.acquire(blocking=False))):
                            pygame.event.pump()
                        self._screen.fill(white)
                        pygame.event.pump()
                        self._text_bubble.draw_text_surface(
                            sector_draw.compost_text_processing(weight))
                        pygame.event.pump()
                        pygame.display.flip()
                        pygame.event.pump()
                        time.sleep(4)
                        pygame.event.pump()
                        self._screen.fill(white)
                        self._header.draw_text_surface(self._header_text)
                        pygame.display.flip()
                        self._screen.fill(white, self._top_rect)
                        self._screen.fill(white, self._mid_rect)
                        self._screen.fill(white, self._bot_rect)
                        pygame.display.flip()
                        pygame.event.pump()
                        self._screen.blit(
                            self._im_list[0], self._top_rect_list[0])
                        pygame.event.pump()
                        self._screen.blit(
                            self._im_list[1], self._mid_rect_list[1])
                        pygame.event.pump()
                        self._screen.blit(
                            self._im_list[2], self._bot_rect_list[2])
                        pygame.event.pump()
                        pygame.event.pump()
                        pygame.display.flip()
                        pygame.event.pump()
                        self._lock.release()


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
        self.weight_threshold = 0.006

    def check(self, raw: bytes) -> Reading:
        self.ser.reset_input_buffer()  # flush all inputs

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
        result = result * (-1.0) if negative else result

        if (self.last_value + self.weight_threshold) < result:

            difference = float(result) - float(self.last_value)
            self.last_value = result

            self.raw = raw

            return difference  # return weight change between this and the last stable read in lbs
        else:
            return 0  # weight decreased or stayed the same

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
