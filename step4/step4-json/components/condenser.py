
"""
Step4-json: General Abstraction and Data Representation of Rankine Cycle 

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

   Last updated: 2018.05.08

   Author:Cheng Maohua  Email: cmh@seu.edu.cn                   

"""

from .node import *


class Condenser:

    energy = "heatExtracted"
    devTYPE="CONDENSER"

    def __init__(self, name, inNode, outNode):
        """ Initializes the condenser """
        self.name = name
        self.inNode = inNode
        self.outNode = outNode
        self.typeStr = 'CONDENSER'
     
        self.fdotok = False

    def state(self, Nodes):
        pass

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
        """  Simulates the Condenser  """
        self.heatExtracted = nodes[self.inNode].fdot * \
            (nodes[self.inNode].h - nodes[self.outNode].h)

    def sm_energy(self, nodes):
        self.QExtracted = nodes[self.inNode].mdot * \
            (nodes[self.inNode].h - nodes[self.outNode].h)
        self.QExtracted /= (3600.0 * 1000.0)

    def export(self, nodes):
        result = '\n' + self.name
        result += '\n' + Node.nodetitle
        result += '\n' + nodes[self.inNode].__str__()
        result += '\n' + nodes[self.outNode].__str__()
        result += '\nheatExtracted(kJ/kg)  \t%.2f \nQExtracted(MW): \t%.2f' % (
            self.heatExtracted, self.QExtracted)
        return result
