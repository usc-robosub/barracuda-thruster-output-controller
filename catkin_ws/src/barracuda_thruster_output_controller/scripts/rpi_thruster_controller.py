#! /usr/bin/env python3

# 1) subscribe to thrusters/i/input topics to get force value for each thruster (in same force unit as in a wrench message)
# 2) convert force values (assuming it's in Newtons) to kgF
# 3) determine pulse widths (in microseconds) to send to each of the thrusters using kgF to pulse width (us) conversion spreadsheet
# 4) determine duty cycle value given the bit granularity & frequency being used by analogWrite function on the Teensy (e.g. 256-bit, 333Hz frequency)
# 5) send a message to appropriate register on appropriate teensy

from smbus2 import *
import struct
import rospy
from uuv_gazebo_ros_plugins_msgs.msg import FloatStamped
from thruster_data_handler import ThrusterDataHandler
from collections import namedtuple

# TODO: set up thrust config in config dir/use parameters 
ThrusterConfig = namedtuple('ThrusterConfig', ['i2c_address', 'register'])
thruster_organization = {
    0: ThrusterConfig(0x2d, 0),
    1: ThrusterConfig(0x2d, 2),
    2: ThrusterConfig(0x2d, 4),
    3: ThrusterConfig(0x2d, 6),
    4: ThrusterConfig(0x2d, 0),
    5: ThrusterConfig(0x2d, 2),
    6: ThrusterConfig(0x2d, 4),
    7: ThrusterConfig(0x2d, 6)
}

thruster_data_handler = ThrusterDataHandler()
bus = SMBus(1)

# TODO: make these ros parameters
# configuration values for teensy 
pwm_frequency = 400 # period = 2500 µs --> frequency = 400 Hz
pwm_bit_resolution = 15 # highest bit resolution allowed for pwm signals on teensy
    
def on_recv_thruster_kgf(msg, thruster_id):
    pwm_us = thruster_data_handler.kgf_to_pwm_us(msg.data)
    
    # pwm_us / pwm_period = pwm_us * pwm_frequency
    # need to divide pwm_us * pwm_frequency by 10^6 to account for us/s difference, 
    # dividing by 10^3 twice to keep intermediate values smaller
    duty_cycle_val = int(round(((pwm_us / 10**3) * (pwm_frequency / 10**3)) * (2**pwm_bit_resolution)))
    print(f"received kgf value of: {msg.data} for thruster {thruster_id}, wrote duty cycle val: {duty_cycle_val}")
    
    send_duty_cycle_val_to_thruster(duty_cycle_val, thruster_id)
    
def thruster_controller_node():
    rospy.init_node('barracuda_thruster_output_controller')
    # Create subscribers for each thruster
    for i in range(8):
        topic = f"/thrusters/{i}/input"
        rospy.Subscriber(topic, FloatStamped, on_recv_thruster_kgf, callback_args=i)
    
    rospy.spin()   
    
# Helper functions

def send_duty_cycle_val_to_thruster(duty_cycle_val, thruster_id):
    i2c_address = thruster_organization[thruster_id].i2c_address
    thruster_register = thruster_organization[thruster_id].register
    write_int16(bus, i2c_address, thruster_register, duty_cycle_val)

# Writes 2 bytes at a time for uint16_t duty cycle val (or n bytes at a time)
def write_int16(bus, address, register, value):
    """Write a 16-bit integer to a register"""
    data = list(struct.pack('<H', value))  # H is for unsigned short (16-bit)
    safe_write_block(bus, address, register, data)

def safe_write_block(bus, address, register, values):
    try:
        bus.write_i2c_block_data(address, register, values)
    except Exception as e:
        print(f"Error writing to target: {e}")
        print("Check that the wiring is correct and you're using the correct pins.")

def safe_write_byte(bus, address, register, value):
    try:
        bus.write_byte_data(address, register, value)
    except:
        print("Error writing to target.\nCheck that the wiring is correct and you're using the correct pins.")

if __name__ == '__main__':
    thruster_controller_node()





