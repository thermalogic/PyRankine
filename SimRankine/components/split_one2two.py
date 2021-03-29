"""
  class Split_One2Two

  sm and so

         ↓ iPort
    ┌────┴────┐                    
  oPort0      oPort1   
  
 json object example:

        {    
         "name": "inpur name",
        "devtype": "SPLIT_ONE2TWO",
        "iPort": {},
        "oPort0": {},
        "oPort1": {}
       }

 mass balance row

 Author:Cheng Maohua  Email: cmh@seu.edu.cn 

"""

from .port import *


class Split_One2Two:
    """ sm and so """

    energy = "none"
    devtype = "SPLIT_ONE2TWO"

    def __init__(self, dictDev):
        """
        Initializes SPLIT_ONE2TWO
        """
        # self.__dict__.update(dictDev)
        self.name = dictDev['name']
        self.iPort = [Port(dictDev['iPort'])]
        self.oPort0 = [Port(dictDev['oPort0'])]
        self.oPort1 = [Port(dictDev['oPort1'])]

        # map the name of port to the port obj
        self.portdict = {
            "iPort": self.iPort,
            "oPort0": self.oPort0,
            "oPort1": self.oPort1
        }

    def state(self):
        if self.iPort[0].p is not None and self.iPort[0].t is not None:
            self.oPort0[0].p = self.iPort[0].p
            self.oPort0[0].t = self.iPort[0].t
            self.oPort0[0].pt()

            self.oPort1[0].p = self.iPort[0].p
            self.oPort1[0].t = self.iPort[0].t
            self.oPort1[0].pt()

        elif self.oPort0[0].p is not None and self.oPort0[0].t is not None:
            self.iPort0[0].p = self.oPort0[0].p
            self.iPort0[0].t = self.oPort[0].t
            self.iPort0[0].pt()

            self.oPort1[0].p = self.oPort0[0].p
            self.oPort1[0].t = self.oPort0[0].t
            self.oPort1[0].pt()

        elif self.oPort1[0].p is not None and self.oPort1[0].t is not None:
            self.iPort0[0].p = self.oPort1[0].p
            self.iPort0[0].t = self.oPort1[0].t
            self.iPort0[0].pt()

            self.oPort0[0].p = self.oPort1[0].p
            self.oPort0[0].t = self.oPort1[0].t
            self.oPort0[0].pt()

    # sequential-modular approach
    def balance(self):
        """ 1kg mass balanceequation"""
        if self.iPort[0].fdot is not None and self.oPort0[0].fdot is not None:
            self.oPort1[0].fdot = self.iPort[0].fdot-self.oPort0[0].fdot
        elif self.iPort[0].fdot is not None and self.oPort1[0].fdot is not None:
            self.oPort0[0].fdot = self.iPort[0].fdot-self.oPort1[0].fdot
        elif self.oPort0[0].fdot is not None and self.oPort1[0].fdot is not None:
            self.iPort[0].fdot = self.oPort0[0].fdot+self.oPort1[0].fdot
        # the ifs maybe without any cal ,so use raise ValueError if fdot is None
        if self.iPort[0].fdot is None or self.oPort0[0].fdot is None or self.oPort1[0].fdot is None:
            raise ValueError("fdot not none")

    #  equation-oriented approach

    def equation_rows(self):
        """ some ports may have values """
        # 1 mass balance  row
        colid = [(self.iPort[0].id, 1),
                 (self.oPort0[0].id, -1),
                 (self.oPort1[0].id, -1),
                 ]
        bv = 0
        # ports have values
        if self.iPort[0].fdot is not None:
            colid = [(self.oPort0[0].id, 1),
                     (self.oPort1[0].id, 1)]
            bv = self.iPort[0].fdot

        if self.oPort0[0].fdot is not None:
            colid = [(self.iPort[0].id, 1),
                     (self.oPort1[0].id, -1)]
            bv = self.oPort0[0].fdot

        if self.oPort1[0].fdot is not None:
            colid = [(self.iPort[0].id, 1),
                     (self.oPort0[0].id, -1)]
            bv = self.oPort1[0].fdot

        self.rows = [{"a": colid, "b": bv}]

    #  equation-oriented approach
    def energy_fdot(self):
        pass

    def calmdot(self, totalmass):
        pass

    def sm_energy(self):
        """ mdot """
        pass

    def __str__(self):
        result = '\n' + self.name
        result += '\n' + " PORT " + Port.title
        result += '\n' + " iPort "+self.iPort[0].__str__()
        result += '\n' + " oPort0 " + self.oPort0[0].__str__()
        result += '\n' + " oPort1 " + self.oPort1[0].__str__()
        return result
