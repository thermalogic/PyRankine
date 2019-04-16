"""
Step4-json-dict: General Abstraction and Data Representation of Rankine Cycle 

    TurbineEx1 class: 
       
        inNode inlet steam   
                 ┌────────┐
              ↓ ╱         │ 
               ┤          │
                ╲         │
                 └──┬─────┤
          extNode   ↓     ↓  outNode exhausted steam   
extracted steam     1    

json object example

     {
            "name": "Turbine1",
            "type": "TURBINE-EX1",
            "ef": 0.85,
            "inNode": 0,
            "outNode": 2,
            "extNode": 1
      } 

  Last updated: 2017.05.05
  Author:Cheng Maohua  Email: cmh@seu.edu.cn

"""
import seuif97
from .node import *


class TurbineEx1(object):

    energy = 'workExtracted'
    devTYPE = 'TURBINE-EX1'

    def __init__(self, dictDev):
        self.name = dictDev['name']
        self.type = dictDev['type']
        self.inNode = dictDev['inNode']
        self.outNode = dictDev['outNode']
        self.extNode = dictDev['extNode']
        self.ef = dictDev['ef'] 

        # add nodes
        self.nodes = [self.inNode, self.outNode, self.extNode]
        self.fdotok = False

    def state(self, nodes):
        if self.ef == 1.0:
            nodes[self.extNode].s = nodes[self.inNode].s
            nodes[self.extNode].ps()
            nodes[self.outNode].s = nodes[self.inNode].s
            nodes[self.outNode].ps()
        else:
            isoh = seuif97.ps2h(
                nodes[self.extNode].p, nodes[self.inNode].s)
            nodes[self.extNode].h = nodes[self.inNode].h - \
                self.ef * (nodes[self.inNode].h - isoh)
            nodes[self.extNode].ph()

            isoh = seuif97.ps2h(
                nodes[self.outNode].p, nodes[self.extNode].s)
            nodes[self.outNode].h = nodes[self.extNode].h - \
                self.ef * (nodes[self.extNode].h - isoh)
            nodes[self.outNode].ph()

    def _fdotok_(self, nodes):
        self.fdotok = nodes[self.nodes[0]].fdot != None
        for node in range(1, len(self.nodes)):
            self.fdotok = self.fdotok and (nodes[node].fdot != None)

    def fdot(self, nodes):
        if (self.fdotok == False):
            try:
                # mass blance equation
                nodes[self.outNode].fdot = nodes[
                    self.inNode].fdot - nodes[self.extNode].fdot

                # check self.fdotok
                self._fdotok_(nodes)
            except:
                self.fdotok = False

    def simulate(self, nodes):
        self.workExtracted = nodes[self.extNode].fdot * \
            (nodes[self.inNode].h - nodes[self.extNode].h)

        self.workExtracted += nodes[self.outNode].fdot * \
            (nodes[self.inNode].h - nodes[self.outNode].h)

    def sm_energy(self, nodes):
        # mdot，get WExtracted
        self.WExtracted = nodes[self.extNode].mdot * \
            (nodes[self.inNode].h - nodes[self.extNode].h)

        self.WExtracted += nodes[self.outNode].mdot * \
            (nodes[self.inNode].h - nodes[self.outNode].h)

        self.WExtracted /= (3600.0 * 1000.0)

    def export(self, nodes):
        result = '\n' + self.name
        result += '\n' + Node.title
        result += '\n' + nodes[self.inNode].__str__()
        result += '\n' + nodes[self.outNode].__str__()

        result += '\n' + nodes[self.extNode].__str__()

        result += '\nworkExtracted(kJ/kg): \t{:>.2f} \nWExtracted(MW): \t{:>.2f}'.format(
            self.workExtracted, self.WExtracted)
        return result
