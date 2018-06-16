"""
The General Simulator of Rankine Cycle

    Turbine class: 
       
        inNode inlet steam   
                 ┌────────┐
              ↓ ╱         │ 
               ┤          │
                ╲         │
                 └────────┤
                          ↓  outNode exhausted steam   
extracted steam  0    

json object example

    {
            "name": "Turbine1",
            "type": "TURBINE-EX0",
            "eff": 100,
            "inNode": 0,
            "outNode": 1
    },

  Last updated: 2017.05.05
  Author:Cheng Maohua  Email: cmh@seu.edu.cn

"""
import seuif97
from .node import *


class TurbineEx0(object):

    energy = 'workExtracted'
    devTYPE = 'TURBINE-EX0'

    def __init__(self, dictDev):
        self.name = dictDev['name']
        self.inNode = dictDev['inNode']
        self.outNode = dictDev['outNode']

        self.type = dictDev['type']

        self.ef = dictDev['eff'] / 100.0

        # add nodes
        self.nodes = [self.inNode, self.outNode]

        self.fdotok = False

    def state(self, nodes):
        if self.ef == 1.0:
            nodes[self.outNode].s = nodes[self.inNode].s
            nodes[self.outNode].ps()
        else:
            isoh = seuif97.ps2h(nodes[self.outNode].p, nodes[self.inNode].s)
            nodes[self.outNode].h = nodes[self.inNode].h - \
                self.ef * (nodes[self.inNode].h - isoh)
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
                nodes[self.outNode].fdot = nodes[self.inNode].fdot

                # modified self.fdotok
                self._fdotok_(nodes)

            except:
                self.fdotok = False

    def simulate(self, nodes):
        self.workExtracted = nodes[self.outNode].fdot * \
            (nodes[self.inNode].h - nodes[self.outNode].h)

    def sm_energy(self, nodes):
        # mdot，get WExtracted
        self.WExtracted = nodes[self.outNode].mdot * \
            (nodes[self.inNode].h - nodes[self.outNode].h)

        self.WExtracted /= (3600.0 * 1000.0)

    def export(self, nodes):
        result = '\n' + self.name
        result += '\n' + Node.title
        result += '\n' + nodes[self.inNode].__str__()
        result += '\n' + nodes[self.outNode].__str__()

        result += '\nworkExtracted(kJ/kg): \t%.2f \nWExtracted(MW): \t%.2f' % (
            self.workExtracted, self.WExtracted)
        return result
