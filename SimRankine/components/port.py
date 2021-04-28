"""
The PyRankine: the hybrid steady-state simulator of Rankine Cycle

 The port of device

Author:Cheng Maohua  Email: cmh@seu.edu.cn 

"""
import seuif97 as if97


class Port:

    title = ('{:^4} \t{:<3} \t{:>3} {:>10} {:>10} \t{:^6} \t{:^6} \t{:>10} \t\t{:^15} '.format
             ("ID", "P(MPa)", "T(°C)", "H(kJ/kg)", "S(kJ/kg.K)",  "X", "FDOT", "MDOT(kg/h)", "DESC"))

    kwargs = {'p': None, 't': None, 'x': None,  'h': None, 'fdot': None}

    def __init__(self, dictport):
        """ create the port/node object"""
        kwargs = Port.kwargs.copy()
        kwargs.update(dictport)
        for key in Port.kwargs.keys():
            if type(kwargs[key]) is int:
                kwargs[key] = float(kwargs[key])
        self.__dict__.update(kwargs)

        self.id=-10
        self.desc=""
        self.s = None
        self.v = None
        self.mdot = None

        if self.p is not None and self.t is not None:
            self.pt()
        elif self.p is not None and self.x is not None:
            self.px()
        elif self.t is not None and self.x is not None:
            self.tx()
        elif self.h is not None and self.p is not None:
            self.ph()
        elif self.h is not None and self.t is not None:
            self.th()
        elif self.h is not None and self.x is not None:
            self.hx()

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
        if (self.id != -10):
            result = '{:^6}'.format(self.id)
        else:
            result = ' -- '

        OutStrs = [{"fstr": '\t{:>7.4}', 'prop': self.p, "sstr": '\t{:>7}'},
                   {"fstr": '\t{:>8.2f}', 'prop': self.t, "sstr": '\t{:>8}'},
                   {"fstr": '{:>10.2f}', 'prop': self.h, "sstr": '\t{:>10}'},
                   {"fstr": '\t{:>8.3f}',  'prop': self.s, "sstr": '\t{:>8}'},
                   {"fstr": '\t{:>6.4f}', 'prop': self.x, "sstr": '\t{:>10}'},
                   {"fstr": '\t\t{:>6.4f}',  'prop': self.fdot, "sstr": '\t{:>6}'},
                   {"fstr": '\t{:>8.2f}',  'prop': self.mdot, "sstr": '\t{:>8}'}
                   ]

        for item in OutStrs:
            try:
                result += item["fstr"].format(item["prop"])
            except:
                result += item["sstr"].format("")

        result += '\t\t{:<30}'.format(self.desc)
        return result
