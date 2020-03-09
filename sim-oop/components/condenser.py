
"""
 General Object-oriented Abstraction and JSON Textual Model of Rankine Cycle

  class  Condenser

                    ↓   inNode exhausted steam
                ┌───┴───┐   (No.i)
                │       │
                │       │
                │       │
                └───┬───┘
                    ↓ outNode condensate water
                            (No.j)
json object example:

   {
            "name": "Condenser1",
            "type": "CONDENSER",
            "inNode": i,
            "outNode": j
   },

   Last updated: 2018.05.10
   Author:Cheng Maohua  Email: cmh@seu.edu.cn
"""

from .node import *


class Condenser:

    energy = "heatExtracted"
    type = "CONDENSER"

    def __init__(self, dictDev, nodes):
        """ Initializes the condenser """
        self.name = dictDev['name']
        self.inNode = dictDev['inNode']
        self.outNode = dictDev['outNode']
        self.iNode = nodes[self.inNode]
        self.oNode = nodes[self.outNode]

    def state(self):
        pass

    def balance(self):
        """ mass and energy balance of the condenser  """
        if (self.iNode.fdot != None):
            self.oNode.fdot = self.iNode.fdot
        elif (self.oNode.fdot != None):
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
        result += '\nheatExtracted(kJ/kg)  \t{:>.2f} \nQExtracted(MW): \t{:>.2f}'.format(
            self.heatExtracted, self.QExtracted)
        return result

    def __iter__(self):
        """ the dict of the object """
        dictobj = {'name': self.name,
                   'inNode': dict(self.iNode),
                   'outNode': dict(self.oNode),
                   'heatExtracted(kJ/kg)': self.heatExtracted,
                   'QExtracted(MW)': self.QExtracted
                   }

        for key, value in dictobj.items():
            yield (key, value)
