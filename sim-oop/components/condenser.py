
"""
 General Object-oriented Abstraction and JSON Textual Model of Rankine Cycle

  class  Condenser

                    ↓   iNode exhausted steam
                ┌───┴───┐   (No.i)
                │       │
                │       │
                │       │
                └───┬───┘
                    ↓ oNode condensate water
                            (No.j)
object example:

   {
            "name": "Condenser1",
            "type": "CONDENSER",
            "iNode": i,
            "oNode": j
   },

   Last updated: 2018.05.10
   Author:Cheng Maohua  Email: cmh@seu.edu.cn
"""

from .node import *


class Condenser:

    energy = "heatExtracted"
    devtype = "CONDENSER"

    def __init__(self, dictDev, nodes):
        """ Initializes the condenser """
        self.name = dictDev['name']
        self.iNode = nodes[dictDev['iNode']]
        self.oNode = nodes[dictDev['oNode']]

    def state(self):
        pass

    def balance(self):
        """ mass and energy balance of the condenser  """
        if self.iNode.fdot is not None:
            self.oNode.fdot = self.iNode.fdot
        elif self.oNode.fdot is not None:
            self.iNode.fdot = self.oNode.fdot

        self.heatExtracted = self.iNode.fdot * (self.iNode.h - self.oNode.h)

    def sm_energy(self):
        self.QExtracted = self.iNode.mdot * \
            (self.iNode.h - self.oNode.h)/(3600.0 * 1000.0)

    def __str__(self):
        result = '\n' + self.name
        result += '\n' + Node.title
        result += '\n' + self.iNode.__str__()
        result += '\n' + self.oNode.__str__()
        result += '\nheatExtracted(kJ/kg)  \t{:>.2f}'.format(self.heatExtracted)
        result += '\nQExtracted(MW): \t{:>.2f}'.format(self.QExtracted)    
        return result

