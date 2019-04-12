"""
Step4-json-dict: General Abstraction and Data Representation of Rankine Cycle 

class Openedheaterdw0

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


class OpenedheaterDw0(object):

    energy = 'internel'
    devTYPE = "FWH-OPENDED-DW0"

    def __init__(self, dictDev):
        """
        Initializes the Opened feedwater with the conditions
        """
        self.name = dictDev['name']
        self.type = dictDev['type']
        self.inNode = dictDev['inNode']
        self.inNode_fw = dictDev['inNode_fw']
        self.outNode_fw = dictDev['outNode_fw']
    
        self.heatAdded = 0
        self.heatExtracted = 0
        self.QExtracted = 0

        # add nodes
        self.nodes = [self.inNode, self.inNode_fw, self.outNode_fw]
        self.fdotok = False

    def state(self, nodes):
        pass

    def _fdotok_(self, nodes):
        self.fdotok = nodes[self.nodes[0]].fdot != None
        for node in range(1, len(self.nodes)):
            self.fdotok = self.fdotok and (nodes[node].fdot != None)

    def fdot(self, nodes):
        """ the initial condition: the fraction of outNode_fw flow is known """
        if (self.fdotok == False):
            try:
                if (nodes[self.outNode_fw].fdot != None):
                    # energy blance equation
                    self.heatAdded = nodes[self.outNode_fw].fdot * \
                        (nodes[self.outNode_fw].h - nodes[self.inNode_fw].h)

                    self.heatExtracted = self.heatAdded

                    nodes[self.inNode].fdot = self.heatExtracted / \
                        (nodes[self.inNode].h - nodes[self.inNode_fw].h)
                    # mass blance equation
                    nodes[self.inNode_fw].fdot = nodes[self.outNode_fw].fdot - \
                        nodes[self.inNode].fdot

                # check self.fdotok
                self._fdotok_(nodes)
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
        result += '\n' + Node.title
        result += '\n' + nodes[self.inNode].__str__()
        result += '\n' + nodes[self.inNode_fw].__str__()
        result += '\n' + nodes[self.outNode_fw].__str__()

        result += '\nheatAdded(kJ/kg) \t{:>.2f}'.format(self.heatAdded)
        result += '\nheatExtracted(kJ/kg) \t{:>.2f}'.format(self.heatExtracted)
        result += '\nQAdded(MW) \t{:>.2f}'.format(self.QAdded)
        result += '\nQExtracted(MW)  \t{:>.2f}'.format(self.QExtracted)
        return result
