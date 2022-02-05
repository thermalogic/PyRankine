
"""
The PyRankine: the  hybrid steady-state simulator of Rankine Cycle
  
  so and sm

  class  Condenser

                  ↓  ↓   iPort/1 exhausted steam
                ┌───┴───┐  
                │       │
                │       │
                │       │
                └───┬───┘=
                   ↓ ↓ oPort/1 condensate water
                           
json object example:

   {
            "name": "Condenser1",
            "devtype": "CONDENSER",
            "iPort": {},
            "oPort": {},
            "iPort1": {},
            "oPort1": {}
   }

mass balance row1/2

   Author:Cheng Maohua  Email: cmh@seu.edu.cn
"""

from .port import *


class Condenser:
    """ so and sm """

    energy = "heatExtracted"
    devtype = "CONDENSER"

    def __init__(self, dictDev):
        """ Initializes the condenser """
        self.name = dictDev['name']
        self.iPort = Port(dictDev['iPort'])
        self.oPort = Port(dictDev['oPort'])
        if ("iPort1" in dictDev):
            self.iPort1 = Port(dictDev['iPort1'])
            self.oPort1 = Port(dictDev['oPort1'])
        else:
            self.iPort1 = None
            self.oPort1 = None

        self.heatExtracted = 0

    def state(self):
        pass

    # sequential-modular approach
    def balance(self):
        """ mass and energy balance of the condenser  """
        self.oPort.fdot = self.iPort.fdot
        if self.iPort1 is not None:
            self.oPort1.fdot = self.iPort1.fdot
        # energy balance
        if self.iPort.h is not None:
            self.heatExtracted = self.iPort.fdot * \
                (self.iPort.h - self.oPort.h)
            if self.iPort1 is not None and self.iPort1.h is not None:
                self.heatExtracted += self.iPort1.fdot * \
                    (self.iPort1.h - self.oPort.h)

    #  equation-oriented approach
    def equation_rows(self):
        """
          each row: {"a":[(colid,val)] "b":val} 
          self.iPort1 fdot maybe have values
        """
        # mass balance row1/2
        colid = [(self.iPort.id, -1),
                 (self.oPort.id, 1)]
        self.rows = [{"a": colid, "b": 0}]
        if self.iPort1 is not None:
            colid1 = [(self.oPort1.id, 1)]
            self.rows.append({"a": colid1, "b": self.iPort1.fdot})

    #  equation-oriented approach

    def energy_fdot(self):
        if self.iPort.h is not None:
            self.heatExtracted = self.iPort.fdot * \
                (self.iPort.h - self.oPort.h)
            if self.iPort1 is not None and self.iPort1.h is not None:
                self.heatExtracted += self.iPort1.fdot * \
                    (self.iPort1.h - self.oPort.h)

    def calmdot(self, totalmass):
        if self.iPort1 is not None:
            self.iPort1.mdot = self.iPort1.fdot * totalmass

    def sm_energy(self):
        uc = 3600.0 * 1000.0
        if self.iPort.h is not None:
            self.QExtracted = self.iPort.mdot * \
                (self.iPort.h - self.oPort.h)/uc
        if self.iPort1 is not None and self.iPort1.h is not None:
            self.QExtracted += self.iPort1.mdot * \
                (self.iPort1.h - self.oPort.h)/uc

    def __str__(self):
        result = '\n' + self.name
        result += '\n'+" PORT " + Port.title
        result += '\n'+" iPort " + self.iPort.__str__()
        result += '\n'+" oPort " + self.oPort.__str__()
        if self.iPort1 is not None:
            result += '\n'+" iPort1 " + self.iPort1.__str__()
            result += '\n'+" oPort1 " + self.oPort1.__str__()
        result += '\nheatExtracted(kJ)  \t{:>.2f}'.format(self.heatExtracted)
        try:
            result += '\nQExtracted(MW): \t{:>.2f}'.format(self.QExtracted)
        except:
            pass
        return result
