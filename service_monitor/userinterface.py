
import sys # for exit
import re # Regular expressions
from cmd import Cmd # Guide: https://wiki.python.org/moin/CmdModule
from monitor import ProcessMonitor
from logger import Converter
import diff
from datetime import datetime,timedelta

class CLI2(Cmd,object):
    
    # cmd fields
    prompt = '[Monitor]> '
    intro = 'Using CLI Version-1.0, enter "help" for commands, supports auto-complete on linux with tab.'

    def __init__(self):
        super(CLI2,self).__init__()
        self.time = 7
        self.monitor = ProcessMonitor(self.time)
        self.monitor.start()

        self.cmdloop()


    def do_diff(self, args):
        # should get 4 args, arg0=date1, arg1=time1, arg2=date2, arg3=time2

        dates = self.parse(args)
        if len(dates) != 4:
            print '-> Invalid arguments [Err:1]: Please enter 2 date and times for two seperate events! '
            return

        date1 = (dates[0] +' '+ dates[1])
        date2 = (dates[2] +' '+ dates[3])
        try:
            d1 = try_parsing_date(date1)
            d2 = try_parsing_date(date2)
        except:
            print '-> Invalid arguments [Err:2]: Please enter 2 date and times for two seperate events!'
            return

        conv = Converter()

        mdelta = timedelta(seconds=3) # max delta to compare with

        ev1 = None
        ev2 = None
        events_strings = self.monitor.loggerServices.inputFromFile()
        for ev_str in events_strings:
            ev_date = ev_str[1:27]
            dd = datetime.strptime(ev_date, '%Y-%m-%d %H:%M:%S.%f')

            if ev_date == (date1) or abs(dd-d1)<mdelta:
                ev1 = conv.decode(ev_str)
            
            if ev_date == (date2) or abs(dd-d2)<mdelta:
                ev2 = conv.decode(ev_str)
        
        if ev1 == None or ev2 == None:
            print '-> Events not found for given two dates and times, try to be more precise.'
            return
        
        started_services,closed_services = diff.diffset(ev1.getServices(),ev2.getServices())
        
        if len(started_services) > 0:
            print '<New Services:>'
            print started_services

        if len(closed_services) > 0:
            print '<Stopped Services:>'
            print closed_services

        if len(closed_services) == 0 and len(started_services) == 0:
            print 'There are no changes.'

    def help_diff(self):
        print 'Show difference between two events with given dates and times.'
        print '<------> Syntax: diff <date1> <time1> <date2> <time2>'
        print '<-> Where \'date\' is of the syntax: YYYY-MM-DD, e.g 2019-03-27'
        print '<-> \'time\' is of the syntax: HH:mm:ss.nnnnnn, e.g 21:43:45.707000'
        print '<-> Example:'
        print '<------> diff 2019-03-27 21:43:45.707000 2019-03-27 15:43:33.207000'

    def do_interval(self, arg):
        if arg:
            try:
                time = int(arg)
                if time <= 4:
                    print '-> Invalid argument [Err:1]: Time interval between scans cannot be negative or zero, must be positive greater than 4 (in seconds)  '
                    return

                self.monitor.interval = time
                print 'Interval between scans has changed to '+str(time)+' seconds.'
            except:
                print '-> Invalid argument [Err:2]: Please enter time as an integer (in seconds)  '
        else:
            print 'The interval between scans is '+ str(self.monitor.interval)+' seconds.'
        

    def do_EOF(self, line):
        return True


    def parse(self, cmdString):
        cmdString = re.sub(' +',' ',cmdString)
        inputs = cmdString.split(' ')

        return inputs
    

# source: 
# https://stackoverflow.com/questions/23581128/how-to-format-date-string-via-multiple-formats-in-python/40800072
# Input: text string of a datetime.
# Output: datetime object created from the string.
def try_parsing_date(text):
    for fmt in ('%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M'):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass
    raise ValueError('no valid date format found')