from event import *
from datetime import datetime # for getting current time
import os
####################### Class Description: ####################### 
# The Logger class is a class which handles all the output to files
# the class contains a last-modified file check before writing or reading to the 
# log file, alerting the user on console if the file has been modified outside
# of the program by someone else, the logger is appending data to the chosen filepath
# and not overwriting it.
class Logger:
    ## Constructor
    # Input: filepath as string to the path+name of the file to log.
    def __init__(self, filepath):
        self.filepath = filepath
        self.last_time = 0
        self.updateLastTime()

    ## outputs an Event class type object to a file.
    # Input: ev as Event
    def output2file(self,ev):
        try:
            self.checkChange()

            f = open(self.filepath, "a")
            f.write(str(ev)+"\n")
            
        except IOError:
            print 'ERROR [Logger-output2file]: file cannot be opened or file not found.'
        finally:
            f.close() # free resources
            self.updateLastTime()

    ## Read file lines from the file, each line can be converted
    ## into an event using an parser from string to event such as
    ## the 'Converter' class using 'decode' function.
    # Input: None.
    # Output: list (array) of lines strings representing events
    def inputFromFile(self):
        try:
            self.checkChange()

            f = open(self.filepath, "r")
            lines = []
            for l in f:
                lines.append(l)

            return lines
        except:
            print 'ERROR [Logger-inputFromFile]: file cannot be opened or file not found.'
        finally:
            f.close()
            self.updateLastTime()

    ## Reads the file properties for last modified property,
    ## compares the time with the 'last_time' field of the object
    ## if the time do no match, then notifying to console on outside modification.
    ## on any case, updating the 'last_time' field of the object for further detections.
    # Input: None/
    # Output: True if file has been modified.
    #         False otherwise.
    def checkChange(self):
        try:
            last_modified = os.path.getmtime(self.filepath)
            if self.last_time < last_modified:
                print "\n----------------------------------------------------------------------------"
                print str(datetime.now())+" - DECTECTED AN UNAUTHURIZED MODIFICATION OF LOG FILES!"
                print "file: "+self.filepath
                print "----------------------------------------------------------------------------"
                return True
            return False
        except:
            pass
    

    ## Updating the field 'last_time' of the object with the
    ## last modified property of the file.
    def updateLastTime(self):
        try:
            self.last_time = os.path.getmtime(self.filepath)
        except:
            pass
            


## Converter Class used for encoding events to strings and decoding from string into event.
## Note: this class might be deprecated in later versions in favour of implementing it inside
## the Event class.
class Converter:
    def __init__(self):
        pass

    def decode(self, string):
        try:
            timeindex = string.index(' - ')
            timevalue = string[1:timeindex-1]
            timeobj   = datetime.strptime(timevalue, '%Y-%m-%d %H:%M:%S.%f')

            processNamesString  = string[timeindex+3:len(string)]
            processNamesList    = processNamesString.split(', ')
            processNamesList    = processNamesList[0:len(processNamesList)-1] 

            ev = Event('','',processNamesList)
            ev.setTime(timeobj)
            return ev
        except:
            pass

    def encode(self, event):
        return str(event)
                
