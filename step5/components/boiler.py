"""
Step5: The General Simulator of Rankine Cycle with the  base class of components
  class Boiler

                    ↑    outNode main steam
                ┌───┼───┐
                │   │   │
                │   │   │
                │   │   │
                └───┼───┘  
                    ↑    inNode main feedwater   


 json object example:

        {    
            "name": "Boiler",  
            "type": "BOILER",
            "inNode": 6,
            "outNode": 0
        }

 Author:Cheng Maohua  Email: cmh@seu.edu.cn 

"""

from .node import *
from .BComponent import BComponent


class Boiler(BComponent):

    energy = "heatAdded"
    devTYPE = "BOILER"

    def __init__(self, dictDev):
        """
        Initializes the boiler
        """
        super().__init__(dictDev)

        self.name = dictDev['name']
        self.inNode = dictDev['inNode']
        self.outNode = dictDev['outNode']
        self.type = dictDev['type']

        # add nodes
        self.nodes = [self.inNode, self.outNode]
     
    def state(self, nodes):
        pass

    def fdot(self, nodes):
        super().fdot(nodes)

    def simulate(self, nodes):
        self.heatAdded = nodes[self.inNode].fdot * \
            (nodes[self.outNode].h - nodes[self.inNode].h)

    def sm_energy(self, nodes):
        self.QAdded = nodes[self.inNode].mdot * \
            (nodes[self.outNode].h - nodes[self.inNode].h)
        self.QAdded /= (3600.0 * 1000.0)

    def export(self, nodes):
        result=super().export(nodes)
        result += '\nheatAdded(kJ/kg) \t%.2f \nQAdded(MW) \t%.2f' % (
            self.heatAdded, self.QAdded)
        return  result
