# pi_i2c_pwm_keyboard_controller.py

from sshkeyboard import listen_keyboard
from smbus2 import *
import struct
from time import sleep
import threading

running = True

sleep_time = 0.1

stopped_duty_cycle = 128

# min duty cycle: 1200 us
# 1200/3000 = 102.4/256
min_duty_cycle = 102

# max duty cycle: 1800 us
# 1800/3000 = 153.6/256
max_duty_cycle = 154

cur_duty_cycle = stopped_duty_cycle

address = 0x2D
bus = SMBus(1)

def main():
    
    try:
        keyboard_thread = threading.Thread(target=start_keyboard_listener)
        keyboard_thread.daemon = True
        keyboard_thread.start()
        
        while running:
            safe_write_byte(bus, address, 0, cur_duty_cycle)
            print(f"sent width (us) {cur_duty_cycle / 256 * (1/333) * 1000000}")
            sleep(sleep_time)
    finally:
        # Reset to stopped position before exiting
        safe_write_byte(bus, address, 0, stopped_duty_cycle)
        bus.close()
        
def start_keyboard_listener():
    listen_keyboard(on_press=press, until=None)
        
def press(key):
    global cur_duty_cycle, running, bus, address
    if key == 'k':
        if cur_duty_cycle - 2 >= min_duty_cycle:
            cur_duty_cycle -= 2
    if key == 'i':
        if cur_duty_cycle + 2 <= max_duty_cycle:
            cur_duty_cycle += 2
    if key == 'r':
        cur_duty_cycle = 128
    if key == 'q':
        running = False
    if key == 'p':
        read_duty_cycles(bus, address)
    print(cur_duty_cycle)
        
        

def write_to_target(bus, address, register, duty_cycle):
    safe_write_byte(bus, address, register, duty_cycle)
    read_duty_cycles(bus, address)
    
def read_duty_cycles(bus, address):
    dc1 = safe_read(bus, address, 0, 1)[0]
    print("duty_cycle_1_us:", dc1 / 256 * (1/333) * 1000000)
    
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