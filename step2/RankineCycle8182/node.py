"""
step 2 : Object-Orientation Abstraction and CSV Textual Representation The Rankine Cycle(Example 8.1,8.2)

License: this code is in the public domain
Cheng Maohua(cmh@seu.edu.cn)

"""
import seuif97 as if97

class Node:

    title = ('{:^6} \t {:^20} \t {:^5}\t {:^7}\t {:^7}\t {:^5} \t {:^7}\t {:^7}'.format
             ("NodeID", "Name", "P", "T", "H", "S", "V", "X"))

    def __init__(self, name, nid):
        self.name = name
        self.nid = nid
        self.p = None
        self.t = None
        self.h = None
        self.s = None
        self.v = None
        self.x = None

    def pt(self):
        self.h = if97.pt2h(self.p, self.t)
        self.s = if97.pt2s(self.p, self.t)
        self.v = if97.pt2v(self.p, self.t)
        self.x = None

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
        result = ('{:^6d} \t {:^20} \t {:>5.2f}\t {:>7.3f}\t {:>7.2f}\t {:>5.2f} \t {:>7.3f}\t {:>5.3}'.format
                  (self.nid, self.name, self.p, self.t, self.h, self.s, self.v, self.x))
        return result
