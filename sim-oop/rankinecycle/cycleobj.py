"""
 General Object-oriented Abstraction and JSON Textual Model of Rankine Cycle 

RankineCycle: the class of Rankine Cycle  Simulator

dictcycle={"name":namestring,
                     "nodes":[dict1,dict2,...],
                     "comps":[dict1,dict2,...]
                     }
  
Author:Cheng Maohua  Email: cmh@seu.edu.cn

"""

import time

from components.node import Node
from components import compdict


class RankineCycle:

    def __init__(self, dictcycle):
        """
          dictcycle={"name":namestring,
                     "nodes":[dict1,dict2,...],
                     "comps":[dict1,dict2,...]
                     }
          TO:           
             self.nodes : list of all node objects
             self.comps : dict of all component objects
        """
        self.name = dictcycle["name"]
        dictnodes = dictcycle["nodes"]
        dictcomps = dictcycle["comps"]

        # 1 convert dict to the object of nodes
        self.NodeNum = len(dictnodes)
        self.nodes = [None for i in range(self.NodeNum)]
        for curnode in dictnodes:
            self.nodes[int(curnode['id'])] = Node(curnode)

        # 2 convert dict to the object of Comps
        self.DevNum = len(dictcomps)
        self.comps = {}
        for curdev in dictcomps:
            self.comps[curdev['name']] = compdict[curdev['type']](
                curdev, self.nodes)

        self.totalworkExtracted = 0
        self.totalworkRequired = 0
        self.totalheatAdded = 0

        self.netpoweroutput = 0
        self.efficiency = 100.0
        self.HeatRate = 0.0
        self.SteamRate = 0.0

        self.mdot = None
        self.Wcycledot = None

        self.totalWExtracted = 0
        self.totalWRequired = 0
        self.totalQAdded = 0

    def ComponentState(self):
        for key in self.comps:
            self.comps[key].state()

    def ComponentBalance(self):
        keys = list(self.comps.keys())
        deviceok = False

        i = 0  # i: the count of deviceok to avoid endless loop
        while (deviceok == False and i <= self.DevNum):

            for curdev in keys:
                try:
                    self.comps[curdev].balance()
                    keys.remove(curdev)
                except:
                    pass

            i += 1
            if (len(keys) == 0):
                deviceok = True

        # for debug: check the failed devices
        if (len(keys) > 0):
            print(keys)

    def simulator(self):
        self.ComponentState()
        self.ComponentBalance()

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

        self.netpoweroutput = self.totalworkExtracted - self.totalworkRequired
        self.efficiency = self.netpoweroutput / self.totalheatAdded
        self.HeatRate = 3600.0 / self.efficiency
        self.SteamRate = self.HeatRate / self.totalheatAdded

    def SpecifiedSimulator(self, SetPower=None, SetMass=None):
        if SetPower != None:
            self.Wcycledot = SetPower
            self.mdot = self.Wcycledot * self.SteamRate * 1000.0
        else:
            self.mdot = SetMass
            self.Wcycledot = self.mdot * \
                self.netpoweroutput / (1000.0 * 3600.0)

        for i in range(self.NodeNum):
            self.nodes[i].calmdot(self.mdot)

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

    def __setformatstr(self, formatstr, result):
        result += formatstr.format('Net Power(MW)', self.Wcycledot)
        result += formatstr.format('Mass Flow(kg/h)', self.mdot)
        result += formatstr.format('Cycle Efficiency(%)',
                                   self.efficiency*100.0)
        result += formatstr.format('Cycle Heat Rate(kJ/kWh)', self.HeatRate)
        result += formatstr.format('Steam Rate(kg/kWh)', self.SteamRate)
        result += formatstr.format('totalWExtracted(MW)', self.totalWExtracted)
        result += formatstr.format('totalWRequired(MW)', self.totalWRequired)
        result += formatstr.format('totalQAdded(MW)', self.totalQAdded)
        return result

    def __str__(self):
        str_curtime = time.strftime(
            "%Y/%m/%d %H:%M:%S", time.localtime(time.time()))
        result = "\n Rankine Cycle: {}, Time: {}\n".format(
            self.name, str_curtime)
        try:
            formatstr = "{:>20} {:>.2f}\n"
            result = self.__setformatstr(formatstr, result)
        except:
            formatstr = "{} {}\n"
            result = self.__setformatstr(formatstr, result)
        return result
