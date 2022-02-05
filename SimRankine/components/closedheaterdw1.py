"""
The PyRankine: the  hybrid steady-state simulator of Rankine Cycle

class Closedheater with drain water inlet  with/without sg inlet

 Closedheaterdw1

                         (No.i)  
                          
       maybe iPort_sg in   │ iPort extracted steam   
              (No.n)  ↓    │
                    ┌─┴────┴──────┐
  feedwater outlet  │             │
  oPort_fw        ← ┼──────N──────┼← iPort_fw (No.j node)
      (No.k)        │             │    feedwater inlet
                    └──┬──────┬───┘  
    delta    iPort_dw  ↑      ↓ oPort_dw  tdeltadw
                 (No. m)      (No. l )



 json object example:
        {    
            "name": "H2",  
            "type": "FWH-CLOSE-DW1",
            "iPort": {},
            "iPort_fw": {},
            "oPort_fw": {},
            "iPort_dw": {},
            "oPort_dw": {},
            "iPort_sg": {},
            "tdelta": 0,
            "tdeltadw": 5.6,
            "eta":0.99
    }

  Rows:
   1. steam mass balance row
   2. feedwater mass balance  row
   3. energy balance row
      
          
 Author:Cheng Maohua  Email: cmh@seu.edu.cn 
"""

from .port import Port
from seuif97 import px2t


class ClosedHeaterDw1:
    """
        Closedheater with drain water inlet and outlet  
        Extracted stream
        maybe: sg inlet
        em and eo
    """

    energy = 'internel'
    devtype = 'FWH-CLOSE-DW1'

    def __init__(self, dictDev):
        """
        Initializes the closed feed water heater with the nodes
        """
        self.name = dictDev['name']

        self.iPort = Port(dictDev['iPort'])
        self.iPort_fw = Port(dictDev['iPort_fw'])
        self.oPort_fw = Port(dictDev['oPort_fw'])
        self.iPort_dw = Port(dictDev['iPort_dw'])
        self.oPort_dw = Port(dictDev['oPort_dw'])
        # sg
        if ('iPort_sg' in dictDev):
            self.iPort_sg = Port(dictDev['iPort_sg'])
        else:
            self.iPort_sg = None
      
        self.tdelta = dictDev['tdelta']
        self.tdeltadw = dictDev['tdeltadw']
        self.eta = dictDev['eta']

        self.heatAdded = None
        self.heatExtracted = None
        self.QExtracted = None
        self.QAdded = None

    def state_fw(self):
        """ oFW """
        if self.iPort_fw.p is not None:
            self.oPort_fw.p = self.iPort_fw.p
        elif self.oPort_fw.p is not None:
            self.iPort_fw.p = self.oPort_fw.p

        self.p_sm_side = self.iPort.p
        self.t_sat = px2t(self.p_sm_side, 0)
        # oFW
        self.oPort_fw.t = self.t_sat - self.tdelta
        self.oPort_fw.pt()

    def state_dw(self):
        """ oDW """
        self.oPort_dw.p = self.p_sm_side
        self.oPort_dw.t = self.iPort_fw.t + self.tdeltadw
        self.oPort_dw.pt()

    def state(self):
        """ oFW,oDW """
        self.state_fw()
        self.state_dw()

    def balance(self):
        """  balance the closed feed water heater  """
        if (self.oPort_fw.fdot != None):
            self.iPort_fw.fdot = self.oPort_fw.fdot
        elif (self.iPort_fw.fdot != None):
            self.oPort_fw.fdot = self.iPort_fw.fdot

        self.heatAdded = self.oPort_fw.fdot * \
            (self.oPort_fw.h - self.iPort_fw.h)
        # eta
        self.heatExtracted = self.heatAdded/self. eta
        # drain water inlet
        self.heatExtracted_dw = self.iPort_dw.fdot * \
            (self.iPort_dw.h - self.oPort_dw.h)
        # extracted stream inlet
        self.heatExtracted_es = self.heatExtracted - self.heatExtracted_dw

        # ---- SG stream inlet ------
        if self.iPort_sg is not None:
            self.heatExtracted_sg = self.iPort_sg.fdot * \
                (self.iPort_sg.h - self.oPort_dw.h)
            self.heatExtracted_es -= self.heatExtracted_sg

        self.iPort.fdot = self.heatExtracted_es / \
            (self.iPort.h - self.oPort_dw.h)
        # oDW
        self.oPort_dw.fdot = self.iPort.fdot+self.iPort_dw.fdot
        # ---- SG stream inlet ------
        if self.iPort_sg is not None:
            self.oPort_dw.fdot += self.iPort_sg.fdot

    #  equation-oriented approach
    def equation_rows(self):
        """ each row {"a":[(colid,val)] "b":val} """
        # 1 steam mass balance row:
        colidms = [(self.iPort.id, -1),
                      (self.iPort_dw.id, -1),
                      (self.oPort_dw.id, 1),
                      ]
        if self.iPort_sg is not None:
            bms = self.iPort_sg.fdot
        else:
            bms = 0
        rowms = {"a":colidms,"b": bms}    
        
        # 2 feedwater mass balance row:
        colidmw = [(self.iPort_fw.id, -1),
                      (self.oPort_fw.id, 1)]
        rowmw = {"a":colidmw,"b": 0}    
        
        # 3 energy balance: row
        colide = [(self.iPort.id, -self.iPort.h),
                     (self.iPort_fw.id, -self.iPort_fw.h),
                     (self.iPort_dw.id, -self.iPort_dw.h),
                     (self.oPort_dw.id, self.oPort_dw.h),
                     (self.oPort_fw.id, self.oPort_fw.h)]
        if self.iPort_sg is not None:
            be = self.iPort_sg.fdot*self.iPort_sg.h
        else:
            be = 0
        rowe = {"a":colide,"b": be}    
        self.rows=[rowms,rowmw,rowe]

    #  equation-oriented approach
    def energy_fdot(self):
        """  Simulates the closed feed water heater  """
        self.heatAdded = self.oPort_fw.fdot * \
            (self.oPort_fw.h - self.iPort_fw.h)
        # eta
        self.heatExtracted = self.iPort.fdot * \
            (self.iPort.h - self.oPort_dw.h)
        # drain water inlet
        self.heatExtracted_dw = self.iPort_dw.fdot * \
            (self.iPort_dw.h - self.oPort_dw.h)
        # extracted stream inlet
        self.heatExtracted_es = self.heatExtracted - self.heatExtracted_dw
        # ---- SG stream inlet ------
        if self.iPort_sg is not None:
            self.heatExtracted_sg = self.iPort_sg.fdot * \
                (self.iPort_sg.h - self.oPort_dw.h)
            self.heatExtracted_es -= self.heatExtracted_sg


    def calmdot(self, totalmass):
        if self.iPort_sg is not None:
            self.iPort_sg.mdot = self.iPort_sg.fdot*totalmass

    def sm_energy(self):
        """ """
        ucovt = 3600.0*1000.0
        self.QExtracted_es = self.iPort.mdot * \
            (self.iPort.h - self.oPort_dw.h) / ucovt
        self.QExtracted_dw = self.iPort_dw.mdot * \
            (self.iPort_dw.h - self.oPort_dw.h) / ucovt
        self.QExtracted = self.QExtracted_es + self.QExtracted_dw
        #  ------ SG stream inlet ------
        if self.iPort_sg is not None:
            self.QExtracted_sg = self.iPort_sg.mdot * \
                (self.iPort_sg.h - self.oPort_dw.h) / ucovt
            self.QExtracted += self.QExtracted_sg
        self.QAdded = self.oPort_fw.mdot * \
            (self.oPort_fw.h - self.iPort_fw.h) / ucovt

    def __str__(self):
        result = '\n'+self.name
        result += '\n'+" PORT "+Port.title
        result += '\n'+" iES"+self.iPort.__str__()
        result += '\n'+" oDW"+self.oPort_dw.__str__()
        result += '\n'+" iFW"+self.iPort_fw.__str__()
        result += '\n'+" iDW"+self.iPort_dw.__str__()
        result += '\n'+" oFW"+self.oPort_fw.__str__()
        # ------ SG stream inlet ------
        if self.iPort_sg is not None:
            result += '\n'+" iSG"+self.iPort_sg.__str__()

        result += '\ndelta(C) \t%.2f' % (self.tdelta)
        result += '\ndeltadw(C) \t%.2f' % (self.tdeltadw)
        result += '\neta(%%) \t%.2f' % (self.eta*100)
        result += '\nheatAdded(kJ): \t%.2f' % (self.heatAdded)
        result += '\nheatExtracted(kJ): \t%.2f' % (self.heatExtracted)
        result += '\n\theatExtracted_es(kJ) \t %.2f' % self.heatExtracted_es
        result += '\n\theatExtracted_dw(kJ) \t%.2f' % self.heatExtracted_dw
        # ------ SG stream inlet ------
        if self.iPort_sg is not None:
            result += '\n\theatExtracted_sg(kJ/kg) \t%.2f' % self.heatExtracted_sg
        try:
            result += '\nQdded(MW) \t%.2f \nQExtracted(MW) \t%.2f ' % (
                self.QExtracted, self.QAdded)
        except:
            pass
        return result
