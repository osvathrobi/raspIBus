#!/usr/bin/python

import os, sys, time, signal, binascii, termcolor, json, logging, subprocess
from time import strftime as date
from ibus_interface import *

import ibus_eventDriver as eventDriver

# put defaults for these globals so we dont get "undefined" errors
DEVPATH           = ""
IBUS              = None
REGISTERED        = False


def initialize():
  global IBUS, REGISTERED, DEVPATH
  REGISTERED=False
  
  # Initialize the iBus interface or wait for it to become available.
  while IBUS == None:
    if os.path.exists(DEVPATH):
      IBUS = ibusFace(DEVPATH)
    else:
      logging.warning("USB interface not found at (%s). Waiting 1 seconds.", DEVPATH)
      time.sleep(2)
  #IBUS.waitClearBus() # Wait for the iBus to clear, then send some initialization signals
  
  logging.info("Initializing eventDriver")
  eventDriver.init(IBUS)
  
def shutdown():
  global IBUS
  logging.info("Shutting down event driver")
  eventDriver.shutDown()
  
  if IBUS:
    logging.info("Killing iBUS instance")
    IBUS.close()
    IBUS = None

def run():
  eventDriver.listen()
