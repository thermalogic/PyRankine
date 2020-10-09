"""
 General Object-oriented Abstraction and JSON Textual Model of Rankine Cycle 

    TurbineEx0 class: 
       
        iNode inlet steam   (No.i)
                 ┌────────┐
              ↓ ╱         │ 
               ┤          │
                ╲         │
                 └────────┤
                          ↓  oNode exhausted steam (No.j)  
extracted steam  0    

json object example

    {
            "name": "Turbine1",
            "type": "TURBINE-EX0",
            "ef": 1.00,
            "iNode": i,
            "oNode": j
    },

  Last updated: 2017.05.05
  Author:Cheng Maohua  Email: cmh@seu.edu.cn

"""
from seuif97 import *
from .node import *


class TurbineEx0:

    energy = 'workExtracted'
    devtype = 'TURBINE-EX0'

    def __init__(self, dictDev, nodes):
        self.name = dictDev['name']
        self.iNode=nodes[dictDev['iNode']]
        self.oNode=nodes[dictDev['oNode']]
        self.ef = dictDev['ef']
       
        self.workExtracted=0
        self.WExtracted=0 
     

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
        self.workExtracted = self.iNode.fdot *(self.iNode.h - self.oNode.h)

    def sm_energy(self):
        # mdot，get WExtracted
        self.WExtracted = self.iNode.mdot * (self.iNode.h - self.oNode.h)
        self.WExtracted /= (3600.0 * 1000.0)

    def __str__(self):
        result = '\n' + self.name
        result += '\n' + Node.title
        result += '\n' + self.iNode.__str__()
        result += '\n' + self.oNode.__str__()
        result += '\nworkExtracted(kJ/kg): \t{:>.2f}'.format(self.workExtracted)
        result += '\nWExtracted(MW): \t{:>.2f}'.format(self.WExtracted)    
        return result
  
   