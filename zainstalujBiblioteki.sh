#!/bin/bash
##Skrypt ten odpowiedzialny jest za instalowanie odpowiednich bibliotek niezbednych do pobierania informacji z czujnika temp/wilg.
apt-get update -y && apt-get --yes --force-yes install python3 python3-setuptools python3-pip python3-dev libffi-dev build-essential python-openssl && sudo pip3 install adafruit-circuitpython-dht && pip3 install pika && echo "Oprogramowanie zainstalowane pomyślnie. Aby rozpocząć pracę proszę wpisać ./wyslijNaServer"
