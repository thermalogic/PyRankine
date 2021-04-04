"""
The PyRankine: the  hybrid steady-state simulator of Rankine Cycle

class OpenedheaterDw1

                       ↓   iPort extracted steam (No. i)
                   ┌───┴───┐
 feedwater         │       │
 oPort_fw        ← ┤       │← iPort_fw  feedwater (No. j)
  (No. k node)     │       │
                   └───┬───┘
                       ↑      iPort_dw exhausted steam
                           (No. m) 

 json object example:
        {    
            "name": "The Open feed water heater 1",  
            "devtype": "FWH-OPEN-DW1",
            "iPort": {},
            "iPort_fw":{}, 
            "oPort_fw":{},
            "iPort_dw": {},
             "eta":0.99

         }

Rows:
   1. mass balance row
   2. energy balance  row
              
Author: Cheng Maohua(cmh@seu.edu.cn)    
 
"""
from seuif97 import px2t
from .port import *


class OpenedheaterDw1:
    """
    sm and eo
      The Opened feedwater heater class with 1 drain water inlet
    """
    energy = "internel"
    type = "FWH-OPEN-DW1"

    # TDDO : modified to fit of inNode_dw=None
    def __init__(self, dictDev):
        """
        Initializes the Open feed water with the conditions
        """
        self.name = dictDev['name']
        self.iPort = [Port(dictDev['iPort'])]
        self.iPort_fw = [Port(dictDev['iPort_fw'])]
        self.oPort_fw = [Port(dictDev['oPort_fw'])]
        self.iPort_dw = [Port(dictDev['iPort_dw'])]
        if ("eta" in dictDev):
            self.eta = dictDev['eta']
        else:
            self.eta = 1.00

        # map the name of port to the port obj
        self.portdict = {
            "iPort": self.iPort,
            "iPort_fw": self.iPort_fw,
            "oPort_fw": self.oPort_fw,
            "iPort_dw": self.iPort_dw

        }

        self.heatAdded = 0
        self.heatExtracted_s = None
        self.heatExtracted_d = None
        self.heatExtracted = None
        self.QExtracted_s = None
        self.QExtracted_d = None

    def state_fw(self):
        """ oPort_fw """
        self.p_sm_side = self.iPort[0].p
        self.t_sat = px2t(self.p_sm_side, 0)
        self.oPort_fw[0].p = self.p_sm_side
        self.oPort_fw[0].t = self.t_sat
        self.oPort_fw[0].x = 0
        self.oPort_fw[0].px()
        self.tdelta = 0

    def state_dw(self):
        pass

    def state(self):
        self.state_fw()
        self.state_dw()

    # sequential-modular approach
    def balance(self):
        """
        balance the opened feedwater heater  
        """
        # 1 1kd 疏水放热
        qdw1 = self.iPort_dw[0].h - self.oPort_fw[0].h
        # 2 1kg 抽汽放热
        qes1 = self.iPort[0].h - self.oPort_fw[0].h
        # 1kg给水吸热
        qfw1 = self.oPort_fw[0].h - self.iPort_fw[0].h

        # eta
        a = self.oPort_fw[0].fdot*qfw1 - \
            self.iPort_dw[0].fdot*(self.eta*qdw1+qfw1)
        b = qes1*self.eta+qfw1
        self.iPort[0].fdot = a/b
        self.iPort_fw[0].fdot = self.oPort_fw[0].fdot - \
            self.iPort[0].fdot-self.iPort_dw[0].fdot

        # heat
        self.heatExtracted_dw = self.iPort_dw[0].fdot * qdw1
        self.heatExtracted_es = self.iPort[0].fdot * qes1
        self.heatExtracted = self.heatExtracted_dw + self.heatExtracted_es
        # heatAddedto feedwater
        self.heatAdded = self.iPort_fw[0].fdot * \
            (self.oPort_fw[0].h - self.iPort_fw[0].h)

    #  equation-oriented approach
    def equation_rows(self):
        """ masss ane erergy equations"""
        # 1 mass balance row
        colidm = [(self.iPort[0].id, 1),
                  (self.iPort_fw[0].id, 1),
                  (self.iPort_dw[0].id, 1),
                  (self.oPort_fw[0].id, -1)]
        rowm = {"a": colidm, "b": 0}
        # 2 energy balance row
        colide = [(self.iPort[0].id, self.iPort[0].h),
                  (self.iPort_fw[0].id, self.iPort_fw[0].h),
                  (self.iPort_dw[0].id, self.iPort_dw[0].h),
                  (self.oPort_fw[0].id, -self.oPort_fw[0].h)]
        rowe = {"a": colide, "b": 0}
        self.rows = [rowm, rowe]

    #  equation-oriented approach
    def energy_fdot(self):
        """
        Simulates the opened feedwater heater  
        """
        # heat
        qdw1 = self.iPort_dw[0].h - self.oPort_fw[0].h
        # 2 1kg 抽汽放热
        qes1 = self.iPort[0].h - self.oPort_fw[0].h
        # 1kg给水吸热
        qfw1 = self.oPort_fw[0].h - self.iPort_fw[0].h
        self.heatExtracted_dw = self.iPort_dw[0].fdot * qdw1
        self.heatExtracted_es = self.iPort[0].fdot * qes1
        self.heatExtracted = self.heatExtracted_dw + self.heatExtracted_es
        # heatAddedto feedwater
        self.heatAdded = self.iPort_fw[0].fdot * \
            (self.oPort_fw[0].h - self.iPort_fw[0].h)

    def calmdot(self, totalmass):
        pass

    def sm_energy(self):
        ucovt = 3600.0*1000.0
        self.QExtracted_es = self.iPort[0].mdot * \
            (self.iPort[0].h - self.oPort_fw[0].h)/ucovt
        # drain water inlet
        self.QExtracted_dw = self.iPort_dw[0].mdot * \
            (self.iPort_dw[0].h - self.oPort_fw[0].h)/ucovt
        self.QExtracted = self.QExtracted_es + self.QExtracted_dw

        self.QAdded = self.iPort_fw[0].mdot * \
            (self.oPort_fw[0].h - self.iPort_fw[0].h)/ucovt

    def __str__(self):
        result = '\n' + self.name
        result += '\n'+" PORT " + Port.title
        result += '\n'+"iES"+self.iPort[0].__str__()
        result += '\n'+"iFW"+self.iPort_fw[0].__str__()
        result += '\n'+"oFW"+self.oPort_fw[0].__str__()
        result += '\n'+"iDW"+self.iPort_dw[0].__str__()

        result += '\neta(%%) \t%.2f' % (self.eta*100)
        result += '\nheatAdded(kJ) \t%.2f' % self.heatAdded
        result += '\nheatExtracted(kJ) \t%.2f' % self.heatExtracted
        result += '\n\theatExtracted_es(kJ) \t %.2f' % self.heatExtracted_es
        result += '\n\theatExtracted_dw(kJ) \t%.2f' % self.heatExtracted_dw
        try:
            result += '\nQAdded(MW) \t%.2f' % self.QAdded
            result += '\nQExtracted(MW)  \t%.2f' % self.QExtracted
            result += '\n\tQExtracted_es(MW) \t%.2f' % self.QExtracted_es
            result += '\n\tQExtracted_dw(MW)\t%.2f' % self.QExtracted_dw
        except:
            pass
        return result
