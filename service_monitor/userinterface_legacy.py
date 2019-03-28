import sys # for exit
import re
from cmd import Cmd
from monitor import ProcessMonitor
from logger import Converter
import diff

class CLI:
    def __init__(self):
        self.state = menuState()
        print self.state.getOptionsString()#temp
        self.run() # temp
    
    def run(self):
        while 1:
            userinput = str(raw_input('monitor->>>'))
            parsedinput = self.parse(userinput)
            self.state.executeCommand(parsedinput)
    
    def parse(self, cmdString):
        cmdString = re.sub(' +',' ',cmdString)
        inputs = cmdString.split(' ')

        inputs[len(inputs)-1] = inputs[len(inputs)-1][:-1]
        return inputs

        

    


class Command:
    def __init__(self,name):
        self.name = name

    def getName(self):
        return self.name
    
    def execute(self,state,args):
        pass


class settimeCMD(Command,object):
    def __init__(self):
        super(settimeCMD,self).__init__('interval')

    def execute(self,state,args):
        pass # TODO

class diffCMD(Command,object):
    def __init__(self):
        super(diffCMD,self).__init__('diff')

    def execute(self,state,args):
        pass # TODO

class showCMD(Command,object):
    def __init__(self):
        super(showCMD,self).__init__('show')

    def execute(self,state,args):
        print state.getOptionsString()

class exitCMD(Command,object):
    def __init__(self):
        super(exitCMD,self).__init__('exit')

    def execute(self,state,args):
        try:
            sys.exit()
        except:
            print 'ERROR: cannot exit '



# using the State-Machine design pattern
class State:
    def __init__(self,name):
        self.name=name
        self.commands = [exitCMD(), showCMD()]

    def getOptionsString(self):
        pass

    def findCommand(self, inputcmd):
        cmdStringName = inputcmd[0]
       
        for cmd in self.commands:
            cmdName = cmd.getName()
            if cmdStringName == cmdName:
                return cmd

    def executeCommand(self, inputcmd):
        cmd = self.findCommand(inputcmd)
        if cmd:
            cmd.execute(self,inputcmd)
        else:
            errmsg = "the command %s not found" %(inputcmd[0])
            print errmsg

# main menu state
class menuState(State,object):
    def __init__(self):
         super(menuState,self).__init__('mainmenu')
        
         
    def getOptionsString(self):
        s =  "1- Show all options (this menu)\n"
        s += "2- view changes between 2 events from service list file\n"
        s += "3- Edit monitor update interval\n"

        return s


