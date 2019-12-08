# RFID Cards for Volumio

Use RFID cards to control Volumio. The association between card IDs and URLs are maintained in a table in [AirTable](https://airtable.com/).

## Installation

Create a file .env in the installation directory:

````
[Airtable]
apikey=key1234567890
````

Copy the service file to /etc/systemd/system/rfid.service

## Further information

* Volumio REST API: https://volumio.github.io/docs/API/REST_API.html
* How to wire the RFID reader: https://pimylifeup.com/raspberry-pi-rfid-rc522/

## Example entries

Here are some examples for pairs RFID / Spotify URL

# London Grammar
660373477523=spotify:artist:3Bd1cgCjtCI32PYvDC3ynO

# Big Big Train - Folklore
866901399775=spotify:album:3j1MgNFNI90XdSTEGDN4pa

# Sting
245858867403=spotify:artist:0Ty63ceoRnnJKVEYP0VQpk

# ???
180259887130=spotify:album:6UN8m07SmIzyDe63H0oljL
