
"""
Step5: The General Simulator of Rankine Cycle with the  base class of components

  class  Condenser 

                    ↓   inNode exhausted steam
                ┌───┴───┐
                │       │ 
                │       │
                │       │
                └───┬───┘  
                    ↓ outNode condensate water 
json object example:

   {
            "name": "Condenser",
            "type": "CONDENSER",
            "inNode": 2,
            "outNode": 3
   },                   

   Last updated: 2018.05.10
   Author:Cheng Maohua  Email: cmh@seu.edu.cn                   

"""

from .node import *
from .BComponent import BComponent


class Condenser(BComponent):

    energy = "heatExtracted"
    devTYPE = "CONDENSER"

    def __init__(self, dictDev):
        """ Initializes the condenser """
        # demo BComponent.__init_
        BComponent.__init__(self,dictDev)
        
        self.name = dictDev['name']
        self.inNode = dictDev['inNode']
        self.outNode = dictDev['outNode']
        self.type = dictDev['type']
        
        # add nodes
        self.nodes = [self.inNode, self.outNode]

    def state(self, Nodes):
        pass

    def fdot(self, nodes):
        # demo BComponent
        BComponent.fdot(self,nodes)

    def simulate(self, nodes):
        """  Simulates the Condenser  """
        self.heatExtracted = nodes[self.inNode].fdot * \
            (nodes[self.inNode].h - nodes[self.outNode].h)

    def sm_energy(self, nodes):
        self.QExtracted = nodes[self.inNode].mdot * \
            (nodes[self.inNode].h - nodes[self.outNode].h)
        self.QExtracted /= (3600.0 * 1000.0)

    def export(self, nodes):
        # demo BComponent
        result=BComponent.export(self,nodes)
        result += '\nheatExtracted(kJ/kg)  \t%.2f \nQExtracted(MW): \t%.2f' % (
            self.heatExtracted, self.QExtracted)
        return result
