"""
The PyRankine: the hybrid steady-state simulator of Rankine Cycle

  class Reheater

                    ↑    oPort steam
                ┌───┼───┐ 
                │   │   │   
                │   │   │
                │   │   │
                └───┼───┘  
                    ↑    iPort steam 
                          
 json object example:

      {    
            "name": "reheater1",  
            "type": "REHEATER",
            "iPort":{},
            "oPort":{}
        }
row:
  1. mass balance row

Author:Cheng Maohua  Email: cmh@seu.edu.cn 

"""

from .port import *


class Reheater:
    """ sm and so """

    energy = "heatAdded"
    devtype = "REHEATER"

    def __init__(self, dictDev):
        """
        Initializes the boiler
        """
        self.name = dictDev['name']
        self.iPort = [Port(dictDev['iPort'])]
        self.oPort = [Port(dictDev['oPort'])]

        # map the name of port to the port obj
        self.portdict = {
            "iPort": self.iPort,
            "oPort": self.oPort
        }

        self.heatAdded = 0

    def state(self):
        pass

    # sequential-modular approach
    def balance(self):
        """ mass and energy balance of the boiler """
        # mass balanceequation
        if self.iPort[0].fdot is not None:
            self.oPort[0].fdot = self.iPort[0].fdot
        elif self.oPort[0].fdot is not None:
            self.iPort[0].fdot = self.oPort[0].fdot

        self.heatAdded = self.iPort[0].fdot * \
            (self.oPort[0].h - self.iPort[0].h)

    #  equation-oriented approach
    def equation_rows(self):
        # 1 mass balance row
        colid = [(self.iPort[0].id, 1), (self.oPort[0].id, -1)]
        self.rows = [{"a": colid, "b": 0}]

    #  equation-oriented approach
    def energy_fdot(self):
        self.heatAdded = self.iPort[0].fdot * \
            (self.oPort[0].h - self.iPort[0].h)

    def calmdot(self, totalmass):
        pass

    def sm_energy(self):
        self.QAdded = self.iPort[0].mdot * \
            (self.oPort[0].h - self.iPort[0].h)
        self.QAdded /= (3600.0 * 1000.0)

    def __str__(self):
        result = '\n' + self.name
        result += '\n' + " PORT " + Port.title
        result += '\n' + " iPort " + self.iPort[0].__str__()
        result += '\n' + " oPort " + self.oPort[0].__str__()
        result += '\nheatAdded(kJ) \t{:>.2f}'.format(self.heatAdded)
        try:
            result += '\nQAdded(MW) \t{:>.2f}'.format(self.QAdded)
        except:
            pass
        return result
