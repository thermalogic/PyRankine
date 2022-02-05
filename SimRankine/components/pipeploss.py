"""
The PyRankine: the hybrid steady-state simulator of Rankine Cycle

class PipePloss
                    ↑ oPort
                    │      ploss
                    │ iPort  
                    ↑ 
                               
 
es1={
        "name": "ES1",
        "devtype": "PIPEPELOSS",
        "oPort": {},
        "iPort": {"p": 24.2, "t": 566.0, "fdot": 1.0},
        "ploss": 0.05
        
}

row:
   mass balance row

Author:Cheng Maohua  Email: cmh@seu.edu.cn 

"""

from .port import *


class PipePloss:
    """ sm and so """
    energy = "heatLossedPipe"
    devtype = "PIPEPLOSS"

    def __init__(self, dictDev):
        """
        Initializes the boiler
        """
        # self.__dict__.update(dictDev)
        self.name = dictDev['name']
        self.iPort = Port(dictDev['iPort'])
        self.oPort = Port(dictDev['oPort'])
      
        self.ploss = dictDev['ploss']

        self.heatLossPipe = None
        self.QLossPipe = None

    def state(self):
        self.oPort.h = self.iPort.h
        self.oPort.p = self.iPort.p*(1.0-self.ploss)
        self.oPort.ph()

    def balance(self):
        """ 1kg """
        # mass balanceequation
        if self.iPort.fdot is not None:
            self.oPort.fdot = self.iPort.fdot
        elif self.oPort.fdot is not None:
            self.iPort.fdot = self.oPort.fdot

        # energy
        self.heatLossPipe = self.oPort.fdot * \
            (self.iPort.h - self.oPort.h)

    #  equation-oriented approach
    def equation_rows(self):
        # 1 mass balance row
        colid = [(self.iPort.id, 1),
                 (self.oPort.id, -1)]
        self.rows = [{"a": colid, "b": 0}]

    #  equation-oriented approach
    def energy_fdot(self):
        """ energy_fdot """
        self.heatLossPipe = self.oPort.fdot * \
            (self.iPort.h - self.oPort.h)

    def calmdot(self, totalmass):
        pass

    def sm_energy(self):
        """ mdot """
        self.QLossPipe = self.oPort.mdot * \
            (self.iPort.h - self.oPort.h)
        self.QLossPipe /= (3600.0 * 1000.0)

    def __str__(self):
        result = '\n' + self.name
        result += '\n' + " PORT " + Port.title
        result += '\n' + " iPort " + self.iPort.__str__()
        result += '\n' + " oPort " + self.oPort.__str__()
        result += '\nheatLossPipe(kJ) \t{:>.2f}'.format(self.heatLossPipe)
        try:
            result += '\nQLossPipe(MW) \t{:>.2f}'.format(self.QLossPipe)
        except:
            pass
        return result
