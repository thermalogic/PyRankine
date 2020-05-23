"""
 General Object-oriented Abstraction and JSON Textual Model of Rankine Cycle 

class Openedheaterdw0

                      ↓   inNode extracted steam(No.i)
                  ┌───┴───┐
 feedwater        │       │
 outNode_fw     ← ┤       │← inNode_fw  feedwater(No.j)
     (No.k)       │       │
                  └───────┘

 json object example:

     {
            "name": "Opened Feedwater Heater1",
            "type": "FWH-OPEN-DW0",
            "iNode":i,
            "iNode_fw":j,
            "oNode_fw":k
     }

  Last updated: 2018.05.08
  Author:Cheng Maohua  Email: cmh@seu.edu.cn

"""
from .node import *


class OpenedheaterDw0:

    energy = 'internel'
    type = "FWH-OPEN-DW0"

    def __init__(self, dictDev, nodes):
        """
        Initializes the Opened feedwater with the conditions
        """
        self.name = dictDev['name']
        self.iNode = nodes[dictDev['iNode']]
        self.iNode_fw = nodes[dictDev['iNode_fw']]
        self.oNode_fw = nodes[ dictDev['oNode_fw']]

        self.heatAdded = 0
        self.heatExtracted = 0
        self.QExtracted = 0

    def state(self):
        pass

    def balance(self):
        """ mass and energy balance of the opened feedwater heater """
        # energy balance equation
        qes1 = self.iNode.h - self.oNode_fw.h
        qfw1 = self.oNode_fw.h - self.iNode_fw.h
        self.iNode.fdot = self.oNode_fw.fdot * qfw1/(qes1 + qfw1)
        # mass balance equation
        self.iNode_fw.fdot = self.oNode_fw.fdot - self.iNode.fdot

        self.heatAdded = self.iNode_fw.fdot * qfw1
        self.heatExtracted = self.iNode.fdot * qes1

    def sm_energy(self):
        ucovt = 3600.0 * 1000.0
        self.QExtracted = self.iNode.mdot * \
            (self.iNode.h - self.oNode_fw.h)/ucovt
        self.QAdded = self.iNode_fw.mdot * \
            (self.oNode_fw.h - self.iNode_fw.h)/ucovt

    def __str__(self):
        result = '\n' + self.name
        result += '\n' + Node.title
        result += '\n' + self.iNode.__str__()
        result += '\n' + self.iNode_fw.__str__()
        result += '\n' + self.oNode_fw.__str__()

        result += '\nheatAdded(kJ/kg) \t{:>.2f}'.format(self.heatAdded)
        result += '\nheatExtracted(kJ/kg) \t{:>.2f}'.format(self.heatExtracted)
        result += '\nQAdded(MW) \t{:>.2f}'.format(self.QAdded)
        result += '\nQExtracted(MW)  \t{:>.2f}'.format(self.QExtracted)
        return result
