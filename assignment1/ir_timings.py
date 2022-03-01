#!/usr/bin/python

import RPi.GPIO as GPIO
from datetime import datetime
from time import sleep
import os

############
# CONSTANTS#
############
# Input pin is 15 (GPIO22)
INPUT_PIN = 15
# To turn on debug print outs, set to 1
DEBUG = 1

###################
# INITIALIZE PINS #
###################
GPIO.setmode(GPIO.BOARD)
GPIO.setup(INPUT_PIN, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(INPUT_PIN, GPIO.IN)

# Main loop, listen for infinite packets
while True:
    print("\nWaiting for GPIO low")

    # If there was a transmission, wait until it finishes
    #GPIO.wait_for_edge(INPUT_PIN, GPIO.RISING)
    value = 1
    while value:
        sleep(0.001)
        #print("Last read value: {}".format(value))
        value = GPIO.input(INPUT_PIN)       

    # timestamps for pulses and packet reception
    startTimePulse = datetime.now()
    previousPacketTime = 0

    print("\nListening for an IR packet")

    # Buffers the pulse value and time durations
    pulseValues = []
    timeValues = []

    # Variable used to keep track of state transitions
    previousVal = 0

    # Inner loop 
    while True:
        # Measure time up state change
        if value != previousVal:
            # The value has changed, so calculate the length of this run
            now = datetime.now()
            pulseLength = now - startTimePulse
            startTimePulse = now

            # Record value and duration of current state
            pulseValues.append(value)
            timeValues.append(pulseLength.microseconds)
            
            # Detect short IR packet using packet length and special timing
            if(len(pulseValues) == 3):
                if(timeValues[1] < 3000):
                    print("Detected Short IR packet")
                    print(pulseValues)
                    print(timeValues)
                    break;

            # Detect standard IR packet using packet length 
            if(len(pulseValues) == 67):
                if(DEBUG==1):
                    print("Finished receiving standard IR packet")
                    print(pulseValues)
                    print(timeValues)
                    #TODO: Decode packet and perform task
                    break;

        # save state
        previousVal = value
        # read GPIO pin
        value = GPIO.input(INPUT_PIN)

