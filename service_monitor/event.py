from datetime import datetime # for getting current time
import processmanager

class Event: 
    # constructor
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

