import psutil # dependency - process management
# Documentation of psutil: https://psutil.readthedocs.io/en/latest/#processes
from subprocess import Popen, PIPE
import re

def getAllRunningServices():
    if psutil.WINDOWS:
        return getServicesWindows()
    
    if psutil.LINUX:
        return getServicesLinux()

def getServicesWindows(): # windows
    services = set()
    for p in psutil.win_service_iter():
        if p.status() == psutil.STATUS_RUNNING:
            services.add(p.name())

    return services

def getServicesLinux(): # linux, see:https://stackoverflow.com/questions/10405515/piping-in-shell-via-python-subprocess-module
    
    cmd1 = Popen(["service","--status-all"],stdout=PIPE,stderr=PIPE)
    cmd2 = Popen(["grep","+"],stdin=cmd1.stdout,stdout=PIPE,stderr=PIPE)

    cmd1.stdout.close()
    stdout = cmd2.communicate()[0]
    stdout = re.sub(' *','',stdout)
    stdout = re.sub('\[\+\]','',stdout)
        
    services = stdout.split('\n')
    return set(services[:-1])
