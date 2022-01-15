"""
The PyRankine: the  hybrid steady-state simulator of Rankine Cycle

 class Boiler

                    ↑    oPort[0] main steam
                ┌───┼───┐ 
                │   │   │   
                │   │   │
                │   │   │
                └───┼───┘  
                    ↑    iPort[0]  main feedwater
                          
 json object example:

        {    
            "name": "Boiler",  
            "devtype": "BOILER",
            "iPort": {"p": 8.0},
            "oPort": {"p": 8.0, "x": 1.0, "fdot": 1.0}
        }

Rows:
   1. mass balance row

Author:Cheng Maohua  Email: cmh@seu.edu.cn 

"""

from .port import *


class Boiler:
    """ Boiler(i,o) sm and eo   """
    energy = "heatAdded"
    devtype = "BOILER"

    def __init__(self, dictDev):
        """
        Initializes the boiler
        """
        self.name = dictDev['name']
        self.iPort = [Port(dictDev['iPort'])]
        self.oPort = [Port(dictDev['oPort'])]

        # map the port's name to the obj
        self.portdict = {
            "iPort": self.iPort,
            "oPort": self.oPort
        }

    def state(self):
        pass

    # sequential-modular approach
    def balance(self):
        """ mass and energy balance of the boiler """
        # mass balance equation
        if self.iPort[0].fdot is not None:
            self.oPort[0].fdot = self.iPort[0].fdot
        elif self.oPort[0].fdot is not None:
            self.iPort[0].fdot = self.oPort[0].fdot

        self.heatAdded = self.iPort[0].fdot * \
            (self.oPort[0].h - self.iPort[0].h)

    #  equation-oriented approach
    def equation_rows(self):
        """ each row {"a":[(colid,val),...] "b":val} """
        # mass balance row
        if self.iPort[0].fdot is not None:
            rowms ={"a":[(self.oPort[0].id, 1)],"b": self.iPort[0].fdot}

        if self.oPort[0].fdot is not None:
            rowms ={"a":[(self.iPort[0].id, 1)],"b": self.oPort[0].fdot}
        self.rows = [rowms]

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
