import time, logging

#http://alextronic.de/bmw/projects_bmw_info_ibus.html
WRITER = ""

def ibusSendRefresh():
  global WRITER
  WRITER.writeBusPacket('68', '3B', ['A5', '60', '01', '00'])

def ibusSendText(dataPacket):
  global WRITER
  WRITER.writeBusPacket('68', '3B', dataPacket)

def sendText(dst, string):  

    # TITLE DISPLAY
  if dst == 0:
    string = string[0:23]
    dataPacket = ['23', '62', '30']  


  # SMALL TEXT T1->T6
  # ID 0
  if dst == 1:
    string = string[0:4]
    dataPacket = ['A5', '62', '01', '01']  
  # ID 1
  if dst == 2:
    string = string[0:2]
    dataPacket = ['A5', '62', '01', '02']  
  # ID 2
  if dst == 3:
    string = string[0:4]
    dataPacket = ['A5', '62', '01', '03']  
  # ID 3
  if dst == 4:
    string = string[0:2]
    dataPacket = ['A5', '62', '01', '04']  
  # ID 4
  if dst == 5:
    string = string[0:7]
    dataPacket = ['A5', '62', '01', '05']  
  # ID 5
  if dst == 6:
    string = string[0:11]
    dataPacket = ['A5', '62', '01', '06']  



  # Item Fields 0
  if dst == 7:
    string = string[0:23]
    dataPacket = ['21', '60', '00', '40']  

  # Item Fields 1
  if dst == 8:
    string = string[0:23]
    dataPacket = ['21', '60', '00', '41']  

  # Item Fields 2
  if dst == 9:
    string = string[0:23]
    dataPacket = ['21', '60', '00', '42']  

  # Item Fields 5
  if dst == 10:
    string = string[0:23]
    dataPacket = ['21', '60', '00', '45']  

  # Item Fields 6
  if dst == 11:
    string = string[0:23]
    dataPacket = ['21', '60', '00', '46']  

  # Item Fields 7
  if dst == 12:
    string = string[0:23]
    dataPacket = ['21', '60', '00', '47']  
    #dataPacket = ['21', '60', '00', '07']  

  logging.debug('>> Sending text: [%s] to: [%d]' , string , dst)
  dataPacket = appendHexText(dataPacket, string)
  ibusSendText(dataPacket)
  logging.debug('Text Data was succesfully sent')

  # check if need to refresh
  if dst >= 7:
    logging.debug('Sending refresh signal')    
    ibusSendRefresh()

def appendHexText(dataPacket, string):
  stringLen = 0
  logging.debug("Got string for hexing: %s", string)
  while (stringLen < 30) and (len(string) > 0):
    c = string[stringLen]
    dataPacket.append('%02X' % (ord(c)))
    stringLen = stringLen + 1
    if (stringLen == len(string)):
      break

  return dataPacket

def init(writer):
  logging.debug('Initializing BordMonitor')

  global WRITER
  WRITER = writer
