"""
 General Object-oriented Abstraction and JSON Textual Model of Rankine Cycle 

    TurbineEx0 class: 
       
        inNode inlet steam   (No.i)
                 ┌────────┐
              ↓ ╱         │ 
               ┤          │
                ╲         │
                 └────────┤
                          ↓  outNode exhausted steam (No.j)  
extracted steam  0    

json object example

    {
            "name": "Turbine1",
            "type": "TURBINE-EX0",
            "ef": 1.00,
            "inNode": i,
            "outNode": j
    },

  Last updated: 2017.05.05
  Author:Cheng Maohua  Email: cmh@seu.edu.cn

"""
from seuif97 import *
from .node import *


class TurbineEx0:

    energy = 'workExtracted'
    type = 'TURBINE-EX0'

    def __init__(self, dictDev, nodes):
        self.name = dictDev['name']
        self.inNode = dictDev['inNode']
        self.outNode = dictDev['outNode']
        self.ef = dictDev['ef']
        self.iNode=nodes[self.inNode]
        self.oNode=nodes[self.outNode]
        self.WExtracted=0 
        self.workExtracted=0

    def state(self):
        if self.ef == 1.0:
            self.oNode.s =self.iNode.s
            self.oNode.ps()
        else:
            isoh =ps2h(self.oNode.p, self.iNode.s)
            self.oNode.h = self.iNode.h -  self.ef * (self.iNode.h - isoh)
            self.oNode.ph()


    def balance(self):
        """ mass and energy balance of the TurbineEx0"""
        # mass balance equation
        self.oNode.fdot = self.iNode.fdot
        # energy
        self.workExtracted = self.oNode.fdot *(self.iNode.h - self.oNode.h)

    def sm_energy(self):
        # mdot，get WExtracted
        self.WExtracted = self.oNode.mdot * (self.iNode.h - self.oNode.h)
        self.WExtracted /= (3600.0 * 1000.0)

    def __str__(self):
        result = '\n' + self.name
        result += '\n' + Node.title
        result += '\n' + self.iNode.__str__()
        result += '\n' + self.oNode.__str__()
        result += '\nworkExtracted(kJ/kg): \t{:>.2f} \nWExtracted(MW): \t{:>.2f}'.format(
            self.workExtracted, self.WExtracted)
        return result
  
    def __iter__(self):
        dictobj = {'name': self.name,
                   'inNode': dict(self.iNode),
                   'outNode': dict(self.oNode),
                   'ef':self.ef,
                   'workExtracted(kJ/kg)': self.workExtracted,
                   'Extracted(MW)': self.WExtracted
                   }

        for key, value in dictobj.items():
            yield (key, value)
  