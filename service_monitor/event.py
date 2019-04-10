from datetime import datetime # for getting current time
import processmanager

##### Event class ######
# An event is an object which stores all the event info about a service scan,
# can be added with additional text such as text head, text foot and time of date in order to
# make the event ready to be converted into string for it to be stored
# on a file.
class Event: 
    ## Constructor
    # Input: head - as a string, the text which preceeds the service set in the string.
    #        foot - as a string, the text which follows the service set in the string.
    #        serv_set - python Set, which contains all services on current scan event.
    def __init__(self,head,foot,serv_set):
        self.message = ''
        self.changed = True

        if head:
            self.header = head
        else:
            self.header = ''
        if foot:
            self.footer=foot
        else:
            self.footer=''
        if len(serv_set) > 0:
            self.setServices(serv_set)
        else:
            self.services = set()

        self.time=datetime.now()

    @classmethod
    def fromString(cls, string):
        try:
            timeindex = string.index(' - ')
            timevalue = string[1:timeindex-1]
            timeobj   = datetime.strptime(timevalue, '%Y-%m-%d %H:%M:%S.%f')

            processNamesString  = string[timeindex+3:len(string)]
            processNamesList    = processNamesString.split(', ')
            processNamesList    = processNamesList[0:len(processNamesList)-1] 

            ev = cls('','',processNamesList) #Event('','',processNamesList)
            ev.setTime(timeobj)
            return ev
        except:
            pass


    def getHeader(self):
        return self.header

    def setHeader(self, newHeader):
        self.header=newHeader
        
    def getFooter(self):
        return self.header

    def setFooter(self, newFooter):
        self.footer=newFooter

    # getter of the time of event
    def getTime(self):
        return self.time

    def setTime(self,time):
        self.time=time

    def updateTime(self):
        self.time=datetime.now()
        
    def getServices(self):
        return self.services
        
    def setServices(self,serv_set):
        self.services = set(serv_set)
        self.changed = True

    def construct_message(self):
        self.message = ''
        for sname in self.services:
            self.message += sname+", "
        self.changed = False
        

    def __str__(self): # to string
        if self.changed:
            self.construct_message()
        string = "["+str(self.time)+"] - "
        string += self.header
        string += self.message
        string += self.footer

        return string






class Event_Log(Event, object): 
    ## Constructor
    # Input: head - as a string, the text which preceeds the service set in the string.
    #        foot - as a string, the text which follows the service set in the string.
    #        serv_set - python Set, which contains all services on current scan event.
    def __init__(self,head,foot,serv_set,stop_set):
        super(Event_Log,self).__init__(head,foot,serv_set)
        self.stopped_services = set()
        if stop_set and len(stop_set):
            self.setStoppedServices(stop_set)


    @classmethod
    def fromString(cls, string):
        try:
            timeindex = string.index(' - ')
            timevalue = string[1:timeindex-1]
            timeobj   = datetime.strptime(timevalue, '%Y-%m-%d %H:%M:%S.%f')

            processNamesString  = string[timeindex+3:len(string)]
            newProcNamesList = []
            try:
                newservindex_s     = processNamesString.index('[')
                newservindex_e     = processNamesString.index(']')
                newProcNamesString = processNamesString[newservindex_s+1:newservindex_e-1]
                newProcNamesList   = newProcNamesString.split(', ')
                newProcNamesList   = newProcNamesList[0:len(newProcNamesList)]
            except:
                print 'error 1'

            stopProcNamesList = []
            try:
                processNamesString  = processNamesString[len(newProcNamesList):len(processNamesString)]
                stopservindex_s     = processNamesString.rindex('[')
                stopservindex_e     = processNamesString.rindex(']')
                stopProcNamesString = processNamesString[stopservindex_s+1:stopservindex_e-1]
                stopProcNamesList   = stopProcNamesString.split(', ')
                stopProcNamesList   = stopProcNamesList[0:len(stopProcNamesList)]
            except:
                print 'error 2'



            ev = cls('','',newProcNamesList,stopProcNamesList) #Event('','',processNamesList)
            ev.setTime(timeobj)
            return ev
        except:
            pass

    def getStoppedServices(self):
        return self.stopped_services

    def setStoppedServices(self,stop_set):
        self.stopped_services = set(stop_set)
        self.changed = True
    

    def construct_message(self):
        self.message = 'New: ['
        for sname in self.services:
            self.message += sname+", "
        
        self.message += '] Stopped: ['

        if len(self.stopped_services) > 0:
            for sname2 in self.stopped_services:
                self.message += sname2+", "

        self.message += ']'
        self.changed = False
        
    def __str__(self): # to string
        if self.changed:
            self.construct_message()
        string = "["+str(self.time)+"] - "
        string += self.header
        string += self.message
        string += self.footer

        return string


    
    
    