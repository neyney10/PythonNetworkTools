from threading import Thread # for threading.
import processmanager
from logger import *
import time # for sleep
from event import Event
import diff
import os

####################### Class Description: ####################### 
# process monitor class ia a class which monitors the processes on 
# the host computer and logs them to a file using the "Logger" class from logger.py.
# The class extends 'Thread' and by is sampleling the processes on the computer every
# time interval which supplied at the constructor (in seconds).
class ProcessMonitor(Thread):
    def __init__(self, interval):
        super(ProcessMonitor, self).__init__()
        self.interval = interval # time interval between scans, by seconds for now
        self.converter = Converter()
        self.loggerServices = Logger('./serv')
        self.loggerStatus = Logger('./log')
        self.processes = []
        

    def run(self):
        print 'ProcessMonitor thread is started...'
        while 1:
            processesTemp = processmanager.getAllRunningProccessNames()
            ev = self.converter.encode(processesTemp)
            self.loggerServices.output2file(ev)

            if len(self.processes)>0:
                d = diff.difflist(self.processes,processesTemp)
                if len(d)>0:
                    ev = self.converter.encode(d)
                    self.loggerStatus.output2file(ev)
                    print d

            self.processes = processesTemp
            time.sleep(self.interval)



    def add(self,proc):
        self.processes.append(proc)
        print 'added a new process to monitoring list' #temp
