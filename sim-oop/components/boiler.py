"""
 General Object-oriented Abstraction and JSON Textual Model of Rankine Cycle  

  class Boiler

                    ↑    oNode main steam
                ┌───┼───┐  (No.i)
                │   │   │   
                │   │   │
                │   │   │
                └───┼───┘  
                    ↑    iNode main feedwater
                            (No.j)  

 json object example:

        {    
            "name": "Boiler",  
            "type": "BOILER",
            "iNode":i,
            "oNode":j
        }

 Last updated: 2018.05.10

 Author:Cheng Maohua  Email: cmh@seu.edu.cn 

"""

from .node import *


class Boiler:

    energy = "heatAdded"
    type = "BOILER"

    def __init__(self, dictDev, nodes):
        """
        Initializes the boiler
        """
        # self.__dict__.update(dictDev)

        self.name = dictDev['name']
        self.iNode = nodes[dictDev['iNode']]
        self.oNode = nodes[dictDev['oNode']]

    def state(self):
        pass

    def balance(self):
        """ mass and energy balance of the boiler """
        # mass blance equation
        if self.iNode.fdot is not None:
            self.oNode.fdot = self.iNode.fdot
        elif self.oNode.fdot is not None:
            self.iNode.fdot = self.oNode.fdot

        self.heatAdded = self.iNode.fdot * (self.oNode.h - self.iNode.h)

    def sm_energy(self):
        self.QAdded = self.iNode.mdot * \
            (self.oNode.h - self.iNode.h)
        self.QAdded /= (3600.0 * 1000.0)

    def __str__(self):
        result = '\n' + self.name
        result += '\n' + Node.title
        result += '\n' + self.iNode.__str__()
        result += '\n' + self.oNode.__str__()
        result += '\nheatAdded(kJ/kg) \t{:>.2f}'.format(self.heatAdded)
        result += '\nQAdded(MW) \t{:>.2f}'.format(self.QAdded)
        return result
