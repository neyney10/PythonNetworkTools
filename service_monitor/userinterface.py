
import sys # for exit
import re # Regular expressions
from cmd import Cmd # Guide: https://wiki.python.org/moin/CmdModule
from monitor import ServiceMonitor
import diff
from event import Event, Event_Log
from datetime import datetime,timedelta

## CLI2 Class is an improvement of the lagacy CLI class.
## the class inherit the Cmd class of the standard python 2.7 package
## meant for CLIs, the CLI2 is going on infinite IO loop at init.
class CLI2(Cmd,object):
    
    # cmd fields
    prompt = '[manual]> '
    intro = 'Using CLI Version-1.0, enter "help" for commands, supports auto-complete on linux with tab.'


    ## Constructor
    # Starting a new thread of ServiceMonitor
    # and entering a CLI input loop.
    # defaulting scanning interval time to 7 seconds.
    def __init__(self):
        super(CLI2,self).__init__()
        self.time = 7
        self.monitor = ServiceMonitor(self.time)
        #self.monitor.start()
        self.modes = {"manual": [self.mode_enter_manual,self.mode_exit_manual],
                    "monitor": [self.mode_enter_monitor,self.mode_exit_monitor]} # add here for more modes
        
        self.current_mode = self.modes.keys()[0]
        self.cmdloop()


    ## [CLI-Command] switch
    ## by getting a mode as a string the function switches
    ## to that mode.
    def do_switch(self, args):
        mode_req = self.parse(args)
        if len(mode_req) != 1: # if there arent 4 arguments, do not continue.
            print '-> Invalid arguments [Err:1]: Please enter a mode such as "manual" or "monitor".'
            return
        for mode in self.modes:
            if mode == mode_req[0]:
                mode_req_info = self.modes.get(mode)
                current_mode_info = self.modes.get(self.current_mode)
                current_mode_info[1]() # activate exiting function
                mode_req_info[0]() # activate entering function
                self.current_mode = mode
                self.change_prompt(self.current_mode)
                print 'Entered into '+self.current_mode+' mode.'
                return

        print '-> Invalid arguments [Err:2]: unknown mode.'

     ## CLI-Help command to print command description
    def help_switch(self):
        print 'Switch to a different mode.'
        print '<------> Syntax: switch <mode>'
        print '<-> Avilable modes: ',
        for mode in self.modes:
            print mode,
        print ''
        print '<-> Example:'
        print '<------> switch '+self.modes.keys()[0]

    ## [CLI-Command] diff
    ## by getting 4 arguments of date and times, the function
    ## prints the difference between those two events.
    def do_diff(self, args):
        if self.current_mode != "manual":
            print '-> must be in manual mode to use the "diff" function.'
            return

        # should get 4 args, arg0=date1, arg1=time1, arg2=date2, arg3=time2
        dates = self.parse(args)

        if '-log' in dates:
            dates.remove('-log')
            self.diffg(dates)
            return

        if len(dates) != 4: # if there arent 4 arguments, do not continue.
            print '-> Invalid arguments [Err:1]: Please enter 2 date and times for two seperate events! '
            return

        date1 = (dates[0] +' '+ dates[1]) # construct a string from Time argument and Date argument
        date2 = (dates[2] +' '+ dates[3]) # construct a string from Time argument and Date argument
        try: # try to convert those strings into a 'datetime' objects.
            d1 = try_parsing_date(date1)
            d2 = try_parsing_date(date2)
        except: # upon failure to parse those strings to datetime objects, do not contrinue.
            print '-> Invalid arguments [Err:2]: Please enter 2 date and times for two seperate events!'
            return

        #conv = Converter() # used to parse each line of the file into an event - legacy

        mdelta = timedelta(seconds=3) # max delta to compare with

        ev1 = None # the event corresponds to the first datetime obj
        ev2 = None # the event corresponds to the second datetime obj
        events_strings = self.monitor.loggerServices.inputFromFile() # read file lines into list
        for ev_str in events_strings: # for each line in the list
            ev_date = ev_str[1:27] # get the datetime as a string.
            dd = try_parsing_date(ev_date) # parse it and store is a 'dd' variable.

            if ev_date == (date1) or abs(dd-d1)<mdelta:
                ev1 = Event.fromString(ev_str) #conv.decode(ev_str) - legacy
            
            if ev_date == (date2) or abs(dd-d2)<mdelta:
                ev2 = Event.fromString(ev_str) #conv.decode(ev_str) -legacy
        
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

    ## CLI-Help command to print command description
    def help_diff(self):
        print 'Show difference between two events with given dates and times.'
        print 'Additional options flags: -log (shows all events between two dates and times from status log file)'
        print '<------> Syntax: diff <date1> <time1> <date2> <time2>'
        print '<-> Where \'date\' is of the syntax: YYYY-MM-DD, e.g 2019-03-27'
        print '<-> \'time\' is of the syntax: HH:mm:ss.nnnnnn, e.g 21:43:45.707000'
        print '<-> Example:'
        print '<------> diff 2019-03-27 21:43:45.707000 2019-03-27 15:43:33.207000'


    ## temp
    def diffg(self,dates):
        date1 = (dates[0] +' '+ dates[1]) # construct a string from Time argument and Date argument
        date2 = (dates[2] +' '+ dates[3]) # construct a string from Time argument and Date argument
        try: # try to convert those strings into a 'datetime' objects.
            d1 = try_parsing_date(date1)
            d2 = try_parsing_date(date2)
        except: # upon failure to parse those strings to datetime objects, do not contrinue.
            print '-> Invalid arguments [Err:2]: Please enter 2 date and times for two seperate events!'
            return

        mdelta = timedelta(seconds=3) # max delta to compare with

        foundev1 = False
        ev1 = None # the event corresponds to the first datetime obj
        ev2 = None # the event corresponds to the second datetime obj
        events_strings = self.monitor.loggerStatus.inputFromFile() # read file lines into list
        for ev_str in events_strings: # for each line in the list
            ev_date = ev_str[1:27] # get the datetime as a string.
            try:
                dd = try_parsing_date(ev_date) # parse it and store is a 'dd' variable.
            except:
                pass


            if not foundev1 and ev_date == (date1) or abs(dd-d1)<mdelta:
                ev1 = Event_Log.fromString(ev_str) #conv.decode(ev_str) - legacy
                print ev1
                foundev1 = True

            if foundev1:
                if not abs(dd-d2)<mdelta:
                    ev2 = Event_Log.fromString(ev_str)
                    print ev2
                else:
                    try:
                        ev2 = Event_Log.fromString(ev_str)
                        print ev2
                    except:
                        pass
                    return

 
    
    ## CLI-Command function 'interval', used to show current interval configuration and 
    ## modify it.
    def do_interval(self, arg):
        if self.current_mode != "manual":
            print '-> must be in manual mode to use the "interval" function.'
            return

        if arg:
            try:
                time = int(arg)
                if time <= 4:
                    print '-> Invalid argument [Err:1]: Time interval between scans cannot be negative or zero, must be positive greater than 4 (in seconds)  '
                    return

                self.time = time
                self.monitor.interval = time
                print 'Interval between scans has changed to '+str(time)+' seconds.'
            except:
                print '-> Invalid argument [Err:2]: Please enter time as an integer (in seconds)  '
        else:
            print 'The interval between scans is '+ str(self.monitor.interval)+' seconds.'
        
    ## CLI-Help command to print command description
    def help_interval(self):
        print 'Show and Configure interval time between scans (in seconds)'
        print '<> Show current interval time.'
        print '<------> Syntax: interval'
        print '<> Change interval time'
        print '<------> Syntax: interval <number>'
        print '<-> Where <number> is an integer greater than 4.'
        print '<-> Example:'
        print '<------> interval 60'

    ## CMD's built-in function.
    def do_EOF(self, line):
        return True

    ## function that get executed when entering manual mode
    def mode_enter_manual(self):
        pass

    ## function that get executed when exiting manual mode
    def mode_exit_manual(self):
        pass

    ## function that get executed when entering monitor mode
    def mode_enter_monitor(self):
        self.monitor = ServiceMonitor(self.time)
        self.monitor.print_mode = True    
        self.monitor.start()   

    ## function that get executed when exiting monitor mode
    def mode_exit_monitor(self):
        self.monitor.print_mode = False     
        self.monitor.stop()


    ## parser - parse a string line into a list of arguments
    # Input: cmdString - as text string.
    # Output: list of string arguments parsed from the input string.
    def parse(self, cmdString):
        cmdString = re.sub(' +',' ',cmdString)
        inputs = cmdString.split(' ')

        return inputs

    ## changes prompt test
    # Input: text as a string.
    # Output: none.
    def change_prompt(self,text):
        self.prompt = '['+text+']> '
    

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