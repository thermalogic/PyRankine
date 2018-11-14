"""
Step4-json-dict: General Abstraction and Data Representation of Rankine Cycle 

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

 Last updated: 2018.05.10

 Author:Cheng Maohua  Email: cmh@seu.edu.cn 

"""

from .node import *


class Boiler(object):

    energy = "heatAdded"
    devTYPE = "BOILER"

    def __init__(self, dictDev):
        """
        Initializes the boiler
        """
        # self.__dict__.update(dictDev)

        self.name = dictDev['name']
        self.inNode = dictDev['inNode']
        self.outNode = dictDev['outNode']
        self.type = dictDev['type']
        # add nodes
        self.nodes = [self.inNode, self.outNode]
        self.fdotok = False

    def state(self, nodes):
        pass

    # add _fdotok_
    def _fdotok_(self, nodes):
        self.fdotok = nodes[self.nodes[0]].fdot != None
        for node in range(1, len(self.nodes)):
            self.fdotok = self.fdotok and (nodes[node].fdot != None)

    def fdot(self, nodes):
        if (self.fdotok == False):
            try:
                # mass blance equation
                if (nodes[self.inNode].fdot != None):
                    nodes[self.outNode].fdot = nodes[self.inNode].fdot
                elif (nodes[self.outNode].fdot != None):
                    nodes[self.inNode].fdot = nodes[self.outNode].fdot

                # modified self.fdotok
                self._fdotok_(nodes)
            except:
                self.fdotok == False

    def simulate(self, nodes):
        self.heatAdded = nodes[self.inNode].fdot * \
            (nodes[self.outNode].h - nodes[self.inNode].h)

    def sm_energy(self, nodes):
        self.QAdded = nodes[self.inNode].mdot * \
            (nodes[self.outNode].h - nodes[self.inNode].h)
        self.QAdded /= (3600.0 * 1000.0)

    def export(self, nodes):
        result = '\n' + self.name
        result += '\n' + Node.title
        result += '\n' + nodes[self.inNode].__str__()
        result += '\n' + nodes[self.outNode].__str__()
        result += '\nheatAdded(kJ/kg) \t%.2f \nQAdded(MW) \t%.2f' % (
            self.heatAdded, self.QAdded)
        return result
