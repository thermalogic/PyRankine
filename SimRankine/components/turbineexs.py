"""
The PyRankine: the hybrid steady-state simulator of Rankine Cycle

    TurbineExs class: 
       
        iPort inlet steam   
                 ┌────────┐
              ↓ ╱         │ 
               ┤          │
                ╲         │
                 └──┬─────┤
          ePort?   ↓  ↓   ↓  oPort exhausted steam  
extracted steam     
  
json object example

     {
            "name": "Turbine1",
            "type": "TURBINEEXS",
            "ef": 0.85,
            "iPort":{},
            "oPort": {},
            "ePort0": {}，
            "ePort1":{}，
            
      } 

row:
  1. mass balance row    

 Author:Cheng Maohua  Email: cmh@seu.edu.cn

"""
from seuif97 import *
from .port import *


class TurbineExs:
    """ sm and so """
    energy = 'workExtracted'
    devtype = 'TURBINEEXS'

    def __init__(self, dictDev):
        self.name = dictDev['name']
        self.iPort = Port(dictDev['iPort'])
        self.oPort = Port(dictDev['oPort'])
        self.ePort = []
        self.ePort0, self.ePort1, self.ePort2, self.ePort3 = None, None, None, None
        if ("ePort0" in dictDev):
            self.ePort0 = Port(dictDev["ePort0"])
            self.ePort.append(self.ePort0)
        if ("ePort1" in dictDev):
            self.ePort1 = Port(dictDev["ePort1"])
            self.ePort.append(self.ePort1)
        if ("ePort2" in dictDev):
            self.ePort2 = Port(dictDev["ePort2"])
            self.ePort.append(self.ePort2)
        if ("ePort3" in dictDev):
            self.ePort3 = Port(dictDev["ePort3"])
            self.ePort.append(self.ePort3)
        
        if ('eta' in dictDev):
            self.eta = dictDev['eta']
        else:
            self.eta = None

        self.workExtracted = 0
        self.WExtracted = 0

    def state(self):
        """
          Two kind of Inputs
            1. input ef, to get all port values 
            2. input port(p,t),to get ef
        """
        if self.eta is not None:
            if self.eta == 1.0:
                # ePort
                for ep in self.ePort:
                    ep.s = self.iPort.s
                    ep.ps()
                # oPort
                self.oPort.s = self.iPort.s
                self.oPort.ps()
            else:
                # ePort
                for ep in self.ePort:
                    isosh = ps2h(ep.p, self.iPort.s)
                    ep.h = self.iPort.h - \
                        self.eta * (self.iPort.h - isosh)
                    ep.ph()
                # oPort
                isoh = ps2h(self.oPort.p, self.iPort.s)
                self.oPort.h = self.iPort.h - \
                    self.eta * (self.iPort.h - isoh)
                self.oPort.ph()

        else:
            isosh = ps2h(self.oPort.p, self.iPort.s)
            isohd = self.iPort.h - isosh
            hd = self.iPort.h-self.oPort.h
            self.eta = hd/isohd

    # sequential-modular approach
    def balance(self):
        """ mass and energy balance of the TurbineEx1
            work=ienergy - oenergy
        """
        totalesfdot = 0
        for ep in self.ePort:
            if ep.fdot is None:  # 所有抽汽计算以后才可以计算排汽,所以，只要有抽汽未计算就抛出异常
                raise ValueError("es.fdot is none")
            else:
               totalesfdot += ep.fdot
        self.oPort.fdot = self.iPort.fdot-totalesfdot

        ienergy = self.iPort.fdot * self.iPort.h
        oenergy = self.oPort.fdot*self.oPort.h
        for ep in self.ePort:
            oenergy += ep.fdot*ep.h
        self.workExtracted = ienergy - oenergy

    #  equation-oriented approach
    def equation_rows(self):
        """ mass balance row """
        # 1 mass balance row
        colid = [(self.iPort.id, 1),
                 (self.oPort.id, -1)]
        for ep in self.ePort:
            colid.append((ep.id, -1))
        self.rows = [{"a": colid, "b": 0}]

    #  equation-oriented approach
    def energy_fdot(self):
        ienergy = self.iPort.fdot * self.iPort.h
        oenergy = self.oPort.fdot*self.oPort.h
        for ep in self.ePort:
            oenergy += ep.fdot*ep.h
        self.workExtracted = ienergy - oenergy

    def calmdot(self, totalmass):
        pass

    def sm_energy(self):
        """ mdot，get WExtracted """
        ienergy = self.iPort.mdot * self.iPort.h
        oenergy = self.oPort.mdot * self.oPort.h
        for ep in self.ePort:
            oenergy += ep.mdot*ep.h
        self.WExtracted = ienergy - oenergy
        self.WExtracted /= (3600.0 * 1000.0)

    def __str__(self):
        result = '\n' + self.name
        result += '\n' + " PORT " + Port.title
        result += '\n' + " iPort " + self.iPort.__str__()
        result += '\n' + " oPort " + self.oPort.__str__()
        i = 0
        for ep in self.ePort:
            result += '\n' + " ePort" + str(i)+" "+ep.__str__()
            i+=1
        result += '\neta(%): \t{:>.2f}'.format(self.eta*100.0)
        result += '\nworkExtracted(kJ): \t{:>.2f}'.format(
            self.workExtracted)
        try:
            result += '\nWExtracted(MW): \t{:>.2f}'.format(self.WExtracted)
        except:
            pass
        return result
