#!/usr/bin/python
# -*- coding: utf-8 -*-
# mcp3208_lm35.py - read an 1k Themistisor on CH0 of an MCP3208 on a Raspberry Pi
# mostly nicked from
#  http://jeremyblythe.blogspot.ca/2012/09/raspberry-pi-hardware-spi-analog-inputs.html
# Also from
# http://scruss.com/blog/2013/02/02/simple-adc-with-the-raspberry-pi/

import spidev
import time
import math

class MCP3208:
    def __init__(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0, 1)

    def getValue_(self, channel):
        r = self.spi.xfer2([1, (8 + channel) << 4, 0])
        v = ((r[1] & 3) << 8) + r[2]
        return v

    def getValue(self, adcnum):
        if adcnum > 7 or adcnum < 0:  # just to check if adcnum is out of the A/D converters channel range
            return -1
        r = self.spi.xfer2([4 + (adcnum >> 2), (adcnum & 3) << 6, 0])
        # send the three bytes to the A/D in the format the A/D's datasheet explains(take time to
        # doublecheck these
        adcout = ((r[1] & 15) << 8) + r[2]
        # use AND operation with the second byte to get the last  4 bits, and then make way
        # for the third data byte with the "move 8 bits to left" << 8 operation
        return adcout