
"""
 
 The PyRankine: the  hybrid steady-state simulator of Rankine Cycle

 inlet pipe

 class PipeIlevel:
        
                               ↓   iPort 
                               │
                               │   iLevel
                               │     (No.i) 
                  oPort  ←─────┘
    (No.j)       
                  
 
  json object example:
     {
            "name": "pipe",
            "type": "PIPEILEVEL",
            "iPort":{},
            "oPort":{},
            "iLevel":20.0
        }

Rows:
   1. mass balance row

Author:Cheng Maohua  Email: cmh@seu.edu.cn               

"""
from seuif97 import px2v
from .port import *


class PipeIlevel:

    energy = "None"
    devtype = "PIPEILEVEL"

    def __init__(self, dictDev):
        """
        Initializes the pump with the conditions
        """
        self.name = dictDev['name']
        self.iPort = Port(dictDev['iPort'])
        self.oPort = Port(dictDev['oPort'])

        self.level = dictDev['iLevel']

    def state(self):
        """ state """
        self.oPort.p = self.level*0.0098+self.iPort.p
        self.oPort.h = self.iPort.h  
        self.oPort.ph()

    def balance(self):
        """ Simulates  """
        # mass balanceequation
        if (self.iPort.fdot is not None):
            self.oPort.fdot = self.iPort.fdot
        elif (self.oPort.fdot is not None):
            self.iPort.fdot = self.oPort.fdot
        if (self.oPort.fdot is None or self.iPort.fdot is None):
            raise ValueError("fdot not none")

    #  equation-oriented approach
    def equation_rows(self):
        # 1 mass balance row
        colid = [(self.iPort.id, 1),
                 (self.oPort.id, -1)]
        self.rows = [{"a": colid, "b": 0}]

    #  equation-oriented approach
    def energy_fdot(self):
        """ energy_fdot """
        pass

    def calmdot(self, totalmass):
        pass

    def sm_energy(self):
        """ mdot """
        pass

    def __str__(self):
        """ string of feedwater pump """
        result = '\n' + self.name
        result += '\n' + " PORT " + Port.title
        result += '\n' + " iPort "+self.iPort.__str__()
        result += '\n' + " oPort "+self.oPort.__str__()
        result += '\nhlevel(m): \t{:>.2f}'.format(self.level)
        return result
