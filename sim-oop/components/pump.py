
"""
 General Object-oriented Abstraction and JSON Textual Model of Rankine Cycle 

    class Pump

                   ┌───────┐
                   │       │
    outNode      ← ┼───────┼← inNode
    (No.j)         │       │  (No.i)
                   └───────┘  
 
  json object example:
     {
            "name": "Feedwater Pump1",
            "type": "PUMP",
            "ef": 1.00,
            "inNode":i,
            "outNode":j
        }

  Last updated: 2018.05.08
  Author:Cheng Maohua  Email: cmh@seu.edu.cn               

"""
from seuif97 import ps2h
from .node import *


class Pump():

    energy = "workRequired"
    type = "PUMP"

    def __init__(self, dictDev,nodes):
        """
        Initializes the pump with the conditions
        """
        self.name = dictDev['name']
        self.inNode = dictDev['inNode']
        self.outNode = dictDev['outNode']
        self.ef = dictDev['ef']
        self.iNode = nodes[self.inNode]
        self.oNode = nodes[self.outNode]

    def state(self):
        """
        calc outNode of the pump 
        """
        sout_s = self.iNode.s
        hout_s = ps2h(self.oNode.p, sout_s)
        self.oNode.h = self.iNode.h + (hout_s - self.iNode.h)/self.ef
        self.oNode.ph()

    def balance(self):
        """  mass and energy balance the pump    """
        # mass balance
        if (self.iNode.fdot != None):
            self.oNode.fdot = self.iNode.fdot
        elif (self.oNode.fdot != None):
            self.iNode.fdot = self.oNode.fdot

        # energy
        self.workRequired = self.iNode.fdot * (self.oNode.h - self.iNode.h)

    def sm_energy(self):
        self.WRequired = self.iNode.mdot * \
            (self.oNode.h - self.iNode.h)/(3600.0 * 1000.0)

    def __str__(self):
        result = '\n' + self.name
        result += '\n' + Node.title
        result += '\n' + self.iNode.__str__()
        result += '\n' + self.oNode.__str__()

        result += '\nworkRequired(kJ/kg): \t{:>.2f}'.format(self.workRequired)
        result += '\nWRequired(MW): \t{:>.2f}'.format(self.WRequired)
        return result

    def __iter__(self):
        """ the dict of the object """
        dictobj = {'name': self.name,
                   'inNode': dict(self.iNode),
                   'outNode': dict(self.oNode),
                   'ef': self.ef,
                   'workRequired(kJ/kg)': self.workRequired,
                   'WRequired(MW)': self.WRequired
                   }

        for key, value in dictobj.items():
            yield (key, value)
