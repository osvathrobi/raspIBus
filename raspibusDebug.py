#!/usr/bin/python

import os
import sys
import time
import signal
import traceback
import logging
import argparse
import gzip

def signal_handler_quit(signal, frame):
  logging.info("Shutting down raspIBUS")
  core.shutdown()
  sys.exit(0)

#################################
# Configure Logging for pySel
#################################
def configureLogging(numeric_level):
  if not isinstance(numeric_level, int):
    numeric_level=0
  logging.basicConfig(
    level=numeric_level,
    format='%(asctime)s [%(levelname)s in %(module)s] %(message)s', 
    datefmt='%Y/%m/%d %I:%M:%S'
  )
  
def createParser():
  parser = argparse.ArgumentParser()
  parser.add_argument('-v', '--verbose', action='count', default=0, help='Increases verbosity of logging.')
  parser.add_argument('--device', action='store', help='Device path for the USB-SERIAL device connected to the IBUS')
  return parser

def restart():
  args = sys.argv[:]
  logging.info('Re-spawning %s' % ' '.join(args))

  args.insert(0, sys.executable)

  os.chdir(_startup_cwd)
  os.execv(sys.executable, args)



#####################################
# MAIN
#####################################
parser   = createParser()
results  = parser.parse_args()
loglevel = results.verbose
_startup_cwd = os.getcwd()

# Manage Ctrl+C
signal.signal(signal.SIGINT, signal_handler_quit) 

# Configure logging
configureLogging(loglevel)

# Setup USB-SERIAL device
if results.device:
  devPath = results.device
else:
  devPath = "/dev/ttyUSB0"
  logging.info('Device argument missing. Using default: %s', devPath)

    
sys.exit(0)
