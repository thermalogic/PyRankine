"""
sm and so
  class Pipemleak
                    ↑ oPort
                    │      pipemass leaks:lPort1,lPort2
                    │ iPort  
                    ↑ 
                               
 
es1={
        "name": "mspipe",
        "devtype": "PIPEMLOSS",
         "iPort": {},
         "oPort": {},
         "lPort1": {},
         "lPort2": {}
}

mass balance row

 Author:Cheng Maohua  Email: cmh@seu.edu.cn 

"""

from .port import Port


class PipeMloss:
    """ sm and so """

    energy = "massLossedPipe"
    devtype = "PIPEMLOSS"

    def __init__(self, dictDev):
        """
        Initializes  PipeMloss
        """
        # self.__dict__.update(dictDev)
        self.name = dictDev['name']
        self.iPort = [Port(dictDev['iPort'])]
        self.oPort = [Port(dictDev['oPort'])]
        self.lPort1 = [Port(dictDev['lPort1'])]
        self.lPort2 = [Port(dictDev['lPort2'])]

        # map the name of port to the port obj
        self.portdict = {
            "iPort": self.iPort,
            "oPort": self.oPort,
            "lPort1": self.lPort1,
            "lPort2": self.lPort2
        }

        self.heatLossPipe = None
        self.QLossPipe = None

    def state(self):
        """ simple set o=i """
        self.oPort[0].t = self.iPort[0].t
        self.oPort[0].p = self.iPort[0].p
        self.oPort[0].pt()

    def balance(self):
        """ 1kg """
        # mass balanceequation
        self.oPort[0].fdot = self.iPort[0].fdot - \
            self.lPort1[0].fdot-self.lPort2[0].fdot
        # energy
        self.heatLossPipe = self.lPort1[0].fdot * \
            self.lPort1[0].h+self.lPort2[0].fdot*self.lPort2[0].h
        # 严格的话应该计算self.oPort[0].h - 结果稍变大
        #self.oPort[0].h = (self.iPort[0].fdot * self.iPort[0].h-self.heatLossPipe)/ self.oPort[0].fdot
        # self.oPort[0].p=self.iPort[0].p
        # self.oPort[0].ph()

    #  equation-oriented approach
    def equation_rows(self):
        # mass balance row
        colid = [(self.iPort[0].id, 1),
                 (self.oPort[0].id, -1)]
        # known fdot in b[]
        bv = self.lPort1[0].fdot+self.lPort2[0].fdot
        self.rows = [{"a": colid, "b": bv}]

    #  equation-oriented approach
    def energy_fdot(self):
        """ energy_fdot """
        self.heatLossPipe = self.lPort1[0].fdot * \
            self.lPort1[0].h+self.lPort2[0].fdot*self.lPort2[0].h

    def calmdot(self, totalmass):
        self.lPort1[0].mdot = self.lPort1[0].fdot * totalmass
        self.lPort2[0].mdot = self.lPort2[0].fdot * totalmass

    def sm_energy(self):
        """ mdot """
        self.QLossPipe = self.lPort1[0].mdot * \
            self.lPort1[0].h+self.lPort2[0].mdot*self.lPort2[0].h
        self.QLossPipe /= (3600.0 * 1000.0)

    def __str__(self):
        result = '\n' + self.name
        result += '\n' + " PORT " + Port.title
        result += '\n' + " iPort " + self.iPort[0].__str__()
        result += '\n' + " oPort " + self.oPort[0].__str__()
        result += '\n' + " lPort1 " + self.lPort1[0].__str__()
        result += '\n' + " lPort2 " + self.lPort2[0].__str__()
        result += '\nheatLossPipe(kJ) \t{:>.2f}'.format(self.heatLossPipe)
        try:
            result += '\nQLossPipe(MW) \t{:>.2f}'.format(self.QLossPipe)
        except:
            pass
        return result
