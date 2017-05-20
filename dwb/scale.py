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
    f. No. 6: D0-D7 = Unit for weight: 1 – Lb; 0 - kg

Bytes 3-5 to Digits
D2: 0001 D1: 0000
D4: 0000 D3: 0000
D6: 0000 D5: 0000
"""

#import serial
import collections

Reading = collections.namedtuple('Reading', ['mode', 'stable', 'overflow', 'weight', 'units'])

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
    result = digit1 + (digit2 * 10) + (digit3 * 100) + (digit4 * 1000) + (digit5 * 10000) + (digit6 * 100000)
    result /= 10 ** decimal_point
    # Handle sixth byte
    unit = raw[5] & 0b1
    return Reading(current_mode, stable, overflow, result, unit)

#ser=serial.Serial('/dev/ttyUSB0/')
#data=ser.read(10)
#ser.open()
#ser.close()
def scaleReading():
    # Skeleton function for reading from scale for now
    return 25

if __name__ == '__main__':
    # Test the examples from Khoi's screenshot
    from binascii import unhexlify
    print(decode(unhexlify('ff4487150000')))
    print(decode(unhexlify('ff4406180000')))
    print(decode(unhexlify('ff4910000000')))
    print(decode(unhexlify('ff4407180000')))
