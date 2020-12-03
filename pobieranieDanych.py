#!/usr/bin/python3
import adafruit_dht
import board
dht_device = adafruit_dht.DHT11(4)
temp = dht_device.temperature
humid = dht_device.humidity
print('{0:0.1f}, {1:0.1f}'.format(temp,humid))
