import os, sys, time, signal, json, logging, traceback

import mpd_client as mpc

WRITER = None
SESSION_DATA = {}
TICK = 0.01 # sleep interval in seconds used between iBUS reads
SUB_OUT = None
AIRPLAY = False

DIRECTIVES = {
  '50'  : {
    'C8' : {
        'A63B': 'd_cdNext'
    }
  },
  '68' : {
      '18' : {
        '01'     : 'd_cdPollResponse',
        '380000' : 'd_cdSendStatus',
        '380100' : 'd_cdStopPlaying',
        '380300' : 'd_cdStartPlaying',
        '380A00' : 'd_cdNext',
        '380A01' : 'd_cdPrev',
        '380700' : 'd_cdScanForward',
        '380701' : 'd_cdScanBackard',
        '380601' : 'd_toggleSS', # 1 pressed
        '380602' : 'd_togglePause', # 2 pressed
        '380603' : 'd_subWDown', # 3 pressed
        '380604' : 'd_subWUp', # 4 pressed
        '380605' : 'd_update', # 5 pressed
        '380606' : 'd_RESET', # 6 pressed
        '380400' : 'd_cdScanBackward',
        '380401' : 'd_cdScanForward',
        '380800' : 'd_cdRandom',
        '380801' : 'd_cdRandom'
      }
  }
}

#####################################
# FUNCTIONS
#####################################
# Set the WRITER object (the iBus interface class) to an instance passed in from the CORE module
def init(writer):
  global WRITER, SESSION_DATA, SUB_OUT
  WRITER = writer

  #pB_display.init(WRITER)
  
  mpc.init()

  #pB_ticker.init(WRITER)
  
  #pB_ticker.enableFunc("announce", 10)


def manage(packet):
  src = packet['src']
  dst = packet['dst']
  dataString = ''.join(packet['dat'])
  methodName = None
  
  #if(not (src in ['A4', '7F', 'E8', 'C8', 'D0', '3B'])):
  
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
      manage(packet)
    time.sleep(TICK) # sleep a bit

def shutDown():

  logging.debug("Quitting Audio Client")
  mpc.quit()

  #logging.debug("Stopping Display Driver")
  #pB_display.end()
  #logging.debug("Killing tick utility")
  #pB_ticker.shutDown()

def d_cdNext(packet):
  logging.info("Playing next song..")
  mpc.next()

class TriggerRestart(Exception):
  pass
class TriggerInit(Exception):
  pass