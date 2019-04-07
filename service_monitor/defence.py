import os
from datetime import datetime
from threading import Thread # for threading.
import time # for sleep
## Defensive function and classes

## Static class
## File monitor detects unauthurized changes in files.()
class File_Monitor():
    filepaths = {}
    active_monitor = False
    running_monitor = False # feedback from the thread


    ## Class for activly checking file modification using a different
    ## thread.
    class Active_File_Monitoring(Thread):
        def __init__(self):
            super(File_Monitor.Active_File_Monitoring, self).__init__()

        def run(self):
            while File_Monitor.active_monitor:
                for key in File_Monitor.filepaths.keys():
                    File_Monitor.checkChange(key)
                    File_Monitor.updateLastTime(key)
                time.sleep(5)
            File_Monitor.running_monitor = True
            


    ## function which starts an active monitoring in different thread
    @staticmethod
    def activate_active_monitoring():
        if File_Monitor.active_monitor or File_Monitor.running_monitor:
            return
        
        File_Monitor.running_monitor = True
        File_Monitor.active_monitor = True
        monitor = File_Monitor.Active_File_Monitoring()
        monitor.start()

    ## function which stops an active monitoring.
    @staticmethod
    def deactivate_active_monitoring():
        File_Monitor.active_monitor = False


    ## Reads the file properties for last modified property,
    ## compares the time with the 'last_time' field of the object
    ## if the time do no match, then notifying to console on outside modification.
    ## on any case, updating the 'last_time' field of the object for further detections.
    # Input: None
    # Output: True if file has been modified.
    #         False otherwise.
    @staticmethod
    def checkChange(filepath):
        try:
            last_modified = os.path.getmtime(filepath)
            if File_Monitor.filepaths[filepath] < last_modified:
                print "\n----------------------------------------------------------------------------"
                print str(datetime.now())+" - DECTECTED AN UNAUTHURIZED MODIFICATION OF LOG FILES!"
                print "file: "+filepath
                print "----------------------------------------------------------------------------"
                return True
            return False
        except:
            pass
    

    ## Updating the field 'last_time' of the object with the
    ## last modified property of the file.
    @staticmethod
    def updateLastTime(filepath):
        try:
            File_Monitor.filepaths[filepath] = os.path.getmtime(filepath)
        except:
            pass