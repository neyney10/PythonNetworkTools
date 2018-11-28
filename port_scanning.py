import socket
import sys
import time
import random
import os.path

# ---------------- NOTES ---------------- #
# this is port scanning python 2.7.1 code written by Ofek Bader, VERSION 1.0 
# last update: 21/10/2018 21:09
# have basic functionalltiy as:
# Modes: "slow" scanning port by port and have a short pause every 10 ports, the time to pause in seconds is SCAN_PARAM
# "random" scanning randomly chosen ports
# "auto" scanning only known ports
# syntax: [TARGET] [SCAN_TYPE] [SCAN_PARAM]
# example: 192.168.0.140 slow 3
# example: 8.8.8.8 random
# example: 10.0.43.12 auto
# ---------------- NOTES ---------------- #

# ----------- DEVELOPER NOTES ----------- #
# - None
# ----------- DEVELOPER NOTES ----------- #

# --------- #
# FUNCTIONS #
# --------- #

# PRINTING + APPENDING TO FILE
def log(text):
    print(text)
    f.write(text+"\n")
    return
    
# ------------ #
# PROGRAM CODE #
# ------------ #

# get command line arguments
args = (sys.argv)

HOST = args[1] # TARGET ADDRESS to scan
PORT = 22 
SCAN_TYPE = args[2] # scan type, can be "slow", "random" or "auto"
SCAN_PARAM = args[3] if SCAN_TYPE == "slow" else 0 # for "slow" mode - time amount of seconds to pause

# init
i = 0
a = []

ext = ''
num = 0
amount = 65536;

# get a non-existent file name to use
while os.path.exists("port_scan"+ext+".txt"):
    num += 1
    ext = `num`

# open/create file for writing/appending
f = open("port_scan"+ext+".txt", "a") 
print("Writing to file: "+f.name)

# for random mode
if SCAN_TYPE == 'random':
    a = range(0, amount)
    random.shuffle(a)

# for auto mode
if SCAN_TYPE == 'auto':
    amount = 1024


print("Mode: " + SCAN_TYPE)
while i < amount:
    try:
        if SCAN_TYPE == 'slow':
            if (PORT+1)%10 == 0:
                time.sleep(int(SCAN_PARAM)) # seconds

        PORT = i
            
        if SCAN_TYPE == 'random':
            PORT = a.pop()

        i += 1

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))

        log('[Open] Port: '+`PORT`)

    except :
        log('[Closed] Port: '+`PORT`)


