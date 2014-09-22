import os, sys, time, signal, json, logging, traceback

import mpd_client as mpc

WRITER = None
SESSION_DATA = {}
TICK = 0.01 # sleep interval in seconds used between iBUS reads
SUB_OUT = None
AIRPLAY = False
MAX_STRINGLEN = 100

# --- Directives setup (SRC, DST, DATA) --- mapped to a function call

DIRECTIVES = {
  '50'  : {
    '68' : {
        '3B21': 'd_cdNext',
        '3B28': 'd_cdPrev'
    }
  },
  'F0'  : {
    '68'  :{
      '4811': 'd_play',
      '4801': 'd_stop'      
    }
  }
}


# -------- Exposed functions for the intercepted events


def d_cdNext(packet):
  logging.info("Playing next song..")
  mpc.next()
  v = mpc.getInfo()
  print v['track']

  #WRITER.writeBusPacket('68', '3B', _hexText(4, ""))  
  #WRITER.waitClearBus()
  WRITER.writeBusPacket('68', '3B', _hexText(0, v['track']['artist']))
  #WRITER.waitClearBus()
  #WRITER.writeBusPacket('68', '3B', _hexText(1, '1' + v['track']['title']))  
  #WRITER.waitClearBus()
  
  #WRITER.waitClearBus()
  #WRITER.writeBusPacket('68', '3B', _hexText(2, '2' + v['track']['title']))  

  #WRITER.waitClearBus()
  # refresh
  #WRITER.writeBusPacket('68', '3B', _hexText(3, ""))

def d_cdPrev(packet):
  logging.info("Playing previous song..")
  mpc.previous()
  
def d_play(packet):
  logging.info("Playing..")
  mpc.play()

def d_stop(packet):
  logging.info("Stopping..")
  mpc.stop()
  #WRITER.write("68 0B 3B A5 62 01 42 20 50 20 35 20 99");  


def _hexText(dst, string):
  #string = string[0:3]
  print string
  #dataPacket = ['23', '42', '01']

  # TITLE DISPLAY
  if dst == 0:
    dataPacket = ['23', '42', '01']  

  # READ: ['68', '08', '3B', ['A5', '62', '01', '44', '54', '50'], 'DD']
  if dst == 1:
    string = string[0:2]
    dataPacket = ['A5', '62', '01', '41']  

  if dst == 2:
    string = ""
    dataPacket = ['21', '60', '01', '01']

  if dst == 3:
    dataPacket = ['21', '60', '00']  

  if dst == 4:
    dataPacket = ['46', '0C']  

  stringLen = 0
  logging.debug("Got string for hexing: %s", string)
  while (stringLen < 10000) and (len(string) > 0):
    c = string[stringLen] # stringLen doubles up as the index to use when retrieving characters of the string to be displayed.. apologies for how misleading this may be
    dataPacket.append('%02X' % (ord(c)))
    stringLen = stringLen + 1
    if (stringLen == len(string)):
      break

  print dataPacket
  return dataPacket

# -------- Low level Interraction with the IBUS Interfcace
def init(writer):
  global WRITER, SESSION_DATA
  WRITER = writer

  mpc.init()


def manage(packet):
  src = packet['src']
  dst = packet['dst']
  dataString = ''.join(packet['dat'])
  methodName = None
  
  try:
    dstDir = DIRECTIVES[src][dst]
    if ('ALL'  in dstDir.keys()):
      methodName = dstDir['ALL']
    else:
      methodName = dstDir[dataString]
  except Exception, e:
    pass
    
  result = None
  if methodName != None:
    methodToCall = globals().get(methodName, None)
    if methodToCall:
      logging.debug("Directive found for packet - %s" % methodName)
      try:
        result = methodToCall(packet)
      except Exception, e:
        pass
    else:
      logging.debug("Method (%s) does not exist" % methodName)
  else:
    logging.debug("MethodName (%s) does not match a function" % methodName)

  return result
  
def listen():
  logging.info('Event listener initialized')
  while True:
    packet = WRITER.readBusPacket()
    if packet:
      try:
        logging.debug('%s - %s',WRITER.LOCATIONS[packet['src']], packet)
      except Exception,e:
        pass
      
      ss = "";
      for p in packet['dat']:
        try:
          ss = ss + chr(int(p,16))
        except:
          pass          
      logging.debug('Stringified data packet: %s', ss)
      
      manage(packet)
    time.sleep(TICK) # sleep a bit

def shutDown():
  logging.debug("Quitting Audio Client")
  mpc.quit()


class TriggerRestart(Exception):
  pass
class TriggerInit(Exception):
  pass