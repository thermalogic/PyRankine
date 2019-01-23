"""
Step5: The General Simulator of Rankine Cycle with the  base class of components

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

  Author:Cheng Maohua  Email: cmh@seu.edu.cn  

"""
from .node import *
from .BComponent import BComponent

class OpenedheaterDw0(BComponent):

    energy = 'internel'
    devTYPE = "FWH-OPENDED-DW0"

    def __init__(self, dictDev):
        """
        Initializes the Opened feedwater with the conditions
        """
        super().__init__(dictDev)

        self.name = dictDev['name']
        self.type = dictDev['type']
        self.inNode = dictDev['inNode']
        self.inNode_fw = dictDev['inNode_fw']
        self.outNode_fw = dictDev['outNode_fw']
     
        # add nodes
        self.nodes = [self.inNode, self.inNode_fw, self.outNode_fw]
        
        self.heatAdded=0
        self.heatExtracted = 0
        self.QExtracted = 0

    def state(self, nodes):
        pass

    def fdot(self, nodes):
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

                # modified self.fdotok
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
        result=super().export(nodes)
        result += '\nheatAdded(kJ/kg) \t%.2f' % self.heatAdded
        result += '\nheatExtracted(kJ/kg) \t%.2f' % self.heatExtracted
        result += '\nQAdded(MW) \t%.2f' % self.QAdded
        result += '\nQExtracted(MW)  \t%.2f' % self.QExtracted
        return result
