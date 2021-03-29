"""
 General Object-oriented Abstraction of Rankine Cycle 

* Sequential-modular(SM)：

    def simulator_sm(self):
        self.component_analysis_sm("STATE")
        self.component_analysis_sm("BALANCE")

* equation-oriented(EO)： 

    def simulator_eo(self):
        self.component_state_eo()
        self.cycle_equation_eo()
        self.cycle_simulator_eo()
"""

import time
from platform import os
import getpass
import numpy as np

from components.port import Port
from components.connector import Connector
from components import compdict

class RankineCycle:

    def __init__(self, dictcycle):
        """
          dictcycle={"name":namestring,
                     "etam":1,
                     "etag":1,
                     "components":[{component1},{component2},...],
                     "connectors":[((name1,port1),(name2,port2)),...]
                  }
          TO:     
             self.comps : dict of all component objects      
             self.curcon : the connector object
        """
        self.name = dictcycle["name"]
        if ("etam" in dictcycle and "etag" in dictcycle):
            self.etam =float(dictcycle["etam"])
            self.etag =float(dictcycle["etag"])
        else:
           self.etam=1.00
           self.etag = 1.00

        dictcomps = dictcycle["components"]
        listconnectors = dictcycle["connectors"]

        # 1 convert dict to the dict of device objects: {device name:device obiect}
        self.DevNum = len(dictcomps)
        self.comps = {}
        for curdev in dictcomps:
            self.comps[curdev['name']] = compdict[curdev['devtype']](curdev)

        self.curcon=Connector()
        # 2 use the dictconnectors to set the nodes value and alias between the item of nodes and the port of devices
        for tupconnector in listconnectors:
            self.curcon.AddConnector(tupconnector, self.comps)

        self.totalworkExtracted = 0
        self.totalworkRequired = 0
        self.totalheatAdded = 0

        self.netpoweroutput = 0
       
        # Specified 
        self.Specified = False

        self.mdot = None
        self.Wcycledot = None
       
        self.totalWExtracted = 0
        self.totalWRequired = 0
        self.totalQAdded = 0

    # sequential-modular approach
    def component_analysis_sm(self, funstr):
        keys = list(self.comps.keys())
        deviceok = False

        i = 0  # i: the count of deviceok to avoid endless loop
        while (deviceok == False and i <= self.DevNum):

            for curdev in keys:
                try:
                    if funstr == "STATE":
                        self.comps[curdev].state()
                    elif funstr == "BALANCE":
                        self.comps[curdev].balance()
                    keys.remove(curdev)
                except:
                    pass

            i += 1
            if (len(keys) == 0):
                deviceok = True

        # for debug: check the failed devices
        if (len(keys) > 0):
            print("--- " + funstr + " -- the failed devices:", keys)

    
    #  equation-oriented approach
    def equation_eo(self):
        connum=len(self.curcon.nodes)
        self.A = np.zeros((connum, connum))
        self.b = np.zeros(connum)
        
        currow=0
        for key in self.comps:
            self.comps[key].equation_rows()
            for row in self.comps[key].rows:
                for col in row["a"]:
                     self.A[currow, col[0]] = col[1]
                self.b[currow]=row["b"]
                #print(key,self.A[currow],self.b[currow])
                currow += 1  
   
        fdot = np.linalg.solve(self.A, self.b)

        #print(" ---------  solution of fraction: fdot -----------")
        #print(fdot)
        
        for i in range(len(self.curcon.nodes)):
            self.curcon.nodes[i][0].fdot = fdot[i]
   
    # sequential-modular approach
    def simulator_sm(self):
        self.component_analysis_sm("STATE")
        self.component_analysis_sm("BALANCE")

    #  equation-oriented approach
    def simulator_eo(self):
        self.component_analysis_sm("STATE") 
        self.equation_eo()
        for key in self.comps:
            self.comps[key].energy_fdot()
 
    def simulator_performance(self):
        self.totalworkExtracted = 0
        self.totalworkRequired = 0
        self.totalheatAdded = 0

        for key in self.comps:
            if self.comps[key].energy == "workExtracted":
                self.totalworkExtracted += self.comps[key].workExtracted
            elif self.comps[key].energy == "workRequired":
                self.totalworkRequired += self.comps[key].workRequired
            elif self.comps[key].energy == "heatAdded":
                self.totalheatAdded += self.comps[key].heatAdded
        
        # 1 循环 cycle efficiency
        self.efficiency_cycle = self.totalworkExtracted / self.totalheatAdded
        # 2 发电  power generation 
        self.poweroutput = self.totalworkExtracted*self.etam *self.etag
        self.efficiency_power_generation = self.efficiency_cycle*self.etam*self.etag
        self.HeatRate_power_generation = 3600.0 / self.efficiency_power_generation
        self.SteamRate_power_generation = self.HeatRate_power_generation / self.totalheatAdded
        # 3 供电 Power supply 
        self.netpoweroutput = self.totalworkExtracted*self.etam * \
               self.etag - self.totalworkRequired
        self.efficiency_power_supply = self.netpoweroutput/self.totalheatAdded
        self.HeatRate_power_supply = 3600.0 / self.efficiency_power_supply
        self.SteamRate_power_supply = self.HeatRate_power_supply / self.totalheatAdded

  
    def specified_simulator(self, set_power=None, set_mass=None):
        if set_power != None:
            self.SpecifiedStr = "\n--- Specified  Power Generation---\n"
            self.Wcycledot = set_power
            self.mdot = self.Wcycledot * self.SteamRate_power_generation * 1000.0
        else:
            self.SpecifiedStr = "\n--- Specified  Mass ---\n"
            self.mdot = set_mass
        
        # mdot计算：两种情况
        # 1 设备之间连接点端口mdot计算
        for item in self.curcon.nodes:
            item[0].calmdot(self.mdot)
        # 2 非设备之间连接点端口mdot计算,这些端口fdot给定，如sg
        for key in self.comps:
            self.comps[key].calmdot(self.mdot)
      
        self.totalWExtracted = 0
        self.totalWRequired = 0
        self.totalQAdded = 0
        for key in self.comps:
            self.comps[key].sm_energy()
            if self.comps[key].energy == "workExtracted":
                self.totalWExtracted += self.comps[key].WExtracted
            elif self.comps[key].energy == "workRequired":
                self.totalWRequired += self.comps[key].WRequired
            elif self.comps[key].energy == "heatAdded":
                self.totalQAdded += self.comps[key].QAdded
     
        self.netWExtracted = self.totalWExtracted *self.etam*self.etag
        if set_mass is not None:
           self.Wcycledot=self.netWExtracted
       
        self.Specified=True;       

    def __set_formatstr(self, formatstr, result):
        result += formatstr.format('The Cycle Efficiency(%): ',
                                   self.efficiency_cycle*100.0)
        result += formatstr.format('etam(%): ', self.etam*100.0)
        result += formatstr.format('etag(%): ', self.etag*100.0)
        result += formatstr.format('The Power Generation Efficiency(%): ',
                                   self.efficiency_power_generation*100.0)
        result += formatstr.format('The Power Generation Heat Rate(kJ/kWh): ',
                                   self.HeatRate_power_generation)
        result += formatstr.format('The Power Generation Steam Rate(kg/kWh): ',
                                   self.SteamRate_power_generation)
        result += formatstr.format('The Power Supply Efficiency(%): ',self.efficiency_power_supply*100.0)
        result += formatstr.format('The Power Supply Heat Rate(kJ/kWh): ',
                                   self.HeatRate_power_supply)
        result += formatstr.format('The Power Generation Steam Rate(kg/kWh): ',
                                   self.SteamRate_power_supply)        
        
        result +="\n--- 1kg ---\n"
        result += formatstr.format('totalheatAddedd(kJ/kg): ',
                                   self.totalheatAdded)
        result += formatstr.format('totalworkExtracted(kJ/kg): ', self.totalworkExtracted)
        result += formatstr.format('totalworkRequired(kJ/kg): ', self.totalworkRequired)
        result += formatstr.format('Power generation poweroutput(kJ/kg): ',  self.poweroutput)
        result += formatstr.format('Power supply netpoweroutput(kJ/kg): ',
                                   self.netpoweroutput)
        return result
    
    def __set_specified_formatstr(self, formatstr, result):
        result += self.SpecifiedStr
        result += formatstr.format('Power(MW): ', self.Wcycledot)
        result += formatstr.format('Mass Flow(kg/h): ', self.mdot)
        result += formatstr.format('totalWExtracted(MW): ', self.totalWExtracted)
        result += formatstr.format('totalWRequired(MW): ', self.totalWRequired)
        result += formatstr.format('totalQAdded(MW): ', self.totalQAdded)
        result += formatstr.format('netWExtracted(MW): ', self.netWExtracted)
        return result


    def __str__(self):
        str_curtime = time.strftime(
            "%Y/%m/%d %H:%M:%S", time.localtime(time.time()))
        result = "\n Rankine Cycle: {}, Time: {}\n".format(
            self.name, str_curtime)
        try:
            formatstr = "\t{:>20} {:>.2f}\n"
            result = self.__set_formatstr(formatstr, result)
        except:
            formatstr = "\t{} {}\n"
            result = self.__set_formatstr(formatstr, result)
        
        if self.Specified:
            try:
                formatstr = "\t{:>20} {:>.2f}\n"
                result = self.__set_specified_formatstr(formatstr, result)
            except:
                formatstr = "\t{} {}\n"
                result = self.__set_specified_formatstr(formatstr, result)

        return result
