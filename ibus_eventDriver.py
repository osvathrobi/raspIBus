import os, sys, time, signal, json, logging, traceback

import mpd_client as mpc

WRITER = None
SESSION_DATA = {}
TICK = 0.01 # sleep interval in seconds used between iBUS reads
SUB_OUT = None
AIRPLAY = False


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
      '4811': 'd_play'
      '4801': 'd_stop'      
    }
  }
}


# -------- Exposed functions for the intercepted events


def d_cdNext(packet):
  logging.info("Playing next song..")
  mpc.next()

def d_cdPrev(packet):
  logging.info("Playing previous song..")
  mpc.previous()
  
def d_play(packet):
  logging.info("Playing..")
  mpc.play()

def d_play(packet):
  logging.info("Stopping..")
  mpc.stop()


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
      logging.debug('Read packet data: %s', packet)
      manage(packet)
    time.sleep(TICK) # sleep a bit

def shutDown():
  logging.debug("Quitting Audio Client")
  mpc.quit()


class TriggerRestart(Exception):
  pass
class TriggerInit(Exception):
  pass