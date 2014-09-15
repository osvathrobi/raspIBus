#!/usr/local/Cellar/python/2.7.6_1/bin/python

import os
import sys
import time
import signal
import traceback
import logging
import argparse
import gzip
import ibus_core as core

def signal_handler_quit(signal, frame):
  logging.info("Shutting down raspIBUS")
  core.shutdown()
  sys.exit(0)

# --- Configure Logging for pySel

def configureLogging(numeric_level):
  # set up logging to file - see previous section for more details
  logging.basicConfig(level=numeric_level,
                      format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                      datefmt='%m-%d %H:%M',
                      filename='log/debugger.log',
                      filemode='a')
  # define a Handler which writes INFO messages or higher to the sys.stderr
  console = logging.StreamHandler()
  console.setLevel(logging.INFO)
  # set a format which is simpler for console use
  formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
  # tell the handler to use this format
  console.setFormatter(formatter)
  # add the handler to the root logger
  logging.getLogger('').addHandler(console)

  # Now, we can log to the root logger, or any other logger. First the root...
  logging.info('Jackdaws love my big sphinx of quartz.')
  
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


# ---- MAIN -----

parser   = createParser()
results  = parser.parse_args()
loglevel = logging.DEBUG
_startup_cwd = os.getcwd()

# Manage Ctrl+C
signal.signal(signal.SIGINT, signal_handler_quit) 

# Configure logging
configureLogging(loglevel)

# Setup USB-SERIAL device
if results.device:
  devPath = results.device
else:
  devPath = "/dev/tty.usbserial-A601HPGR"
  logging.warning('Device argument missing. Using default: %s', devPath)

try:
  core.DEVPATH = devPath
  core.initialize();
  core.run();
except:
  logging.error("Caught unexpected exception:")
  logging.error(traceback.format_exc())
  logging.info("Restarting in 3 seconds.. Press CTRL+C to permanantly shut down!")
  time.sleep(3)  
  restart()
    
sys.exit(0)
