raspIBus
========

-- INCOMPLETE PROJECT --

RaspberryPi media player for the iBUS - for BMW X3 / E83 / 2010 

RaspberryPi 	->		FT232RL (USB to SERIAL adapter) 	->		iBus simple interface				

RaspberryPi 	-> 		AUX (sound)


TODO
----

[*] Debug interface - Read and Write messages from connected car through IBUS - raspibusDebug.py

[ ] CD Changer Emulator - Output custom information to the BoardMonitor through IBUS identified as the CD Changer

[ ] Map input from steering wheel and car controls to events

[ ] Setup media player interface with input and output modules


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


Some IBUS Codes on the X3 (e83/2010)
------------------------------------

NEXT / PREV
{'dat': ['3B', '01'], 'src': '50', 'dst': 'C8', 'xor': 'A6', 'len': '04'}
{'dat': ['3B', '21'], 'src': '50', 'dst': 'C8', 'xor': '86', 'len': '04'}
{'dat': ['3B', '08'], 'src': '50', 'dst': 'C8', 'xor': 'AF', 'len': '04'}
{'dat': ['3B', '28'], 'src': '50', 'dst': 'C8', 'xor': '8F', 'len': '04'}

VOL - / +
{'dat': ['32', '10'], 'src': '50', 'dst': '68', 'xor': '1E', 'len': '04'}
{'dat': ['32', '10'], 'src': '50', 'dst': '68', 'xor': '1E', 'len': '04'}
{'dat': ['32', '11'], 'src': '50', 'dst': '68', 'xor': '1F', 'len': '04'}
{'dat': ['32', '11'], 'src': '50', 'dst': '68', 'xor': '1F', 'len': '04'}

BMB PREV / NEXT
{'dat': ['48', '10'], 'src': 'F0', 'dst': '68', 'xor': 'C4', 'len': '04'}
{'dat': ['48', '90'], 'src': 'F0', 'dst': '68', 'xor': '44', 'len': '04'}
{'dat': ['48', '00'], 'src': 'F0', 'dst': '68', 'xor': 'D4', 'len': '04'}
{'dat': ['48', '80'], 'src': 'F0', 'dst': '68', 'xor': '54', 'len': '04'}

BMB ENCODER LEFT / RIGHT / CLICK
{'dat': ['32', '10'], 'src': 'F0', 'dst': '68', 'xor': 'BE', 'len': '04'}
{'dat': ['32', '11'], 'src': 'F0', 'dst': '68', 'xor': 'BF', 'len': '04'}
{'dat': ['48', '06'], 'src': 'F0', 'dst': '68', 'xor': 'D2', 'len': '04'}
{'dat': ['48', '86'], 'src': 'F0', 'dst': '68', 'xor': '52', 'len': '04'}

BMB BUTTONS 1 -> 6
{'dat': ['48', '11'], 'src': 'F0', 'dst': '68', 'xor': 'C5', 'len': '04'}
{'dat': ['48', '91'], 'src': 'F0', 'dst': '68', 'xor': '45', 'len': '04'}
{'dat': ['48', '01'], 'src': 'F0', 'dst': '68', 'xor': 'D5', 'len': '04'}
{'dat': ['48', '81'], 'src': 'F0', 'dst': '68', 'xor': '55', 'len': '04'}
{'dat': ['48', '12'], 'src': 'F0', 'dst': '68', 'xor': 'C6', 'len': '04'}
{'dat': ['48', '92'], 'src': 'F0', 'dst': '68', 'xor': '46', 'len': '04'}
{'dat': ['48', '02'], 'src': 'F0', 'dst': '68', 'xor': 'D6', 'len': '04'}
{'dat': ['48', '82'], 'src': 'F0', 'dst': '68', 'xor': '56', 'len': '04'}
{'dat': ['48', '13'], 'src': 'F0', 'dst': '68', 'xor': 'C7', 'len': '04'}
{'dat': ['48', '93'], 'src': 'F0', 'dst': '68', 'xor': '47', 'len': '04'}
{'dat': ['48', '03'], 'src': 'F0', 'dst': '68', 'xor': 'D7', 'len': '04'}
{'dat': ['48', '83'], 'src': 'F0', 'dst': '68', 'xor': '57', 'len': '04'}

