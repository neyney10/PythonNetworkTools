from threading import Thread # for threading.
import processmanager
from logger import Converter, Logger
import time # for sleep
from event import Event
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
        self.converter = Converter()
        self.loggerServices = Logger('./serv')
        self.loggerStatus = Logger('./log')
        self.processes = set()
        self.print_mode = False
        
    ## overriding Run method of Thread.
    ## the function runs an infinite loop and sampling the systen services,
    ## logging them into files, and notify the user on console on any changes.
    def run(self):
        # print 'ProcessMonitor thread is started...'
        while 1:
            processesTemp = processmanager.getAllRunningServices()
            ev = Event('','',processesTemp)
            self.loggerServices.output2file(ev)

            if len(self.processes)>0:
                d = diff.diffset(self.processes,processesTemp)
                if len(d[0])>0:
                    ev = Event('<<--New Services:-->> [',']',d[0])
                    self.loggerStatus.output2file(ev)
                    if self.print_mode:
                        print ev
                if len(d[1])>0:
                    ev = Event('<<--Stopped Services:-->> [',']',d[1])
                    self.loggerStatus.output2file(ev)
                    if self.print_mode:
                        print ev

            self.processes = processesTemp
            time.sleep(self.interval)




