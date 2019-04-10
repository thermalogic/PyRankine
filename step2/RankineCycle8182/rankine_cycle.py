import sys
import csv
import numpy as np

from boiler import *
from turbine import *
from pump import *
from condenser import *
from node import  *


def read_nodesfile(filename):
    """ csvfile：nodes:unorder in the file"""

    # get count of Nodes,init nodes[] with size in count
    countNodes = len(open(filename, 'r').readlines()) - 1
    nodes = [None for i in range(countNodes)]

    # put each node in nodes
    csvfile = open(filename, 'r')
    reader = csv.DictReader(csvfile)
    for line in reader:
        i = int(line['NID'])
        nodes[i] = Node(line['NAME'], i)
        try:
            nodes[i].p = float(line['p'])
        except:
            nodes[i].p = None
        try:
            nodes[i].t = float(line['t'])
        except:
            nodes[i].t = None
        try:
            nodes[i].x = float(line['x'])
        except:
            nodes[i].x = None

        if line['p'] != '' and line['t'] != '':
            nodes[i].pt()
        elif line['p'] != '' and line['x'] != '':
            nodes[i].px()
        elif line['t'] != '' and line['x'] != '':
            nodes[i].tx()

    csvfile.close()
    return nodes


compdict = {
    "BOILER": Boiler,
    "TURBINE-EX0": Turbine,
    "PUMP": Pump,
    "CONDENSER": Condenser
}


def read_devicefile(filename):
    csvfile = open(filename, 'r')
    reader = csv.DictReader(csvfile)
    Comps = {}
    for curdev in reader:
        minID = int(curdev['minID'])
        moutID = int(curdev['moutID'])
        try:
            eta = float(curdev['eta'])
            Comps[curdev['NAME']] = compdict[curdev['TYPE']](
                minID, moutID, eta)
        except:
            Comps[curdev['NAME']] = compdict[curdev['TYPE']](minID, moutID)
    csvfile.close()
    return Comps


class RankineCycle:

    def __init__(self, name):
        """
          self.nodes : list of all nodes
          self.Comps : dict of all components
        """
        self.name = name
        self.nodes = []
        self.Comps = {}
        self.totalworkExtracted = 0
        self.totalworkRequired = 0
        self.totalheatAdded = 0
        self.efficiency = 100.0

    def addNodes(self, filename):
        self.nodes = read_nodesfile(filename)

    def addComponent(self, filename):
        self.Comps = read_devicefile(filename)

    def cycleSimulator(self):
        for key in self.Comps:
            self.Comps[key].simulate(self.nodes)

            if self.Comps[key].energy == "workExtracted":
                self.totalworkExtracted += self.Comps[key].workExtracted
            elif self.Comps[key].energy == "workRequired":
                self.totalworkRequired += self.Comps[key].workRequired
            elif self.Comps[key].energy == "heatAdded":
                self.totalheatAdded += self.Comps[key].heatAdded

        self.efficiency = 100.0 * \
            (self.totalworkExtracted - self.totalworkRequired) / self.totalheatAdded

    def OutFiles(self, outfilename=None):
        savedStdout = sys.stdout
        if (outfilename != None):
            datafile = open(outfilename, 'w', encoding='utf-8')
            sys.stdout = datafile

        print("\n  \t%s" % self.name)
        print("{:>20} {:>.2f} {:1}".format(
            'Thermal efficiency:', self.efficiency, '%'))

        print(Node.title)
        for node in self.nodes:
            print(node)

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
        self.cycle.cycleSimulator()

    def SimulatorOutput(self):
        # output
        self.cycle.OutFiles()
        self.cycle.OutFiles(self.cyclename + '-sp.txt')
