
"""
pumu with inlet pipe

    class Pump_Pipe

                ┌───────┐        ↓   iPort iLevel
                │       │        │   (No.i) 
       oPort   ←┼───────┼────────┘
    (No.j)      │       │ 
                └───────┘  
 
  json object example:
     {
            "name": "Feedwater Pump",
            "type": "PUMP-PIPE",
            "iPort":{},
            "oPort":{},
            "eta": 0.83,
            "iLevel":20.0
        }

  Author:Cheng Maohua  Email: cmh@seu.edu.cn               

"""
from seuif97 import px2v
from .port import *


class Pump_Pipe:

    energy = "workRequired"
    devtype = "PUMP-PIPE"

    def __init__(self, dictDev):
        """
        Initializes the pump with the conditions
        """
        self.name = dictDev['name']
        self.iPort = [Port(dictDev['iPort'])]
        self.oPort = [Port(dictDev['oPort'])]

        # map the name of port to the port obj
        self.portdict = {
            "iPort": self.iPort,
            "oPort": self.oPort
        }

        self.eta = dictDev['eta']

        self.level = dictDev['iLevel']

        self.workRequired = None

    def state(self):
        """ state """
        p_pu_in = self.level*0.0098+self.iPort[0].p
        v_av = px2v(p_pu_in, 0)
        h_delta_pu = 1000*v_av*(self.oPort[0].p-p_pu_in)/self.eta
        self.oPort[0].h = self.iPort[0].h+h_delta_pu
        self.oPort[0].ph()

    def balance(self):
        """ Simulates the pump  """
        # mass balanceequation
        if (self.iPort[0].fdot != None):
            self.oPort[0].fdot = self.iPort[0].fdot
        elif (self.oPort[0].fdot != None):
            self.iPort[0].fdot = self.oPort[0].fdot
        # energy
        self.workRequired = self.iPort[0].fdot * (self.oPort[0].h - self.iPort[0].h)

    def calmdot(self, totalmass):
        pass

    def sm_energy(self):
        """ mdot """
        ucovt = 3600.0 * 1000.0
        self.WRequired = self.iPort[0].mdot * (self.oPort[0].h - self.iPort[0].h)/ucovt

    def __str__(self):
        """ string of feedwater pump """
        result = '\n' + self.name
        result += '\n' +" PORT "+ Port.title
        result += '\n' + " iPort "+self.iPort[0].__str__()
        result += '\n' + " oPort "+self.oPort[0].__str__()
        result += '\nhlevel(m): \t{:>.2f}'.format(self.level)
        result += '\neta(%): \t{:>.2f}'.format(self.eta*100)
        result += '\nworkRequired(kJ): \t{:>.2f}'.format(self.workRequired)
        try:
            result += '\nWRequired(MW): \t{:>.2f}'.format(self.WRequired)
        except:
            pass    
        return result
