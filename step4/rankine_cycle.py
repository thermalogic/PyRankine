# -*- coding: utf-8 -*-
"""

Main Module of the General Simulator of Rankine Cycle 
   
    1 RankineCycle: the class of Rankine Cycle 

    2 SimRankineCycle: the simulator of Rankine Cycle 
  
Last updated: 2017.05.05

Author:Cheng Maohua  Email: cmh@seu.edu.cn

"""
import sys
import numpy as np

from components.node import Node
from components.boiler import Boiler
from components.openedheater import Openedheater
from components.turbine import Turbine
from components.condenser import Condenser
from components.pump import Pump

# for running python through CMD in VS code under windows only
import win_unicode_console
win_unicode_console.enable()

def read_nodesfile(filename):
    """ csvfile：node's info in the file"""
    countNodes = len(open(filename, 'r').readlines()) - 1
    nodes = [None for i in range(countNodes)]

    ndsFile = open(filename, 'r')
    discardHeader = ndsFile.readline()
    for line in ndsFile:
        NAME, NID, p, t, x, fdot = line.split(',')
        i = int(NID)
        nodes[i] = Node(NAME, i)
        try:
            nodes[i].p = float(p)
        except:
            nodes[i].p = None
        try:
            nodes[i].t = float(t)
        except:
            nodes[i].t = None
        try:
            nodes[i].x = float(x)
        except:
            nodes[i].x = None
        try:
            nodes[i].fdot = float(fdot)
        except:
            nodes[i].fdot = None

        if nodes[i].p != None and nodes[i].t != None:
            nodes[i].pt()
        elif nodes[i].p != None and nodes[i].x != None:
            nodes[i].px()
        elif nodes[i].t != None and nodes[i].x != None:
            nodes[i].tx()

    ndsFile.close()
    return nodes, countNodes


def read_devicefile(filename):
    devFile = open(filename, 'r')
    discardHeader = devFile.readline()
    Comps = {}
    i = 0
    begId = 3
    for line in devFile:
        dev = line.split(',')

        if dev[1] == "TURBINE-EX1":
            Comps[dev[0]] = Turbine(dev[0], int(dev[begId]),  int(
                dev[begId + 1]), int(dev[begId + 2]), ef=float(dev[2]))
        elif dev[1] == "TURBINE-EX0":
            Comps[dev[0]] = Turbine(dev[0], int(
                dev[begId]),  int(dev[begId + 1]), ef=float(dev[2]))
        elif dev[1] == "BOILER":
            Comps[dev[0]] = Boiler(
                dev[0], int(dev[begId]), int(dev[begId + 1]))
        elif dev[1] == "CONDENSER":
            Comps[dev[0]] = Condenser(
                dev[0], int(dev[begId]), int(dev[begId + 1]))
        elif dev[1] == "PUMP":
            Comps[dev[0]] = Pump(dev[0], int(
                dev[begId]),  int(dev[begId + 1]), ef=float(dev[2]))
        elif dev[1] == "OH-FEEDWATER-DW0":
            Comps[dev[0]] = Openedheater(dev[0], int(
                dev[begId]), int(dev[begId + 1]), int(dev[begId + 2]))

        i = i + 1

    devFile.close()

    DevNum = i
    return Comps, DevNum


class RankineCycle(object):

    def __init__(self, name):
        """
          self.nodes : list of all nodes
          self.Comps : dict of all components
        """
        self.name = name
        self.nodes = []
        self.Comps = {}
        self.NodehNum = 0
        self.DevNum = 0
        self.totalworkExtracted = 0
        self.totalworkRequired = 0
        self.totalWExtracted = 0
        self.totalWRequired = 0

        self.totalheatAdded = 0
        self.totalQAdded = 0

        self.netpoweroutput = 0
        self.efficiency = 100.0

        self.mdot = None
        self.Wcycledot = None

        self.fdotok = False

    def addNodes(self, filename):
        self.nodes, self.NodeNum = read_nodesfile(filename)

    def addComponent(self, filename):
        self.Comps, self.DevNum = read_devicefile(filename)

    def componentState(self):
        for key in self.Comps:
            self.Comps[key].state(self.nodes)

    def cycleFdot(self):

        i = 0
        while (self.fdotok == False):
            curfdotok = True
            for key in self.Comps:
                self.Comps[key].fdot(self.nodes)
                curfdotok = curfdotok and self.Comps[key].fdotok

            i = i + 1
            if (i > 20 or curfdotok == True):
                self.fdotok = True

    def cycleSimulator(self):
        for key in self.Comps:
            self.Comps[key].simulate(self.nodes)

        self.totalworkExtracted = 0
        self.totalworkRequired = 0
        self.totalheatAdded = 0
        for key in self.Comps:
            self.Comps[key].simulate(self.nodes)
            if self.Comps[key].energy == "workExtracted":
                self.totalworkExtracted += self.Comps[key].workExtracted
            if self.Comps[key].energy == "workRequired":
                self.totalworkRequired += self.Comps[key].workRequired
            if self.Comps[key].energy == "heatAdded":
                self.totalheatAdded += self. Comps[key].heatAdded

        self.netpoweroutput = self.totalworkExtracted - self.totalworkRequired
        self.efficiency = 100.0 * self.netpoweroutput / self.totalheatAdded
        self.HeatRate = 3600.0 / (self.efficiency * 0.01)
        self.SteamRate = self.HeatRate / self.totalheatAdded

    def SpecifiedNetOutputPowerSimulator(self, Wcycledot):
        self.Wcycledot = Wcycledot
        self.mdot = self.Wcycledot * self.SteamRate * 1000.0

        for i in range(self.NodeNum):
            self.nodes[i].calmdot(self.mdot)

        self.totalWExtracted = 0
        self.totalWRequired = 0
        self.totalQAdded = 0
        for key in self.Comps:
            self.Comps[key].sm_energy(self.nodes)
            if self.Comps[key].energy == "workExtracted":
                self.totalWExtracted += self.Comps[key].WExtracted
            if self.Comps[key].energy == "workRequired":
                self.totalWRequired += self.Comps[key].WRequired
            if self.Comps[key].energy == "heatAdded":
                self.totalQAdded += self. Comps[key].QAdded

    def SpecifiedMassFlowSimulator(self, mdot):
        self.mdot = mdot
        self.Wcycledot = self.mdot * self.netpoweroutput / (1000.0 * 3600.0)

        for i in range(self.NodeNum):
            self.nodes[i].calmdot(self.mdot)

        self.totalWExtracted = 0
        self.totalWRequired = 0
        self.totalQAdded = 0
        for key in self.Comps:
            self.Comps[key].sm_energy(self.nodes)
            if self.Comps[key].energy == "workExtracted":
                self.totalWExtracted += self.Comps[key].WExtracted
            if self.Comps[key].energy == "workRequired":
                self.totalWRequired += self.Comps[key].WRequired
            if self.Comps[key].energy == "heatAdded":
                self.totalQAdded += self. Comps[key].QAdded

    def OutFiles(self, outfilename=None):
        savedStdout = sys.stdout
        if (outfilename != None):
            datafile = open(outfilename, 'w', encoding='utf-8')
            sys.stdout = datafile

        print("\n  \t%s" % self.name)
        print("{:>20} {:>.2f}".format('Net Power(MW)', self.Wcycledot))
        print("{:>20} {:>.2f}".format('Mass Flow(kg/h)', self.mdot))
        print("{:>20} {:>.2f}".format('Efficiency(%)', self.efficiency))
        print("{:>20} {:>.2f}".format('Heat Rate(kJ/kWh)', self.HeatRate))
        print("{:>20} {:>.2f}".format('Steam Rate(kg/kWh)', self.SteamRate))

        print("{:>20} {:>.2f}".format(
            'totalWExtracted(MW)', self.totalWExtracted))
        print("{:>20} {:>.2f}".format(
            'totalWRequired(MW)', self.totalWRequired))
        print("{:>20} {:>.2f} \n".format('totalQAdded(MW)', self.totalQAdded))

        # output nodes    
        print(Node.nodetitle)
        for node in self.nodes:
            print(node)
        # output devices    
        for key in self.Comps:
            print(self.Comps[key].export(self.nodes))

        if (outfilename != None):
            datafile.close()
            sys.stdout = savedStdout


class SimRankineCycle(object):

    def __init__(self, nodes_filesname, dev_filesname):
        self.nodes_filesname = nodes_filesname
        self.dev_filesname = dev_filesname
        self.cyclename = nodes_filesname[0:nodes_filesname.find('-')]

    def CycleSimulator(self):
        self.cycle = RankineCycle(self.cyclename)
        self.cycle.addNodes(self.nodes_filesname)
        self.cycle.addComponent(self.dev_filesname)
        self.cycle.componentState()
        self.cycle.cycleFdot()
        self.cycle.cycleSimulator()

    def SpecifiedNetOutputPowerSimulatorAndOutput(self, Wcycledot):
        """ Specified Net Output Power"""
        self.cycle.SpecifiedNetOutputPowerSimulator(Wcycledot)
        # output
        self.cycle.OutFiles()
        self.cycle.OutFiles(self.cyclename + '-SP.txt')

    def SpecifiedMassFlowSimulatorAndOutput(self, mdot):
        """ Specified Mass Flow"""
        self.cycle.SpecifiedMassFlowSimulator(mdot)
        # output
        self.cycle.OutFiles()
        self.cycle.OutFiles(self.cyclename + '-SM.txt')
