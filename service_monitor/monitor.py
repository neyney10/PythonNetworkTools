from threading import Thread # for threading.
import processmanager
from logger import Logger
import time # for sleep
from event import Event, Event_Log
import diff


####################### Class Description: ####################### 
# process monitor class ia a class which monitors the processes on 
# the host computer and logs them to a file using the "Logger" class from logger.py.
# The class extends 'Thread' and by is sampleling the processes on the computer every
# time interval which supplied at the constructor (in seconds).
class ServiceMonitor(Thread):
    def __init__(self, interval):
        super(ServiceMonitor, self).__init__()
        self.interval = interval # time interval between scans, by seconds for now
        self.loggerServices = Logger('./serviceList.txt')
        self.loggerStatus = Logger('./Status_Log.txt')
        self.processes = set()
        self.print_mode = False
        self.isstopping = False
        
    def stop(self):
        self.isstopping = True

    ## overriding Run method of Thread.
    ## the function runs an infinite loop and sampling the systen services,
    ## logging them into files, and notify the user on console on any changes.
    def run(self):
        # print 'ProcessMonitor thread is started...'
        while not self.isstopping:
            processesTemp = processmanager.getAllRunningServices()
            ev = Event('','',processesTemp)
            self.loggerServices.output2file(ev)

            if len(self.processes)>0:
                d = diff.diffset(self.processes,processesTemp)
                if len(d[0])>0 or len(d[1])>0:
                    evlog = Event_Log('','',d[0],d[1])
                    self.loggerStatus.output2file(evlog)
                    if self.print_mode:
                        print evlog

            self.processes = processesTemp
            time.sleep(self.interval)




