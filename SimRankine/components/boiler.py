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
        self.iPort = Port(dictDev['iPort'])
        self.oPort = Port(dictDev['oPort'])

        self.heatAdded=None

    def state(self):
        pass

    # sequential-modular approach
    def balance(self):
        """ mass and energy balance of the boiler """
        # mass balance equation
        if self.iPort.fdot is None and self.oPort.fdot is None:
            raise ValueError("fdot is none")
        elif self.iPort.fdot is not None:
            self.oPort.fdot = self.iPort.fdot
        elif self.oPort.fdot is not None:
            self.iPort.fdot = self.oPort.fdot
        self.heatAdded = self.iPort.fdot * \
            (self.oPort.h - self.iPort.h)

    #  equation-oriented approach
    def equation_rows(self):
        """ each row {"a":[(colid,val),...] "b":val} """
        # mass balance row
        if self.iPort.fdot is not None:
            rowms ={"a":[(self.oPort.id, 1)],"b": self.iPort.fdot}

        if self.oPort.fdot is not None:
            rowms ={"a":[(self.iPort.id, 1)],"b": self.oPort.fdot}
        self.rows = [rowms]

    #  equation-oriented approach
    def energy_fdot(self):
        self.heatAdded = self.iPort.fdot * \
            (self.oPort.h - self.iPort.h)

    def calmdot(self, totalmass):
        pass

    def sm_energy(self):
        self.QAdded = self.iPort.mdot * \
            (self.oPort.h - self.iPort.h)
        self.QAdded /= (3600.0 * 1000.0)

    def __str__(self):
        result = '\n' + self.name
        result += '\n' + " PORT " + Port.title
        result += '\n' + " iPort " + self.iPort.__str__()
        result += '\n' + " oPort " + self.oPort.__str__()
        result += '\nheatAdded(kJ) \t{:>.2f}'.format(self.heatAdded)
        try:
            result += '\nQAdded(MW) \t{:>.2f}'.format(self.QAdded)
        except:
            pass
        return result
