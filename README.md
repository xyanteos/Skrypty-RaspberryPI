# Logika działania
(outdated)
Na urządzeniu `Raspberry Pi` w czasie rzeczywistym działa program o nazwie `"dzialaj"`. 
Program ten uruchamia równo co minutę skrypt python-owski `"mqtt.py"`, który pobiera dane wyjściowe z krótkiego skryptu `"wyslijNaServer"`, zapisuje je w postaci tymczasowego stringa, po czym wycina z niego dane potrzebne do porównania. Pobieranie danych odbywa się 3 razy w przerwach 5-cio sekundowych, aby ostatecznie poddać je analizie oraz uwiarygodnieniu, stworzyć średnią arytmetyczną z wiarygodnych danych, i wysłać do brokera wiadomości MQTT.
