#! /usr/bin/python 

import RPi.GPIO as GPIO
from time import time

GPIO.setmode(GPIO.BCM)

data_pins = [24, 4, 17, 22, 9, 25, 18, 23]
clock_pin = 8
chip_select = 10
irq_pin = 20

GPIO.setup(clock_pin, GPIO.OUT)
GPIO.setup(irq_pin, GPIO.IN)
GPIO.setup(chip_select, GPIO.OUT)

def send_byte(byte_out):
    """
    Send a single byte.
    """
    GPIO.output(clock_pin, 0)
    # set the chip select to write
    #GPIO.output(chip_select, 1)
    # send the byte 
    values = [(ord(byte_out) >> i) % 2 for i in range(0, 8)]
    GPIO.setup(data_pins, GPIO.OUT)
    GPIO.output(data_pins, values)
    # flash the clock pin
    GPIO.output(clock_pin, 1)
    GPIO.output(clock_pin, 0)   


def get_byte():
    """
    Get a single byte.
    """
    GPIO.setup(data_pins, GPIO.IN)
    # read the data pins
    #GPIO.output(chip_select, 0)
    GPIO.output(clock_pin, 1)
    GPIO.output(clock_pin, 0)
    value = 0
    for i in range(0, 8):
        value += GPIO.input(data_pins[i]) << i
    return value

if __name__ == "__main__":
    while True:
        start = time()

        GPIO.output(clock_pin, 0)
        GPIO.output(clock_pin, 0)
        send_byte(chr(0xaa))

        array = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a]
        str1 = [chr(e) for e in array]
        for i in str1:
            send_byte(i)
        while GPIO.input(irq_pin) != 1:
            print("not irq received")
        while GPIO.input(irq_pin) == 1:
            print("irq still received")
        
        GPIO.output(chip_select, 1)
        for i in len(array):
            value = get_byte()
            print("In[",i,"]:",value)
        GPIO.output(chip_select, 0)

        print("Transaction finished.", time()-start)

