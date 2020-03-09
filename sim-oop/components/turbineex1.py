"""
 General Object-oriented Abstraction and JSON Textual Model of Rankine Cycle 

    TurbineEx1 class: 
       
        inNode inlet steam   (No.i)
                 ┌────────┐
              ↓ ╱         │ 
               ┤          │
                ╲         │
                 └──┬─────┤
          extNode   ↓     ↓  outNode exhausted steam  (No.i) 
extracted steam     1    
   (No.k)

json object example

     {
            "name": "Turbine1",
            "type": "TURBINE-EX1",
            "ef": 0.85,
            "inNode": i,
            "outNode": j,
            "extNode": k
      } 

  Last updated: 2018.05.05
  Author:Cheng Maohua  Email: cmh@seu.edu.cn

"""
from seuif97 import *
from .node import *


class TurbineEx1:

    energy = 'workExtracted'
    type = 'TURBINE-EX1'

    def __init__(self, dictDev, nodes):
        self.name = dictDev['name']
        self.inNode = dictDev['inNode']
        self.outNode = dictDev['outNode']
        self.extNode = dictDev['extNode']
        self.ef = dictDev['ef']
        self.iNode = nodes[self.inNode]
        self.oNode = nodes[self.outNode]
        self.eNode = nodes[self.extNode]

    def state(self):
        if self.ef == 1.0:
            self.eNode.s = self.iNode.s
            self.eNode.ps()
            self.oNode.s = self.iNode.s
            self.oNode.ps()
        else:
            isoh = ps2h(self.eNode.p, self.iNode.s)
            self.eNode.h = self.iNode.h - self.ef * (self.iNode.h - isoh)
            self.eNode.ph()
            isoh = ps2h(self.oNode.p, self.eNode.s)
            self.oNode.h = self.eNode.h - self.ef * (self.eNode.h - isoh)
            self.oNode.ph()

    def balance(self):
        """ mass and energy balance of the TurbineEx1"""
        self.oNode.fdot = self.iNode.fdot - self.eNode.fdot

        self.workExtracted = self.eNode.fdot * (self.iNode.h - self.eNode.h)
        self.workExtracted += self.oNode.fdot * (self.iNode.h - self.oNode.h)

    def sm_energy(self):
        # mdot，get WExtracted
        self.WExtracted = self.eNode.mdot*(self.iNode.h - self.eNode.h)

        self.WExtracted += self.oNode.mdot * (self.iNode.h - self.oNode.h)

        self.WExtracted /= (3600.0 * 1000.0)

    def __str__(self):
        result = '\n' + self.name
        result += '\n' + Node.title
        result += '\n' + self.iNode.__str__()
        result += '\n' + self.oNode.__str__()
        result += '\n' + self.eNode.__str__()
        result += '\nworkExtracted(kJ/kg): \t{:>.2f} \nWExtracted(MW): \t{:>.2f}'.format(
            self.workExtracted, self.WExtracted)
        return result

    def __iter__(self):
        """ the dict of the object """
        dictobj = {'name': self.name,
                   'inNode': dict(self.iNode),
                   'outNode': dict(self.oNode),
                   'extNode': dict(self.eNode),
                   'ef': self.ef,
                   'workExtracted(kJ/kg)': self.workExtracted,
                   'Extracted(MW)': self.WExtracted
                   }

        for key, value in dictobj.items():
            yield (key, value)
