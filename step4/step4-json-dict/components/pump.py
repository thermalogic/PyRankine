
"""
The General Simulator of Rankine Cycle

    class Pump

                ┌───────┐
                │       │
    outNode   ← ┼───────┼← inNode
                │       │
                └───────┘  
 
  json object example:
     {
            "name": "Feedwater Pump",
            "type": "PUMP",
            "eff": 100,
            "inNode":5,
            "outNode":6
        }

  Last updated: 2018.05.08
  
  Author:Cheng Maohua  Email: cmh@seu.edu.cn               

"""
from .node import *


class Pump():
    
    energy = "workRequired"
    devTYPE="PUMP"

    def __init__(self,dictDev):
        """
        Initializes the pump with the conditions
        """
        self.name = dictDev['name']
        self.inNode = dictDev['inNode']
        self.outNode = dictDev['outNode']
        self.typeStr = dictDev['type']
     
        self.ef = dictDev['eff'] / 100.0

        self.fdotok = False

    def state(self, nodes):
        """
        calc outNode of the pump 
        """
        nodes[self.outNode].h = (
            nodes[self.inNode].h +
            (nodes[self.inNode].v * (nodes[self.outNode].p -
                                     nodes[self.inNode].p) * 1000.0) / self.ef
        )
        nodes[self.outNode].ph()

    def fdot(self, nodes):
        if (self.fdotok == False):
            try:
                if (nodes[self.inNode].fdot != None):
                    nodes[self.outNode].fdot = nodes[self.inNode].fdot
                elif (nodes[self.outNode].fdot != None):
                    nodes[self.inNode].fdot = nodes[self.outNode].fdot

                self.fdotok = nodes[self.outNode].fdot != None
                self.fdotok = self.fdotok and (nodes[self.inNode].fdot != None)
            except:
                self.fdotok == False

    def simulate(self, nodes):
        """
        Simulates the pump 
        """
        self.workRequired = nodes[self.inNode].fdot * \
            (nodes[self.outNode].h - nodes[self.inNode].h)

    def sm_energy(self, nodes):
        self.WRequired = nodes[self.inNode].mdot * \
            (nodes[self.outNode].h - nodes[self.inNode].h)
        self.WRequired /= (3600.0 * 1000.0)

    def export(self, nodes):
        result = '\n' + self.name
        result += '\n' + Node.nodetitle
        result += '\n' + nodes[self.inNode].__str__()
        result += '\n' + nodes[self.outNode].__str__()

        result += '\nworkRequired(kJ/kg): \t%.2f' % self.workRequired
        result += '\nWRequired(MW): \t%.2f' % self.WRequired
        return result
