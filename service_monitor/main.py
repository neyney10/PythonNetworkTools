# main file for the service_monitor program, use this file to start the program.
# Author: Ofek Bader 207206947
# Dependencies: psutil

from logger import *
import processmanager
from monitor import *
from userinterface import CLI
import diff



###### program ######
print('starting service monitor...')



time = 3

monitor = ProcessMonitor(time)
monitor.start()

CLI()





