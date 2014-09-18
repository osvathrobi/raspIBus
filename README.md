raspIBus
========

-- INCOMPLETE PROJECT --

RaspberryPi media player for the iBUS - for BMW X3 / E83 / 2010 

RaspberryPi 	->		FT232RL (USB to SERIAL adapter) 	->		iBus simple interface				

RaspberryPi 	-> 		AUX (sound)


TODO
----

[OK] Debug interface - Read and Write messages from connected car through IBUS - raspibusDebug.py

[ ] CD Changer Emulator - Output custom information to the BoardMonitor through IBUS identified as the CD Changer

[OK] Map input from steering wheel and car controls to events

[OK] Setup media player interface with input and output modules


Resources and External links
----------------------------

http://pibus.info/index.html

https://github.com/toxsedyshev/imBMW

https://github.com/cgart/OpenBM

http://www.alextronic.de/bmw/projects_bmw_info_ibus.html

https://github.com/ezeakeal/pyBus

http://e46canbus.blogspot.ro/2014/03/ikbus-interface-options-for-arduino.html

http://www.reslers.de/IBUS/index.html

https://github.com/karis79/bmw-ibus/blob/master/bmw-ibus.c


Thank you pyBus
---------------

https://github.com/ezeakeal/pyBus


Instalation on my rig
---------------------

- A custom made adapter to work with the usb adapter.

![alt text](http://i58.tinypic.com/5efx3n.jpg)

- iBUS tapped into NAV blue connector (with PIN jumper cables)

![alt text](http://i62.tinypic.com/10sdhdx.jpg)

- Final instalation is an open USB Connector

![alt text](http://i58.tinypic.com/358qmgi.jpg)

