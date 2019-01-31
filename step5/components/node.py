
"""
Step5: The General Simulator of Rankine Cycle with the  base class of components

    class Node
                      ──┐           ┌──
                        │           │
       component A      ├─⇒ Node ⇒─┤ component B
                        │           │
                      ──┘           └──

json object example:

    {
            "name": "Extracted Steam To Opened FWH",
            "id": 1,
            "p": 0.7,
            "t": null,
            "x": null,
            "fdot":null
    }
  
Author:Cheng Maohua(cmh@seu.edu.cn)
  
"""
import seuif97 as if97


class Node(object):

    title = ('{:^6} \t {:^30} \t {:^5}\t {:^7}\t {:^7}\t {:^5} \t {:^7}\t {:^7}\t {:^5}\t {:^10}'.format
             ("NodeID", "Name", "P", "T", "H", "S", "V", "X", "FDOT", "MDOT"))

    def __init__(self, dictnode):
        self.name = dictnode['name']
        self.nodeid = dictnode['id']
        try: 
           self.p =  float(dictnode['p'])
        except:  
           self.p=None  
        try:   
           self.t =  float(dictnode['t'])
        except:  
           self.t=None 
        try: 
           self.x = float(dictnode['x'])
        except:  
           self.x=None  
      
        self.h = None
        self.s = None
        self.v = None

        try:
           self.fdot =  float(dictnode['fdot'])
        except:
           self.fdot = None
        self.mdot = None

        if self.p!=None and self.t != None:
            self.pt()
        elif self.p!=None and self.x!=None:
            self.px()
        elif self.t!=None and self.x!=None:
            self.tx()

    def calmdot(self, totalmass):
        self.mdot = totalmass * self.fdot

    def pt(self):
        self.h = if97.pt2h(self.p, self.t)
        self.s = if97.pt2s(self.p, self.t)
        self.v = if97.pt2v(self.p, self.t)
        self.x = if97.pt2x(self.p, self.t)

    def ph(self):
        self.t = if97.ph2t(self.p, self.h)
        self.s = if97.ph2s(self.p, self.h)
        self.v = if97.ph2v(self.p, self.h)
        self.x = if97.ph2x(self.p, self.h)

    def ps(self):
        self.t = if97.ps2t(self.p, self.s)
        self.h = if97.ps2h(self.p, self.s)
        self.v = if97.ps2v(self.p, self.s)
        self.x = if97.ps2x(self.p, self.s)

    def hs(self):
        self.t = if97.hs2t(self.h, self.s)
        self.p = if97.hs2p(self.h, self.s)
        self.v = if97.hs2v(self.h, self.s)
        self.x = if97.hs2x(self.h, self.s)

    def px(self):
        self.t = if97.px2t(self.p, self.x)
        self.h = if97.px2h(self.p, self.x)
        self.s = if97.px2s(self.p, self.x)
        self.v = if97.px2v(self.p, self.x)

    def tx(self):
        self.p = if97.tx2p(self.t, self.x)
        self.h = if97.tx2h(self.t, self.x)
        self.s = if97.tx2s(self.t, self.x)
        self.v = if97.tx2v(self.t, self.x)

    def __str__(self):
        result = ('{:^6d} \t {:<30} \t {:>6.3f}\t {:>7.3f}\t {:>7.2f}\t {:>5.2f} \t {:>7.3f}\t {:>5.3}\t {:>6.4f}\t {:>.2f}'.format
                  (self.nodeid, self.name, self.p, self.t, self.h, self.s, self.v, self.x, self.fdot, self.mdot))
        return result
