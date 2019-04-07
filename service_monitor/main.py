############### Description ###########################
# Program Version: 1.1
# Last release date: 07/04/2019
# main file for the service_monitor program, use this file to start the program.
# Python version: 2.7
# Author: Ofek Bader 207206947
# Dependencies: psutil v5.6.1 or better
########################################################

from userinterface import CLI2
from defence import File_Monitor
###### program ######
print('starting service monitor...')
File_Monitor.activate_active_monitoring()
CLI2() #