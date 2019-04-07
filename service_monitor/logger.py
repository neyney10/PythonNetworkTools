from event import *
from datetime import datetime # for getting current time
import os
from defence import File_Monitor
####################### Class Description: ####################### 
# The Logger class is a class which handles all the output to files
# the class contains a last-modified file check before writing or reading to the 
# log file, alerting the user on console if the file has been modified outside
# of the program by someone else using the "defence\File_Monitor" module, the logger is appending data to the chosen filepath
# and not overwriting it.
class Logger:
    ## Constructor
    # Input: filepath as string to the path+name of the file to log.
    def __init__(self, filepath):
        self.filepath = filepath
        File_Monitor.updateLastTime(self.filepath)
        
        #self.last_time = 0
        #self.updateLastTime()

    ## outputs an Event class type object to a file.
    # Input: ev as Event
    def output2file(self,ev):
        try:
            File_Monitor.checkChange(self.filepath)

            f = open(self.filepath, "a")
            f.write(str(ev)+"\n")
            
        except IOError:
            print 'ERROR [Logger-output2file]: file cannot be opened or file not found.'
        finally:
            f.close() # free resources
            File_Monitor.updateLastTime(self.filepath)

    ## Read file lines from the file, each line can be converted
    ## into an event using an parser from string to event such as
    ## the 'Converter' class using 'decode' function.
    # Input: None.
    # Output: list (array) of lines strings representing events
    def inputFromFile(self):
        try:
            File_Monitor.checkChange(self.filepath)

            f = open(self.filepath, "r")
            lines = []
            for l in f:
                lines.append(l)

            return lines
        except:
            print 'ERROR [Logger-inputFromFile]: file cannot be opened or file not found.'
        finally:
            f.close()
            File_Monitor.updateLastTime(self.filepath)

    