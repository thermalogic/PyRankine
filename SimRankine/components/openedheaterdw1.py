"""
The PyRankine: the  hybrid steady-state simulator of Rankine Cycle

class OpenedHeaterDw1

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


class OpenedHeaterDw1:
    """
    sm and eo
      The Opened feedwater heater class with 1 drain water inlet
    """
    energy = "internal"
    devtype = "FWH-OPEN-DW1"

    # TODO : modified to fit of inNode_dw=None
    def __init__(self, dictDev):
        """
        Initializes the Open feed water with the conditions
        """
        self.name = dictDev['name']
        self.iPort = Port(dictDev['iPort'])
        self.iPort_fw = Port(dictDev['iPort_fw'])
        self.oPort_fw = Port(dictDev['oPort_fw'])
        self.iPort_dw = Port(dictDev['iPort_dw'])
        if ("eta" in dictDev):
            self.eta = dictDev['eta']
        else:
            self.eta = 1.00

        self.heatAdded = 0
        self.heatExtracted_s = None
        self.heatExtracted_d = None
        self.heatExtracted = None
        self.QExtracted_s = None
        self.QExtracted_d = None

    def state_fw(self):
        """ oPort_fw """
        self.p_sm_side = self.iPort.p
        self.t_sat = px2t(self.p_sm_side, 0)
        self.oPort_fw.p = self.p_sm_side
        self.oPort_fw.t = self.t_sat
        self.oPort_fw.x = 0
        self.oPort_fw.px()
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
        # 1 1kg dw 
        qdw1 = self.iPort_dw.h - self.oPort_fw.h
        # 2 1kg es
        qes1 = self.iPort.h - self.oPort_fw.h
        # 1kg fw
        qfw1 = self.oPort_fw.h - self.iPort_fw.h

        # eta
        a = self.oPort_fw.fdot*qfw1 - \
            self.iPort_dw.fdot*(self.eta*qdw1+qfw1)
        b = qes1*self.eta+qfw1
        self.iPort.fdot = a/b
        self.iPort_fw.fdot = self.oPort_fw.fdot - \
            self.iPort.fdot-self.iPort_dw.fdot

        # heat
        self.heatExtracted_dw = self.iPort_dw.fdot * qdw1
        self.heatExtracted_es = self.iPort.fdot * qes1
        self.heatExtracted = self.heatExtracted_dw + self.heatExtracted_es
        # heatAddedto feedwater
        self.heatAdded = self.iPort_fw.fdot * \
            (self.oPort_fw.h - self.iPort_fw.h)

    #  equation-oriented approach
    def equation_rows(self):
        """ mass and energy equations"""
        # 1 mass balance row
        colidm = [(self.iPort.id, 1),
                  (self.iPort_fw.id, 1),
                  (self.iPort_dw.id, 1),
                  (self.oPort_fw.id, -1)]
        rowm = {"a": colidm, "b": 0}
        # 2 energy balance row
        colide = [(self.iPort.id, self.iPort.h),
                  (self.iPort_fw.id, self.iPort_fw.h),
                  (self.iPort_dw.id, self.iPort_dw.h),
                  (self.oPort_fw.id, -self.oPort_fw.h)]
        rowe = {"a": colide, "b": 0}
        self.rows = [rowm, rowe]

    #  equation-oriented approach
    def energy_fdot(self):
        """
        Simulates the opened feedwater heater  
        """
        # heat
        qdw1 = self.iPort_dw.h - self.oPort_fw.h
        # 2 1kg es
        qes1 = self.iPort.h - self.oPort_fw.h
        # 1kg fw
        qfw1 = self.oPort_fw.h - self.iPort_fw.h
        self.heatExtracted_dw = self.iPort_dw.fdot * qdw1
        self.heatExtracted_es = self.iPort.fdot * qes1
        self.heatExtracted = self.heatExtracted_dw + self.heatExtracted_es
        # heatAddedto feedwater
        self.heatAdded = self.iPort_fw.fdot * \
            (self.oPort_fw.h - self.iPort_fw.h)

    def calmdot(self, totalmass):
        pass

    def sm_energy(self):
        ucovt = 3600.0*1000.0
        self.QExtracted_es = self.iPort.mdot * \
            (self.iPort.h - self.oPort_fw.h)/ucovt
        # drain water inlet
        self.QExtracted_dw = self.iPort_dw.mdot * \
            (self.iPort_dw.h - self.oPort_fw.h)/ucovt
        self.QExtracted = self.QExtracted_es + self.QExtracted_dw

        self.QAdded = self.iPort_fw.mdot * \
            (self.oPort_fw.h - self.iPort_fw.h)/ucovt

    def __str__(self):
        result = '\n' + self.name
        result += '\n'+" PORT " + Port.title
        result += '\n'+"iES"+self.iPort.__str__()
        result += '\n'+"iFW"+self.iPort_fw.__str__()
        result += '\n'+"oFW"+self.oPort_fw.__str__()
        result += '\n'+"iDW"+self.iPort_dw.__str__()

        result += f'\neta(%) \t{self.eta*100:.2f}'
        result += f'\nheatAdded(kJ) \t{self.heatAdded:.2f}'
        result += f'\nheatExtracted(kJ) \t{self.heatExtracted:.2f}'
        result += f'\n\theatExtracted_es(kJ) \t {self.heatExtracted_es:.2f}'
        result += f'\n\theatExtracted_dw(kJ) \t{self.heatExtracted_dw:.2f}'
        try:
            result += f'\nQAdded(MW) \t{self.QAdded:.2f}'
            result += f'\nQExtracted(MW)  \t{self.QExtracted:.2f}'
            result += f'\n\tQExtracted_es(MW) \t{self.QExtracted_es:.2f}'
            result += f'\n\tQExtracted_dw(MW)\t{self.QExtracted_dw:.2f}'
        except:
            pass
        return result
