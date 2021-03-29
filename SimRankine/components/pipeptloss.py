"""
sm and eo

  class PipePtloss
                    ↑ oPort
                    │  pipe: tdelta,pdelta
                    │ iPort  
                    ↑ 
                               
 
bopipe1={
        "name": "pipe1",
        "devtype": "PIPEPTLOSS",
        "oPort": {},
        "iPort": {"p": 24.2, "t": 566.0, "fdot": 1.0},
       "tdelta": 1.8,
        "pdelta": 0.515

}

mass balance row

 Author:Cheng Maohua  Email: cmh@seu.edu.cn 

"""

from .port import *


class PipePtloss:
    """ sm and eo """

    energy = "heatLossedPipe"
    devtype = "PIPEPTLOSS"

    def __init__(self, dictDev):
        """
        Initializes the boiler
        """
        # self.__dict__.update(dictDev)
        self.name = dictDev['name']
        self.iPort = [Port(dictDev['iPort'])]
        self.oPort = [Port(dictDev['oPort'])]
        # map the name of port to the port obj
        self.portdict = {
            "iPort": self.iPort,
            "oPort": self.oPort
        }

        self.tdelta = dictDev['tdelta']
        self.pdelta = dictDev['pdelta']

        self.heatLossPipe = 0
        self.QLossPipe = None

    def state(self):
        self.oPort[0].t = self.iPort[0].t-self.tdelta
        self.oPort[0].p = self.iPort[0].p-self.pdelta
        self.oPort[0].pt()

    def balance(self):
        """ 1kg """
        # mass balanceequation
        if self.iPort[0].fdot is not None:
            self.oPort[0].fdot = self.iPort[0].fdot
        elif self.oPort[0].fdot is not None:
            self.iPort[0].fdot = self.oPort[0].fdot
        # energy
        self.heatLossPipe = self.oPort[0].fdot * \
            (self.iPort[0].h - self.oPort[0].h)

    #  equation-oriented approach
    def equation_rows(self):
        # 1 mass balance row
        colid = [(self.iPort[0].id, 1),
                 (self.oPort[0].id, -1)]
        self.rows = [{"a": colid, "b": 0}]

    #  equation-oriented approach
    def energy_fdot(self):
        """ energy_fdot """
        self.heatLossPipe = self.oPort[0].fdot * \
            (self.iPort[0].h - self.oPort[0].h)

    def calmdot(self, totalmass):
        pass

    def sm_energy(self):
        """ mdot """
        self.QLossPipe = self.oPort[0].mdot * \
            (self.iPort[0].h - self.oPort[0].h)
        self.QLossPipe /= (3600.0 * 1000.0)

    def __str__(self):
        result = '\n' + self.name
        result += '\n' + " PORT " + Port.title
        result += '\n' + " iPort " + self.iPort[0].__str__()
        result += '\n' + " oPort " + self.oPort[0].__str__()
        result += '\nheatLossPipe(kJ) \t{:>.2f}'.format(self.heatLossPipe)
        try:
            result += '\nQLossPipe(MW) \t{:>.4f}'.format(self.QLossPipe)
        except:
            pass
        return result
