#!/usr/bin/python3

#Importowanie potrzebnych bibliotek, pika - komunikacja miedzy Rasp a brokerem, subprocess - umozliwia pobranie danych wyjściowych innego skryptu
import pika
import subprocess

##Ustalanie polaczenia z brokerem wiadomosci
credentials = pika.PlainCredentials("client", "clientpass")
conn_params = pika.ConnectionParameters("83.8.31.15", credentials = credentials)
conn_broker = pika.BlockingConnection(conn_params)
channel = conn_broker.channel()

#####pobieram dane nr1
##ustawiam wartosc humid na skrajnie wysoka zeby zrobic zabezpieczenie przed blednym pomiarem (wszystkie bledne pomiary maja humid powyzej 145):
humidity = 255.00
#program bedzie pobieral dane z czujnika dopoki sie nie upewni, ze ma realny wynik
while humidity>145:
    proc0 = subprocess.Popen('./pobierzDane',stdout=subprocess.PIPE)
    wiadomoscPrzed1 = str(proc0.stdout.read())
    #print(wiadomoscPrzed1)
    temp = float(wiadomoscPrzed1[2:6])
    humidity = float(wiadomoscPrzed1[8:12])
    date = wiadomoscPrzed1[15:25]
    time = wiadomoscPrzed1[28:36]
#drukuje dane zebrane przez urzadzenie przed ich wyslaniem
print("{Temp : " + str(temp) + ", Humid : " + str(humidity) + ", Date : " + date + ", Time : " + time+"}")
#tworze formatke wiadomosci do przeslania do brokera
wiadomosc = str("{\nTemp : '" + str(temp) + "',\nHumid : '" + str(humidity) + "',\nDate : '" + date + "',\nTime : '" + time+"'\n}")


###wysylanie danych do brokera
#Drukuje formatke danych przed przesłaniem
print("wysylam : " + wiadomosc)
msg = "".join(wiadomosc)
msg_props = pika.BasicProperties()
msg_props.content_type = "text/plain"
channel.basic_publish(exchange="data_exchange",properties=msg_props,routing_key="raspberry",body=msg)
#zamykam polaczenie z brokerem
conn_broker.close()
