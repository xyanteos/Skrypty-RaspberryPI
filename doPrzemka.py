#!/usr/bin/python3

#Importowanie potrzebnych bibliotek, pika - komunikacja miedzy Rasp a brokerem, subprocess - umozliwia pobranie danych wyjściowych innego skryptu
import pika #,sys
import subprocess
import time


###Tutaj jest sposob na pobranie zmiennych podczas wywolania kodu
#sensor_args = { '11': Adafruit_DHT.DHT11,
#                '22': Adafruit_DHT.DHT22,
#                '2302': Adafruit_DHT.AM2302 }
#if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
#    sensor = sensor_args[sys.argv[1]]
#    pin = sys.argv[2]



credentials = pika.PlainCredentials("client", "clientpass")
conn_params = pika.ConnectionParameters("83.8.31.15", credentials = credentials)
conn_broker = pika.BlockingConnection(conn_params)
channel = conn_broker.channel()


listaWynikow = []

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
print("{Temp : " + str(temp) + ", Humid : " + str(humidity) + ", Date : " + date + ", Time : " + time+"}")
wiadomosc = str("{\nTemp : '" + str(temp) + "',\nHumid : '" + str(humidity) + "',\nDate : '" + date + "',\nTime : '" + time+"'\n}")


listaWynikow.append([temp,humidity])


#time.sleep(5)


###pobieram dane nr2
#proc = subprocess.Popen('../pi/wyslijNaServer',stdout=subprocess.PIPE)
#wiadomosc = str(proc.stdout.read())
###wiadomosc1 = '{Temp:"'+wiadomosc[9:13] + '",Humidity:"' + wiadomosc[27:31]+ '",Date:"' + wiadomosc[44:54] + '",Time:"' + wiadomosc[68:76] +'"}'
#temp = wiadomosc[9:13]
#humidity = wiadomosc[27:31]
#listaWynikow.append([temp,humidity])


#time.sleep(5)


###pobieram dane nr3
#proc1=subprocess.Popen('../pi/wyslijNaServer',stdout=subprocess.PIPE)
#wiadomoscPo = str(proc1.stdout.read())
#temp = wiadomoscPo[9:13]
#humidity = wiadomoscPo[27:31]
#listaWynikow.append([temp,humidity])


###sprawdzam w "brudny" sposob
#print(listaWynikow)
#tempTemp = []
#tempHum= []

#for i in range(0,3):
#    tempTemp.append(int(float(listaWynikow[i][0])))
#    tempHum.append(int(float(listaWynikow[i][1])))
#if(abs(tempTemp[0]-tempTemp[1])<=2.0 and abs(tempTemp[1]-tempTemp[2])<2.0):
#    sredniaTemp = (tempTemp[0]+tempTemp[1]+tempTemp[2])/3
#elif (abs(tempTemp[0]-tempTemp[1])<=2.0):
#    sredniaTemp=(tempTemp[0]+tempTemp[1])/2
#elif (abs(tempTemp[1]-tempTemp[2])<=2.0):
#    sredniaTemp = (tempTemp[1]+tempTemp[2])/2
#elif (abs(tempTemp[0]-tempTemp[2])<=2.0):
#    sredniaTemp = (tempTemp[0]+tempTemp[2])/2
#else:
#    sredniaTemp = tempTemp[2]

#if(abs(tempHum[0]-tempHum[1])<=2 and abs(tempHum[1]-tempHum[2])<2):
#    sredniaHum = (tempHum[0]+tempHum[1]+tempHum[2])/3
#elif (abs(tempHum[0]-tempHum[1])<=2):
#    sredniaHum=(tempHum[0]+tempHum[1])/2
#elif (abs(tempHum[1]-tempHum[2])<=2):
#    sredniaHum = (tempHum[1]+tempHum[2])/2
#elif (abs(tempHum[0]-tempHum[2])<=2):
#    sredniaHum = (tempHum[0]+tempHum[2])/2
#else:
#    sredniaHum=tempTemp[2]


###tworze wiadomosc koncowa
#wiadomoscKoncowa = '{Temp:"'+str(sredniaTemp) + '",Humidity:"' + str(sredniaHum) + '",Date:"' + wiadomoscPo[44:54] + '",Time:"' + wiadomoscPo[68:76] +'"}'



###wysylam
print("wysylam : " + wiadomosc)
msg = "".join(wiadomosc)
msg_props = pika.BasicProperties()
msg_props.content_type = "text/plain"
channel.basic_publish(exchange="data_exchange",properties=msg_props,routing_key="raspberry",body=msg)

conn_broker.close()
