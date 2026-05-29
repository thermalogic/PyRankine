"""
The PyRankine: the hybrid steady-state simulator of Rankine Cycle

 The port of device

Author:Cheng Maohua  Email: cmh@seu.edu.cn 

"""
import seuif97 as if97


class Port:

    title = f'{"ID":^4} {"P(MPa)":^10} {"T(°C)":^10} {"H(kJ/kg)":^10} {"S(kJ/kg.K)":^10} {"X":^10} {"FDOT":^10} {"MDOT(kg/h)":^10} DESC'

    def __init__(self, dictport):
        """ create the port/node object"""
        self.id = -10
        self.desc = ""

        self.p = None
        self.t = None
        self.x = None
        self.h = None
        self.fdot = None

        self.s = None
        self.v = None
        self.mdot = None

        self.__dict__.update(dictport)
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

    def th(self):
        self.p = if97.th2p(self.t, self.h)
        self.x = if97.th2x(self.t, self.h)
        self.s = if97.th2s(self.t, self.h)
        self.v = if97.th2v(self.t, self.h)

    def hx(self):
        self.t = if97.hx2t(self.h, self.x)
        self.p = if97.hx2p(self.h, self.x)
        self.v = if97.hx2v(self.h, self.x)
        self.s = if97.hx2s(self.h, self.x)

    def __str__(self):
        if self.id != -10:
            result = f'{self.id:^6}'
        else:
            result = '--'

        OutStrs = [{"fspec": '^11.4f', 'prop': self.p, "sspec": '>7'},
                   {"fspec": '^11.2f', 'prop': self.t, "sspec": '>8'},
                   {"fspec": '^11.2f', 'prop': self.h, "sspec": '>10'},
                   {"fspec": '^11.2f', 'prop': self.s, "sspec": '>8'},
                   {"fspec": '^11.4f', 'prop': self.x, "sspec": '>10'},
                   {"fspec": '^11.4f', 'prop': self.fdot, "sspec": '>6'},
                   {"fspec": '^11.2f', 'prop': self.mdot, "sspec": '>8'}
                   ]

        for item in OutStrs:
            try:
                result += f"{item['prop']:{item['fspec']}}"
            except:
                result += f"{'':{item['sspec']}}"

        result += f'{self.desc}'
        return result
