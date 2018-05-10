"""
The General Simulator of Rankine Cycle 

class Openedheater

                    ↓   inNode extracted steam
                ┌───┴───┐
 feedwater      │       │
 outNode_fw   ← ┤       │← inNode_fw  feedwater
                │       │
                └───────┘  
 
 json object example:

     {
            "name": "Opened Feedwater Heater",
            "type": "OH-FEEDWATER-DW0",
            "inNode":1,
            "inNode_fw":4,
            "outNode_fw":5
     }

  Last updated: 2018.05.08

  Author:Cheng Maohua  Email: cmh@seu.edu.cn  

"""
from .node import *


class Openedheater:
  
    energy = 'internel'
    devTYPE="OH-FEEDWATER-DW0"
    
    def __init__(self,dictDev):
        """
        Initializes the Opened feedwater with the conditions
        """
        self.name = dictDev['name']
        self.inNode = dictDev['inNode']
        self.inNode_fw = dictDev['inNode_fw']
        self.outNode_fw = dictDev['outNode_fw']

        self.heatExtracted = 0
        self.QExtracted = 0

        self.typeStr = dictDev['type']
      

        self.fdotok = False

    def state(self, nodes):
        pass

    def fdot(self, nodes):
        if (self.fdotok == False):
            try:
                if (nodes[self.outNode_fw].fdot != None):
                    self.heatAdded = nodes[self.outNode_fw].fdot * \
                        (nodes[self.outNode_fw].h - nodes[self.inNode_fw].h)
                    self.heatExtracted = self.heatAdded
                    nodes[self.inNode].fdot = self.heatExtracted / \
                        (nodes[self.inNode].h - nodes[self.inNode_fw].h)
                    nodes[self.inNode_fw].fdot = nodes[self.outNode_fw].fdot - nodes[self.inNode].fdot

                self.fdotok = (nodes[self.outNode_fw].fdot != None)
                self.fdotok = self.fdotok and (nodes[self.inNode_fw].fdot != None)
                self.fdotok = self.fdotok and (nodes[self.inNode].fdot != None)
            except:
                self.fdotok = False

    def simulate(self, nodes):
        """
        Simulates the opened feedwater heater  
        """
        self.heatAdded = nodes[self.outNode_fw].fdot * \
            (nodes[self.outNode_fw].h - nodes[self.inNode_fw].h)
        self.heatExtracted = self.heatAdded

    def sm_energy(self, nodes):
        self.QExtracted = nodes[self.inNode].mdot * \
            (nodes[self.inNode].h - nodes[self.inNode_fw].h)
        self.QExtracted /= (3600.0 * 1000.0)
        self.QAdded = self.QExtracted

    def export(self, nodes):
        result = '\n' + self.name
        result += '\n' + Node.nodetitle
        result += '\n' + nodes[self.inNode].__str__()
        result += '\n' + nodes[self.inNode_fw].__str__()
        result += '\n' + nodes[self.outNode_fw].__str__()

        result += '\nheatAdded(kJ/kg) \t%.2f' % self.heatAdded
        result += '\nheatExtracted(kJ/kg) \t%.2f' % self.heatExtracted
        result += '\nQAdded(MW) \t%.2f' % self.QAdded
        result += '\nQExtracted(MW)  \t%.2f' % self.QExtracted
        return result
