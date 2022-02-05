"""
The PyRankine: the  hybrid steady-state simulator of Rankine Cycle

class combinedheater:  heater + SG + CDW + HeatWELL

                         (No.i)
                           │ iPort extracted steam
                           │         iPort_sg1     iPort_sg2
                           │         ↓ (No. m)  ↓(No. n)
                    ┌──────┴─────────┴──────────┴──────────────┐
  feedwater outlet  │                                          │
  oPort_fw        ← ┼──│ Heater │←──│ GS │←──│CWP│──│ WELL │───┼←  iPort_fw0 (No.j1 node)(unknow)
      (No.k)        │                                          │←  iPort_fw1 (No.j2 node)(know！)
                    └──────┬───────────────────────────────────┘   feedwater inlet
    delta         iPort_dw ↑
                     (No. l)


 json object example:
        {
            "name": "combinedheater",
            "devtype": "FWH-CLOSE-DW1-SG-CWP-WELL",
            "iPort":{},
            "iPort_fw0":{},
            "iPort_fw1": {},
            "oPort_fw": {},
            "iPort_dw": {},
            "iPort_sg1": {},
            "iPort_sg2": {},
            "tdelta": 0,
            "eta":0.99
        }

Rows:
   1. mass balance row
   2. energy balance  row:
              
Author:Cheng Maohua  Email: cmh@seu.edu.cn
"""

from .port import *
from seuif97 import px2t


class CombinedHeater:
    """
        COMBINED:
          HEATER-CLOSE-DW1
          HEATER-SG
          CWP
          HEATWALL
        em and eo  
    """

    energy = 'internel'
    devtype = 'FWH-CLOSE-DW1-SG-CWP-WELL'

    def __init__(self, dictDev):
        """
        Initializes -SG-WALL
        """
        self.name = dictDev['name']

        self.iPort = [Port(dictDev['iPort'])]
        self.iPort_fw0 = [Port(dictDev['iPort_fw0'])]
        self.iPort_fw1 = [Port(dictDev['iPort_fw1'])]
        self.oPort_fw = [Port(dictDev['oPort_fw'])]
        self.iPort_dw = [Port(dictDev['iPort_dw'])]
        # ------- isg -----------
        self.iPort_sg1 = [Port(dictDev['iPort_sg1'])]
        self.iPort_sg2 = [Port(dictDev['iPort_sg2'])]

        # map the name of port to the port obj
        self.portdict = {
            "iPort": self.iPort,
            "iPort_fw0": self.iPort_fw0,
            "iPort_fw1": self.iPort_fw1,
            "oPort_fw": self.oPort_fw,
            "iPort_dw": self.iPort_dw,
            "iPort_sg1": self.iPort_sg1,
            "iPort_sg2": self.iPort_sg2
        }

        self.tdelta = dictDev['tdelta']
        self.eta = dictDev['eta']

        self.heatAdded = None
        self.heatExtracted = None
        self.QExtracted = None
        self.QAdded = None

    def state_fw(self):
        """ oFW """
        self.p_sm_side = self.iPort[0].p
        self.t_sat = px2t(self.p_sm_side, 0)
        # oFW
        self.oPort_fw[0].t = self.t_sat - self.tdelta
        self.oPort_fw[0].pt()

    def state_dw(self):
        pass

    def state(self):
        """ oFW,oDW """
        self.state_fw()
        self.state_dw()

    def balance(self):
        """  balance the closed feed water heater 
         self.iPort[0].fdot
         self.iPort_fw0[0].fdot

        """

        qfw0 = self.oPort_fw[0].h-self.iPort_fw0[0].h
        qes1 = self.iPort[0].h-self.oPort_fw[0].h

        a = self.eta*qes1+qfw0

        self.heatAdded_iFW1 = self.iPort_fw1[0].fdot * \
            (self.oPort_fw[0].h - self.iPort_fw1[0].h)
        b1 = (self.oPort_fw[0].fdot-self.iPort_dw[0].fdot-self.iPort_sg1[0].fdot -
              self.iPort_sg2[0].fdot-self.iPort_fw1[0].fdot)*qfw0

        self.heatExtracted_dw = self.iPort_dw[0].fdot * \
            (self.iPort_dw[0].h-self.oPort_fw[0].h)
        self.heatExtracted_sg1 = self.iPort_sg1[0].fdot * \
            (self.iPort_sg1[0].h - self.oPort_fw[0].h)
        self.heatExtracted_sg2 = self.iPort_sg2[0].fdot * \
            (self.iPort_sg2[0].h - self.oPort_fw[0].h)
        self.heatExtracted_sg = self.heatExtracted_sg1+self.heatExtracted_sg2
        b = self.heatAdded_iFW1 + b1 - self.eta * \
            (self.heatExtracted_dw + self.heatExtracted_sg)
        self.iPort[0].fdot = b/a

        self.heatExtracted_es = self.iPort[0].fdot * \
            (self.iPort[0].h - self.oPort_fw[0].h)
        self.heatExtracted = self.heatExtracted_es + \
            self.heatExtracted_dw + self.heatExtracted_sg

        # mass balance
        self.iPort_fw0[0].fdot = self.oPort_fw[0].fdot-self.iPort[0].fdot-self.iPort_dw[0].fdot - \
            self.iPort_sg1[0].fdot-self.iPort_sg2[0].fdot - \
            self.iPort_fw1[0].fdot
        self.heatAdded_iFW0 = self.iPort_fw1[0].fdot * \
            (self.oPort_fw[0].h - self.iPort_fw0[0].h)
        self.heatAdded = self.heatAdded_iFW0+self.heatAdded_iFW1

       #  equation-oriented approach
    def equation_rows(self):
        """ each row {"a":[(colid,val)] "b":val} """

        # 1 mass balance row:
        colidm = [(self.iPort[0].id, -1),
                  (self.iPort_fw0[0].id, -1),
                  (self.iPort_fw1[0].id, -1),
                  (self.iPort_dw[0].id, -1),
                  (self.oPort_fw[0].id, 1)
                  ]
        bm = self.iPort_sg1[0].fdot + self.iPort_sg2[0].fdot
        rowm = {"a": colidm, "b": bm}
        # 2 energy balance row
        colide = [(self.iPort[0].id, -self.iPort[0].h),
                  (self.iPort_fw0[0].id, -self.iPort_fw0[0].h),
                  (self.iPort_fw1[0].id, -self.iPort_fw1[0].h),
                  (self.iPort_dw[0].id, -self.iPort_dw[0].h),
                  (self.oPort_fw[0].id, self.oPort_fw[0].h)]

        be = self.iPort_sg1[0].fdot*self.iPort_sg1[0].h + \
            self.iPort_sg2[0].fdot*self.iPort_sg2[0].h
        rowe = {"a": colide,  "b": be}

        self.rows = [rowm, rowe]

      #  equation-oriented approach
    def energy_fdot(self):
        """  ch  """
        self.heatExtracted_sg1 = self.iPort_sg1[0].fdot * \
            (self.iPort_sg1[0].h - self.oPort_fw[0].h)
        self.heatExtracted_sg2 = self.iPort_sg2[0].fdot * \
            (self.iPort_sg2[0].h - self.oPort_fw[0].h)
        self.heatExtracted_sg = self.heatExtracted_sg1+self.heatExtracted_sg2

        self.heatExtracted_dw = self.iPort_dw[0].fdot * \
            (self.iPort_dw[0].h-self.oPort_fw[0].h)

        self.heatExtracted_es = self.iPort[0].fdot * \
            (self.iPort[0].h - self.oPort_fw[0].h)

        self.heatExtracted = self.heatExtracted_es + \
            self.heatExtracted_dw + self.heatExtracted_sg

        self.heatAdded_iFW1 = self.iPort_fw1[0].fdot * \
            (self.oPort_fw[0].h - self.iPort_fw1[0].h)
        self.heatAdded_iFW0 = self.iPort_fw1[0].fdot * \
            (self.oPort_fw[0].h - self.iPort_fw0[0].h)
        self.heatAdded = self.heatAdded_iFW0+self.heatAdded_iFW1

    def calmdot(self, totalmass):
        self.iPort_sg1[0].mdot = self.iPort_sg1[0].fdot * totalmass
        self.iPort_sg2[0].mdot = self.iPort_sg2[0].fdot * totalmass

    def sm_energy(self):
        """ mass """
        ucovt = 3600.0*1000.0
        self.QExtracted_es = self.iPort[0].mdot * \
            (self.iPort[0].h - self.oPort_fw[0].h) / ucovt
        self.QExtracted_dw = self.iPort_dw[0].mdot * \
            (self.iPort_dw[0].h - self.oPort_fw[0].h) / ucovt
        #  ------ SG stream inlet ------
        self.QExtracted_sg1 = self.iPort_sg1[0].mdot * \
            (self.iPort_sg1[0].h - self.oPort_fw[0].h) / ucovt
        self.QExtracted_sg2 = self.iPort_sg2[0].mdot * \
            (self.iPort_sg2[0].h - self.oPort_fw[0].h) / ucovt
        self.QExtracted_sg = self.QExtracted_sg1+self.QExtracted_sg2
        #  ------ SG stream inlet ------
        self.QExtracted = self.QExtracted_es + self.QExtracted_dw + self.QExtracted_sg
        self.QAdded = self.iPort_fw0[0].mdot * \
            (self.oPort_fw[0].h - self.iPort_fw0[0].h) / ucovt
        self.QAdded += self.iPort_fw1[0].mdot * \
            (self.oPort_fw[0].h - self.iPort_fw1[0].h) / ucovt

    def __str__(self):
        result = '\n'+self.name
        result += '\n'+" PORT "+Port.title
        result += '\n'+" iES "+self.iPort[0].__str__()
        result += '\n'+" iFW0 "+self.iPort_fw0[0].__str__()
        result += '\n'+" iFW1 "+self.iPort_fw1[0].__str__()
        result += '\n'+" iDW "+self.iPort_dw[0].__str__()
        result += '\n'+" oFW "+self.oPort_fw[0].__str__()
        # ------ SG stream inlet ------
        result += '\n'+" iSG1 "+self.iPort_sg1[0].__str__()
        result += '\n'+" iSG2 "+self.iPort_sg2[0].__str__()

        result += '\ndelta(C) \t%.2f' % (self.tdelta)
        result += '\neta(%%) \t%.2f' % (self.eta*100)
        result += '\nheatAdded(kJ): \t%.2f' % (self.heatAdded)
        result += '\nheatExtracted(kJ): \t%.2f' % (self.heatExtracted)
        result += '\n\theatExtracted_es(kJ) \t %.2f' % self.heatExtracted_es
        result += '\n\theatExtracted_dw(kJ) \t%.2f' % self.heatExtracted_dw
        # ------ SG stream inlet ------
        result += '\n\theatExtracted_sg(kJ) \t%.2f' % self.heatExtracted_sg
        try:
            result += '\nQdded(MW) \t%.2f \nQExtracted(MW) \t%.2f ' % (
                self.QExtracted, self.QAdded)
        except:
            pass
        return result
