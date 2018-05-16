getIDm: getIDm.cpp
	g++ -c -DUNICODE HardwareSerial.cpp
	g++ -c -DUNICODE RCS620S.cpp
	g++ -lwiringPi RCS620S.o HardwareSerial.o -DUNICODE getIDm.cpp -o getIDm
