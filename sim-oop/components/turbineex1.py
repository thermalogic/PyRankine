"""
General Object-oriented Abstraction and JSON Textual Model of Rankine Cycle 

    TurbineEx1 class: 
       
        iNode inlet steam   (No.i)
                 ┌────────┐
              ↓ ╱         │ 
               ┤          │
                ╲         │
                 └──┬─────┤
          eNode   ↓     ↓  oNode exhausted steam  (No.i) 
extracted steam     1    
   (No.k)

object example

     {
            "name": "Turbine1",
            "type": "TURBINE-EX1",
            "ef": 0.85,
            "iNode": i,
            "oNode": j,
            "eNode": k
      } 

  Last updated: 2018.05.05
  Author:Cheng Maohua  Email: cmh@seu.edu.cn

"""
from seuif97 import *
from .node import *


class TurbineEx1:

    energy = 'workExtracted'
    devtype = 'TURBINE-EX1'

    def __init__(self, dictDev, nodes):
        self.name = dictDev['name']
        self.iNode = nodes[dictDev['iNode']]
        self.oNode = nodes[dictDev['oNode']]
        self.eNode = nodes[dictDev['eNode']]

        self.ef = dictDev['ef']
        self.workExtracted =0
        self.WExtracted=0

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
        """ mass and energy balance of the TurbineEx1
            work=ienergy - oenergy
        """
        self.oNode.fdot = self.iNode.fdot - self.eNode.fdot

        ienergy=self.iNode.fdot * self.iNode.h
        oenergy=self.eNode.fdot*self.eNode.h+self.oNode.fdot*self.oNode.h
        self.workExtracted = ienergy - oenergy
        
        
    def sm_energy(self):
        """ mdot，get WExtracted """
        ienergy=self.iNode.mdot * self.iNode.h
        oenergy=self.eNode.mdot*self.eNode.h+self.oNode.mdot*self.oNode.h
        self.WExtracted = ienergy - oenergy
        self.WExtracted /= (3600.0 * 1000.0)

    def __str__(self):
        result = '\n' + self.name
        result += '\n' + Node.title
        result += '\n' + self.iNode.__str__()
        result += '\n' + self.oNode.__str__()
        result += '\n' + self.eNode.__str__()
        result += '\nworkExtracted(kJ/kg): \t{:>.2f}'.format(self.workExtracted)
        result += '\nWExtracted(MW): \t{:>.2f}'.format(self.WExtracted)     
        return result
