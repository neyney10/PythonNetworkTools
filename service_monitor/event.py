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
        self.message = ''
        for sname in self.services:
            self.message += sname+", "
        

    def __str__(self): # to string
        string = "["+str(self.time)+"] - "
        string += self.header
        string += self.message
        string += self.footer

        return string

