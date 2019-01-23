"""
Step5: The General Simulator of Rankine Cycle with the  base class of components

    TurbineEx0 class: 
       
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
            "ef": 1.0,
            "inNode": 0,
            "outNode": 1
    },

   Author:Cheng Maohua  Email: cmh@seu.edu.cn

"""
import seuif97
from .node import *
from .BComponent import BComponent


class TurbineEx0(BComponent):

    energy = 'workExtracted'
    devTYPE = 'TURBINE-EX0'

    def __init__(self, dictDev):
        super().__init__(dictDev)

        self.name = dictDev['name']
        self.inNode = dictDev['inNode']
        self.outNode = dictDev['outNode']
        self.type = dictDev['type']
        self.ef = dictDev['ef'] 

        # add nodes
        self.nodes = [self.inNode, self.outNode]
    

    def state(self, nodes):
        if self.ef == 1.0:
            nodes[self.outNode].s = nodes[self.inNode].s
            nodes[self.outNode].ps()
        else:
            isoh = seuif97.ps2h(nodes[self.outNode].p, nodes[self.inNode].s)
            nodes[self.outNode].h = nodes[self.inNode].h - \
                self.ef * (nodes[self.inNode].h - isoh)
            nodes[self.outNode].ph()

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
        result=super().export(nodes)
     
        result += '\nworkExtracted(kJ/kg): \t%.2f \nWExtracted(MW): \t%.2f' % (
            self.workExtracted, self.WExtracted)
        return result
