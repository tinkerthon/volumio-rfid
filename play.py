#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import configparser
import requests
import json

reader = SimpleMFRC522()

cards = configparser.ConfigParser()
cards.read('cards.ini')

try:
        while True:
                print("Warte auf Karte...")
                id, _ = reader.read()
                id = str(id)
                
                if id in cards['cards'].keys():
                        uri = cards['cards'][id].strip()
                        print("Karte fuer", uri)
                        payload = { "item": { "uri": uri } }
                        headers = { 'content-type': 'application/json' }
                        r = requests.post("http://localhost:3000/api/v1/replaceAndPlay",
                                          data=json.dumps(payload),
                                          headers=headers)
                        print(r.text)
                        r = requests.get("http://localhost:3000/api/v1/getState")
                        print(r.text)
                elif id in cards['commands'].keys():
                        cmd = cards['commands'][id].strip()
                        print("Befehl:", cmd)
                        r = requests.get("http://localhost:3000/api/v1/commands/?cmd=stop")
                        print(r.text)
                else:
                        print("Karte mit ID", id, " ist noch nicht programmiert")
                        continue
finally:
	GPIO.cleanup()


