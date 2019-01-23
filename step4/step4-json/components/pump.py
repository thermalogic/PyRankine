
"""
Step4-json-dict: General Abstraction and Data Representation of Rankine Cycle 

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
            "ef": 1.00,
            "inNode":5,
            "outNode":6
        }

  Last updated: 2018.05.08
  Author:Cheng Maohua  Email: cmh@seu.edu.cn               

"""
from .node import *


class Pump():

    energy = "workRequired"
    devTYPE = "PUMP"

    def __init__(self, dictDev):
        """
        Initializes the pump with the conditions
        """
        self.name = dictDev['name']
        self.inNode = dictDev['inNode']
        self.outNode = dictDev['outNode']
        self.type = dictDev['type']
        self.ef = dictDev['ef'] 

        # add nodes
        self.nodes = [self.inNode, self.outNode]

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
        result += '\n' + Node.title
        result += '\n' + nodes[self.inNode].__str__()
        result += '\n' + nodes[self.outNode].__str__()

        result += '\nworkRequired(kJ/kg): \t%.2f' % self.workRequired
        result += '\nWRequired(MW): \t%.2f' % self.WRequired
        return result
