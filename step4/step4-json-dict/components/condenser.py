
"""
The General Simulator of Rankine Cycle 

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


class Condenser(object):

    energy = "heatExtracted"
    devTYPE="CONDENSER"

    def __init__(self,dictDev):
        """ Initializes the condenser """
        self.name =  dictDev['name']
        self.inNode = dictDev['inNode']
        self.outNode = dictDev['outNode']
        self.type = dictDev['type']
         # add nodes 
        self.nodes=[self.inNode, self.outNode]
     
        self.fdotok = False

    def state(self, Nodes):
        pass

     # add _fdotok_
    def _fdotok_(self, nodes):
        self.fdotok = nodes[self.nodes[0]].fdot != None
        for node in range(1, len(self.nodes)):
            self.fdotok = self.fdotok and (nodes[node].fdot != None)

    def fdot(self, nodes):
        if (self.fdotok == False):
            try:
                if (nodes[self.inNode].fdot != None):
                    nodes[self.outNode].fdot = nodes[self.inNode].fdot
                elif (nodes[self.outNode].fdot != None):
                    nodes[self.inNode].fdot = nodes[self.outNode].fdot
               
                # modified self.fdotok
                self._fdotok_(nodes)
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
        result += '\n' + Node.title
        result += '\n' + nodes[self.inNode].__str__()
        result += '\n' + nodes[self.outNode].__str__()
        result += '\nheatExtracted(kJ/kg)  \t%.2f \nQExtracted(MW): \t%.2f' % (
            self.heatExtracted, self.QExtracted)
        return result
