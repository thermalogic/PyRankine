"""
The General Simulator of Rankine Cycle

    Turbine class: 
       
        inNode inlet steam   
                 ┌────────┐
              ↓ ╱         │ 
               ┤          │
                ╲         │
                 └──┬─────┤
          extNode   ↓     ↓  outNode exhausted steam   
extracted steam  (0/1)     

  Last updated: 2017.05.05
  
  Author:Cheng Maohua  Email: cmh@seu.edu.cn

"""
import seuif97
from .node import *


class Turbine(object):

    energy = 'workExtracted'

    def __init__(self, name, inNode, outNode, extNode=None, ef=100.0):
        self.name = name
        self.inNode = inNode
        self.outNode = outNode
        self.extNode = extNode
        if extNode != None:
            self.typeStr = 'TURBINE-EX0'
        else:
            self.typeStr = 'TURBINE-EX1'

        self.ef = ef / 100.0

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

        if self.extNode != None:
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
                if self.extNode != None:
                    nodes[self.outNode].fdot = nodes[
                        self.inNode].fdot - nodes[self.extNode].fdot
                else:
                    nodes[self.outNode].fdot = nodes[self.inNode].fdot

                self.fdotok = nodes[self.outNode].fdot != None
                self.fdotok = self.fdotok and (nodes[self.inNode].fdot != None)
                self.fdotok = self.fdotok and (
                    nodes[self.extNode].fdot != None)

            except:
                self.fdotok = False

    def simulate(self, nodes):
        self.workExtracted = 0
        if self.extNode != None:
            self.workExtracted = nodes[self.extNode].fdot * \
                (nodes[self.inNode].h - nodes[self.extNode].h)
        self.workExtracted += nodes[self.outNode].fdot * \
            (nodes[self.inNode].h - nodes[self.outNode].h)

    def sm_energy(self, nodes):
        # mdot，get WExtracted
        self.WExtracted = 0

        if self.extNode != None:
            self.WExtracted = nodes[self.extNode].mdot * \
                (nodes[self.inNode].h - nodes[self.extNode].h)

        self.WExtracted += nodes[self.outNode].mdot * \
            (nodes[self.inNode].h - nodes[self.outNode].h)

        self.WExtracted /= (3600.0 * 1000.0)

    def export(self, nodes):
        result = '\n' + self.name
        result += '\n' + Node.nodetitle
        result += '\n' + nodes[self.inNode].__str__()
        result += '\n' + nodes[self.outNode].__str__()
        if self.extNode != None:
            result += '\n' + nodes[self.extNode].__str__()

        result += '\nworkExtracted(kJ/kg): \t%.2f \nWExtracted(MW): \t%.2f' % (
            self.workExtracted, self.WExtracted)
        return result
