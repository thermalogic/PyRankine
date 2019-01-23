"""
Step5: The General Simulator of Rankine Cycle with the  base class of components

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

 
  Author:Cheng Maohua  Email: cmh@seu.edu.cn

"""
import seuif97
from .node import *
from .BComponent import BComponent


class TurbineEx1(BComponent):

    energy = 'workExtracted'
    devTYPE = 'TURBINE-EX1'

    def __init__(self, dictDev):
        super().__init__(dictDev)

        self.name = dictDev['name']
        self.type = dictDev['type']
        self.inNode = dictDev['inNode']
        self.outNode = dictDev['outNode']
        self.extNode = dictDev['extNode']
        self.ef = dictDev['ef']

        # add nodes
        self.nodes = [self.inNode, self.outNode, self.extNode]

    def state(self, nodes):
        if self.ef == 1.0:
            nodes[self.outNode].s = nodes[self.inNode].s
            nodes[self.outNode].ps()
        else:
            isoh = seuif97.ps2h(nodes[self.outNode].p, nodes[self.inNode].s)
            nodes[self.outNode].h = nodes[self.inNode].h - \
                self.ef * (nodes[self.inNode].h - isoh)
            nodes[self.outNode].ph()

        if self.ef == 1.0:
            nodes[self.extNode].s = nodes[self.inNode].s
            nodes[self.extNode].ps()
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

    def fdot(self, nodes):
        if (self.fdotok == False):
            try:
                # mass blance equation
                nodes[self.outNode].fdot = nodes[self.inNode].fdot - \
                    nodes[self.extNode].fdot

                # modified self.fdotok
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
        result = super().export(nodes)
        result += '\nworkExtracted(kJ/kg): \t%.2f \nWExtracted(MW): \t%.2f' % (
            self.workExtracted, self.WExtracted)
        return result
