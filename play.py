#!/usr/bin/env python3
#-*- coding: utf-8 -*-

INSTALL_PATH = '/home/volumio/rfid/.env'
SEARCH_URL = 'https://api.airtable.com/v0/appJTWuESqyjqLY5Q/Cards?filterByFormula={ID}=%(id)i'
PLAY_URL = 'http://localhost:3000/api/v1/replaceAndPlay'
STATE_URL = 'http://localhost:3000/api/v1/getState'
NEWCARD_URL = 'https://api.airtable.com/v0/appJTWuESqyjqLY5Q/Cards'
PAUSE_URL = 'http://localhost:3000/api/v1/commands/?cmd=pause'

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import configparser
import requests
import json

reader = SimpleMFRC522()

env = configparser.ConfigParser()
env.read(INSTALL_PATH)

count_reset = 5
last_id = None
count = count_reset

def search(id):
        headers = { 'Authorization': 'Bearer ' + env['Airtable']['apikey'] }
        cards = requests.get(SEARCH_URL % { 'id': id }, headers=headers).json()

        if 'records' in cards and len(cards['records']) > 0:
                return cards['records'][0]['fields']['URL']
        else:
                return None

def play(id):
        uri = search(id)
        if uri:
                print("Spiele", uri)
                payload = { "item": { "uri": uri } }
                headers = { 'content-type': 'application/json' }
                r = requests.post(PLAY_URL,
                                  data=json.dumps(payload),
                                  headers=headers)
                return
                print(r.text)
                r = requests.get(STATE_URL)
                print(r.text)
        else:
                print("Neue Karte", id)
                newcard(id)


def newcard(id):
        headers = {
                'Authorization': 'Bearer ' + env['Airtable']['apikey'],
                'Content-Type': 'application/json'
        }
        payload = {
                'fields': {
                        'ID': str(id)
                }
        }
        r = requests.post(NEWCARD_URL,
                          data=json.dumps(payload),
                          headers=headers)
        print(r.text)

#
#-----------------------------------------------------
try:
        print("Warte auf Karte")
        while True:
                id = reader.read_id_no_block()
                if id:
                        count = count_reset
                        if id == last_id:
                                continue
                        
                        last_id = id
                        print("Karte", id)
                        play(id)
                else:
                        if not last_id:
                                continue

                        if count > 0:
                                #print(" - Counting", count)
                                count -= 1
                                continue

                        count = count_reset
                        last_id = None
                        print("Pause")
                        try:
                                requests.get(PAUSE_URL,
                                             timeout=0.1
                                )
                        except:
                                pass

finally:
	GPIO.cleanup()


