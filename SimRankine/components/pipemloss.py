"""
The PyRankine: the hybrid steady-state simulator of Rankine Cycle

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

row:
  1. mass balance row

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
        self.iPort = Port(dictDev['iPort'])
        self.oPort = Port(dictDev['oPort'])
        self.lPort1 = Port(dictDev['lPort1'])
        self.lPort2 = Port(dictDev['lPort2'])

        self.heatLossPipe = None
        self.QLossPipe = None

    def state(self):
        """ simple set o=i """
        self.oPort.t = self.iPort.t
        self.oPort.p = self.iPort.p
        self.oPort.pt()

    def balance(self):
        """ 1kg """
        # mass balanceequation
        self.oPort.fdot = self.iPort.fdot - \
            self.lPort1.fdot-self.lPort2.fdot
        # energy
        self.heatLossPipe = self.lPort1.fdot * \
            self.lPort1.h+self.lPort2.fdot*self.lPort2.h
     
    #  equation-oriented approach
    def equation_rows(self):
        # mass balance row
        colid = [(self.iPort.id, 1),
                 (self.oPort.id, -1)]
        # known fdot in b[]
        bv = self.lPort1.fdot+self.lPort2.fdot
        self.rows = [{"a": colid, "b": bv}]

    #  equation-oriented approach
    def energy_fdot(self):
        """ energy_fdot """
        self.heatLossPipe = self.lPort1.fdot * \
            self.lPort1.h+self.lPort2.fdot*self.lPort2.h

    def calmdot(self, totalmass):
        self.lPort1.mdot = self.lPort1.fdot * totalmass
        self.lPort2.mdot = self.lPort2.fdot * totalmass

    def sm_energy(self):
        """ mdot """
        self.QLossPipe = self.lPort1.mdot * \
            self.lPort1.h+self.lPort2.mdot*self.lPort2.h
        self.QLossPipe /= (3600.0 * 1000.0)

    def __str__(self):
        result = '\n' + self.name
        result += '\n' + " PORT " + Port.title
        result += '\n' + " iPort " + self.iPort.__str__()
        result += '\n' + " oPort " + self.oPort.__str__()
        result += '\n' + " lPort1 " + self.lPort1.__str__()
        result += '\n' + " lPort2 " + self.lPort2.__str__()
        result += '\nheatLossPipe(kJ) \t{:>.2f}'.format(self.heatLossPipe)
        try:
            result += '\nQLossPipe(MW) \t{:>.2f}'.format(self.QLossPipe)
        except:
            pass
        return result
