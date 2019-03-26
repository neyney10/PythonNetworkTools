from datetime import datetime # for getting current time
import processmanager

class Event:
    # constructor
    def __init__(self,msg):
        self.message=msg
        self.time=str(datetime.now())

    def getMessage(self, newMsg):
        return self.message

    def setMessage(self, newMsg):
        self.message=newMsg

    # getter of the time of event
    def getTime(self):
        return self.time

    def setTime(self,time):
        self.time=time

    def updateTime(self):
        self.time=str(datetime.now())
        


    def __str__(self): # to string
         string = "["+self.time+"] - "
         string += self.message

         return string

