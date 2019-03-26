import psutil # dependency - process management
# Documentation of psutil: https://psutil.readthedocs.io/en/latest/#processes
from pprint import pprint as pp

# source:
# https://thispointer.com/python-check-if-a-process-is-running-by-name-and-find-its-process-id-pid/
def findProcessIdByName(processName):
    '''
    Get a list of all the PIDs of a all the running process whose name contains
    the given string processName
    '''
 
    listOfProcessObjects = []
 
    #Iterate over the all the running process
    for proc in psutil.process_iter():
       try:
           pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
           # Check if process name contains the given name string.
           if processName.lower() in pinfo['name'].lower() :
               listOfProcessObjects.append(pinfo)
       except (psutil.NoSuchProcess, psutil.AccessDenied , psutil.ZombieProcess) :
           pass
 
    return listOfProcessObjects

def getProcessByID(proc_id):
    try:
        proc = psutil.Process(proc_id)
        return proc
    except (psutil.NoSuchProcess):
        print 'error: no such process exists'

def printAllRunningProcesses():
    names = getAllRunningProccessNames()
    for n in names:
        print n

def getAllRunningPID():
    return psutil.pids()

def getAllRunningProccessNames():
    process_ids = getAllRunningPID()
    names = []

    for proc_id in process_ids:
        try:
            proc = psutil.Process(proc_id)
            names.append(proc.name())
        except (psutil.NoSuchProcess):
           pass
    return names

def test():
    print pp([(p.pid, p.info) for p in psutil.process_iter(attrs=['name','status']) if p.info['status'] == psutil.STATUS_RUNNING])


        
