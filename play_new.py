#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import configparser
import requests
import json

reader = SimpleMFRC522()

env = configparser.ConfigParser()
env.read('.env')

last_id = None

try:
        print("Warte auf Karte")
        while True:
                id = reader.read_id_no_block()

                if id == last_id:
                        continue

                if not id:
                        last_id = None
                        print("Pause")
                        requests.get("http://localhost:3000/api/v1/commands/?cmd=pause")
                        continue

                last_id = id
                print("Suche Karte...")
                headers = { 'Authorization': 'Bearer ' + env['Airtable']['apikey'] }
                cards = requests.get('https://api.airtable.com/v0/appJTWuESqyjqLY5Q/Cards?filterByFormula={ID}=%(id)i' % { 'id': id }, headers=headers).json()

                print(cards)

                if 'records' in cards and len(cards['records']) > 0:
                        uri = cards['records'][0]['fields']['URL']                
                        print("Spiele", uri)

                        payload = { "item": { "uri": uri } }
                        headers = { 'content-type': 'application/json' }
                        r = requests.post("http://localhost:3000/api/v1/replaceAndPlay",
                                          data=json.dumps(payload),
                                          headers=headers)
                        print(r.text)
                        r = requests.get("http://localhost:3000/api/v1/getState")
                        print(r.text)
                else:
                        print("Neue Karte", id)
finally:
	GPIO.cleanup()


