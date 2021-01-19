#!/bin/bash
apt-get update -y && apt-get --yes --force-yes install python3 python3-setuptools python3-pip python3-dev libffi-dev build-essential python-openssl && sudo pip3 install adafruit-circuitpython-dht && python3 -m venv .env && source .env/bin/activate && pip3 install adafruit-circuitpython-dht
