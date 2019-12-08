#!/usr/bin/env python3
#-*- coding: utf-8 -*-

SERIAL_PORT = '/dev/ttyAMA0'
TOGGLE_URL = 'http://localhost:3000/api/v1/commands/?cmd=toggle'
VOL_URL = 'http://localhost:3000/api/v1/commands/?cmd=volume&volume=%(vol)s'

import serial

knob = serial.Serial(
    port=SERIAL_PORT,
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

while True:
    if knob.in_waiting:
        x = knob.read(knob.in_waiting)
        if x[0] == 47:
            url = TOGGLE_URL
        elif x[0] == 43:
            url = VOL_URL % { 'vol': 'plus' }
        elif x[0] == 45:
            url = VOL_URL % { 'vol': 'minus' }
        else:
            continue

        print(x, url)
        try:
            requests.get(url, timeout=0.1)
        except:
            pass
