#!/usr/bin/python

import os, sys, time, signal, binascii, termcolor, json, logging, subprocess
from time import strftime as date
from ibus_interface import *

# put defaults for these globals so we dont get "undefined" errors
DEVPATH           = ""
IBUS              = None
REGISTERED        = False


def initialize():
  global IBUS, REGISTERED, DEVPATH
  REGISTERED=False
  
  print DEVPATH

  # Initialize the iBus interface or wait for it to become available.
  while IBUS == None:
    if os.path.exists(DEVPATH):
      IBUS = ibusFace(DEVPATH)
    else:
      logging.warning("USB interface not found at (%s). Waiting 1 seconds.", DEVPATH)
      time.sleep(2)
  IBUS.waitClearBus() # Wait for the iBus to clear, then send some initialization signals
  
  #eventDriver.init(IBUS)
  
def shutdown():
  global IBUS
  logging.info("Shutting down event driver")
  #eventDriver.shutDown()
  
  if IBUS:
    logging.info("Killing iBUS instance")
    IBUS.close()
    IBUS = None

def run():
  print ""
  #eventDriver.listen()
