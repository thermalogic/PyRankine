
"""
Step5: The General Simulator of Rankine Cycle with the  base class of components

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
            "ef": 1.0,
            "inNode":5,
            "outNode":6
        }

Author:Cheng Maohua(cmh@seu.edu.cn)              

"""
from .node import *
from .BComponent import BComponent

class Pump(BComponent):

    energy = "workRequired"
    devTYPE = "PUMP"

    def __init__(self, dictDev):
        """
        Initializes the pump with the conditions
        """
        super().__init__(dictDev)
       
        self.name = dictDev['name']
        self.type = dictDev['type']
        self.inNode = dictDev['inNode']
        self.outNode = dictDev['outNode']
        self.ef = dictDev['ef'] 

        # add nodes
        self.nodes = [self.inNode, self.outNode]

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
        super().fdot(nodes)

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
        result=super().export(nodes)
        result += '\nworkRequired(kJ/kg): \t%.2f' % self.workRequired
        result += '\nWRequired(MW): \t%.2f' % self.WRequired
        return result
