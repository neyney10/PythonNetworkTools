from event import *
import os
####################### Class Description: ####################### 
# The Logger class is a class which handles all the output to files
class Logger:
    def __init__(self, filepath):
        self.filepath = filepath
        self.last_time = 0
        self.updateLastTime()
        print self.last_time



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

    def checkChange(self):
        try:
            last_modified = os.path.getmtime(self.filepath)
            if self.last_time < last_modified:
                print "\nCHANGED !!!!!!!!!! OMFG\n"#temp
                return True
            return False
        except:
            pass
    
    def updateLastTime(self):
        try:
            self.last_time = os.path.getmtime(self.filepath)
        except:
            pass
            


class Converter:
    def __init__(self):
        pass

    def decode(self, string):
        try:
            timeindex = string.index(' - ')
            timevalue = string[0:timeindex]
            processNamesString = string[timeindex+3:len(string)]
            processNamesList = processNamesString.split(', ')
            processNamesList = processNamesList[0:len(processNamesList)-1] 

            return processNamesList
        except:
            pass

    def encode(self, lst):
        string = ''
        for p in lst:
            if p:
                string+=p+", "

        return Event(string)
                
