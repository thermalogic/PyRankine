
"""
The PyRankine: the hybrid steady-state simulator of Rankine Cycle

    class Pump

                   ┌───────┐
                   │       │
    oPort        ← ┼───────┼← iPort
                   │       │  
                   └───────┘  
 
  json object example:
     {
            "name": "Feedwater Pump1",
            "devtype": "PUMP",
            "ef": 1.00,
            "iPort": {},
            "oPort": {"p": 8.0}
        
        }

row:
  1. mass balance row      

  Author:Cheng Maohua  Email: cmh@seu.edu.cn               

"""
from seuif97 import ps2h
from .port import *
from . import KJ_TO_MW


class Pump():
    """ sm and so """
    energy = "workRequired"
    devtype = "PUMP"

    def __init__(self, dictDev):
        """
        Initializes the pump with the conditions
        """
        self.name = dictDev['name']
        self.eta = dictDev['eta']
        self.iPort = Port(dictDev['iPort'])
        self.oPort = Port(dictDev['oPort'])

      
    def state(self):
        """
        calc oPort[0] of the pump 
        """
        sout_s = self.iPort.s
        hout_s = ps2h(self.oPort.p, sout_s)
        self.oPort.h = self.iPort.h + (hout_s - self.iPort.h)/self.eta
        self.oPort.ph()

    # sequential-modular approach
    def balance(self):
        """  mass and energy balance the pump    """
        # mass balance
        if self.iPort.fdot is not None:
            self.oPort.fdot = self.iPort.fdot
        elif self.oPort.fdot is not None:
            self.iPort.fdot = self.oPort.fdot

        # energy
        self.workRequired = self.iPort.fdot * \
            (self.oPort.h - self.iPort.h)

    #  equation-oriented approach
    def equation_rows(self):
        # 1 mass balance row
        colid = [(self.iPort.id, 1), (self.oPort.id, -1)]
        self.rows = [{"a": colid, "b": 0}]

    #  equation-oriented approach
    def energy_fdot(self):
        """ energy_fdot """
        self.workRequired = self.iPort.fdot * \
            (self.oPort.h - self.iPort.h)

    def calmdot(self, totalmass):
        pass

    def sm_energy(self):
        self.WRequired = self.iPort.mdot * \
            (self.oPort.h - self.iPort.h) / KJ_TO_MW

    def __str__(self):
        result = '\n' + self.name
        result += '\n' + " PORT " + Port.title
        result += '\n'+" iPort " + self.iPort.__str__()
        result += '\n'+" oPort " + self.oPort.__str__()
        result += f'\neta(%): \t{self.eta*100.0:>.2f}'
        result += f'\nworkRequired(kJ): \t{self.workRequired:>.2f}'
        try:
            result += f'\nWRequired(MW): \t{self.WRequired:>.2f}'
        except:
            pass
        return result
