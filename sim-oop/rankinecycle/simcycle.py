"""
General Object-oriented Abstraction and JSON Textual Model of Rankine Cycle 

SimRankineCycle: The Simulator of Rankine Cycle 

Input and Output are data files

   - input: json file  

   - output: txt and json file
 
Last updated: 2018.05.10

Author:Cheng Maohua  Email: cmh@seu.edu.cn

"""

from .objcycle import *
from .iocycle import create_dictcycle_from_jsonfile,OutFiles,OutToJSONFiles

class SimRankineCycle:

    def __init__(self, rankinefilename):
        self.prefixResultFileName = (
            rankinefilename[0:-5]).replace("txtcycle", "output")  # -5 remove .json
        self.idictcycle =create_dictcycle_from_jsonfile(rankinefilename)
        self.cycle = RankineCycle(self.idictcycle)

    def CycleSimulator(self):
        self.cycle.simulator()
  
    def CycleSpecifiedSimulator(self, SetPower=None,SetMass=None):
        # Specified Simulating
        self.cycle.SpecifiedSimulator(SetPower,SetMass)
        self.cycle.CycleResultDict()
        
        # for output to files
        if SetPower!=None:
           outprefix= self.prefixResultFileName + '-sp'
        else:
           outprefix= self.prefixResultFileName + '-sm'
        # output to text
        OutFiles(self.cycle)
        OutFiles(self.cycle,outprefix+ '.txt')
        
        # output to json 
        OutToJSONFiles(self.cycle.odictcycle,outprefix+ '.json')

    
