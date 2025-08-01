# coding=utf-8
# Copyright © 2020 Richard Gemmell
# Released under the MIT License. See license.txt. (https://opensource.org/licenses/MIT)

import struct
from time import sleep

from smbus2 import *

# duty cycle vals range from 0 to 256, result in a duty cycle of val/256  
# (using uint 8 here so missing 256, but will never be using 100% duty cycle)
stopped_duty_cycle = 128
min_duty_cycle = 167
max_duty_cycle = 217

sleep_time = 0.1

registers = [0, 2, 4, 6]

def main():
    address = 0x2D
    bus = SMBus(1)
    try:
        safe_write_byte(bus, address, 0, stopped_duty_cycle)
        for i in range(stopped_duty_cycle, max_duty_cycle):
            for reg in registers:
                write_to_target(bus, address, reg, i)
            
        for i in range(max_duty_cycle, min_duty_cycle - 1, -1):
            for reg in registers:
                write_to_target(bus, address, reg, i)
            
        for i in range(min_duty_cycle, stopped_duty_cycle + 1):
            for reg in registers:
                write_to_target(bus, address, reg, i)
            
    finally:
        bus.close()
        
def write_to_target(bus, address, register, duty_cycle):
    safe_write_byte(bus, address, register, duty_cycle)
    sleep(sleep_time)
    read_duty_cycles(bus, address)


# def read_values(bus, address):
#     flags = safe_read(bus, address, 2, 1)[0]
#     print("Flags:", flags)
#     temp = safe_read(bus, address, 3, 1)[0]
#     print("Temp:", temp)
#     voltage = to_long(safe_read(bus, address, 6, 4))
#     print("Voltage:", voltage)
#     voltage = to_long(safe_read(bus, address, 10, 4))
#     print("Current:", voltage)

def read_duty_cycles(bus, address):
    dc1 = safe_read(bus, address, 0, 1)[0]
    print("duty_cycle_1:", dc1)
    # dc2 = safe_read(bus, address, 1, 1)[0]
    # print("duty_cycle_2:", dc2)


def safe_read(bus, address, register, num_bytes):
    data = []
    try:
        data = bus.read_i2c_block_data(address, register, num_bytes)
    except:
        print("Error reading from slave.\nCheck that the wiring is correct and you're using the correct pins.")
    return data


def safe_write_byte(bus, address, register, value):
    try:
        bus.write_byte_data(address, register, value)
    except:
        print("Error writing to slave.\nCheck that the wiring is correct and you're using the correct pins.")


def to_long(data):
    return struct.unpack('<L', bytes(data))[0]


if __name__ == '__main__':
    main()
