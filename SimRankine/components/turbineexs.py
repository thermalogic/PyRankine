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
        self.iPort = [Port(dictDev['iPort'])]
        self.oPort = [Port(dictDev['oPort'])]
        self.ePort = []
        eportstrs = ['ePort0', 'ePort1', 'ePort2', 'ePort3']
        for epstr in eportstrs:
            if (epstr in dictDev):
                self.ePort.append([Port(dictDev[epstr])])
            else:
                self.ePort.append(None)

        if ('eta' in dictDev):
            self.eta = dictDev['eta']
        else:
            self.eta = None

        # map the name of port to the port obj
        self.portdict = {
            "iPort": self.iPort,
            "oPort": self.oPort,
            "ePort0": self.ePort[0],
            "ePort1": self.ePort[1],
            "ePort2": self.ePort[2],
            "ePort3": self.ePort[3]

        }

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
                    if ep is not None:
                        ep[0].s = self.iPort[0].s
                        ep[0].ps()
                # oPort
                self.oPort[0].s = self.iPort[0].s
                self.oPort[0].ps()
            else:
                # ePort
                for ep in self.ePort:
                    if ep is not None:
                        isosh = ps2h(ep[0].p, self.iPort[0].s)
                        ep[0].h = self.iPort[0].h - \
                            self.eta * (self.iPort[0].h - isosh)
                        ep[0].ph()
                # oPort
                isoh = ps2h(self.oPort[0].p, self.iPort[0].s)
                self.oPort[0].h = self.iPort[0].h - \
                    self.eta * (self.iPort[0].h - isoh)
                self.oPort[0].ph()

        else:
            isosh = ps2h(self.oPort[0].p, self.iPort[0].s)
            isohd = self.iPort[0].h - isosh
            hd = self.iPort[0].h-self.oPort[0].h
            self.eta = hd/isohd

    # sequential-modular approach
    def balance(self):
        """ mass and energy balance of the TurbineEx1
            work=ienergy - oenergy
        """
        totalesfdot = 0
        for ep in self.ePort:
            if ep is not None:
                if ep[0].fdot is None:  # 所有抽汽计算以后才可以计算排汽,所以，只要有抽汽未计算就抛出异常
                    raise ValueError("es.fdot is none")
                else:
                    totalesfdot += ep[0].fdot
        self.oPort[0].fdot = self.iPort[0].fdot-totalesfdot

        ienergy = self.iPort[0].fdot * self.iPort[0].h
        oenergy = self.oPort[0].fdot*self.oPort[0].h
        for ep in self.ePort:
            if ep is not None:
                oenergy += ep[0].fdot*ep[0].h
        self.workExtracted = ienergy - oenergy

    #  equation-oriented approach
    def equation_rows(self):
        """ mass balance row """
        # 1 mass balance row
        colid = [(self.iPort[0].id, 1),
                 (self.oPort[0].id, -1)]
        for ep in self.ePort:
            if ep is not None:
                colid.append((ep[0].id, -1))
        self.rows = [{"a": colid, "b": 0}]

    #  equation-oriented approach
    def energy_fdot(self):
        ienergy = self.iPort[0].fdot * self.iPort[0].h
        oenergy = self.oPort[0].fdot*self.oPort[0].h
        for ep in self.ePort:
            if ep is not None:
                oenergy += ep[0].fdot*ep[0].h
        self.workExtracted = ienergy - oenergy

    def calmdot(self, totalmass):
        pass

    def sm_energy(self):
        """ mdot，get WExtracted """
        ienergy = self.iPort[0].mdot * self.iPort[0].h
        oenergy = self.oPort[0].mdot * self.oPort[0].h
        for ep in self.ePort:
            if ep is not None:
                oenergy += ep[0].mdot*ep[0].h
        self.WExtracted = ienergy - oenergy
        self.WExtracted /= (3600.0 * 1000.0)

    def __str__(self):
        result = '\n' + self.name
        result += '\n' + " PORT " + Port.title
        result += '\n' + " iPort " + self.iPort[0].__str__()
        result += '\n' + " oPort " + self.oPort[0].__str__()
        i = 0
        for ep in self.ePort:
            if ep is not None:
                result += '\n' + " ePort" + str(i)+" "+ep[0].__str__()
                i += 1
        result += '\neta(%): \t{:>.2f}'.format(self.eta*100.0)
        result += '\nworkExtracted(kJ): \t{:>.2f}'.format(
            self.workExtracted)
        try:
            result += '\nWExtracted(MW): \t{:>.2f}'.format(self.WExtracted)
        except:
            pass
        return result
