"""
Step 1 :The Basic Abstraction of The Ideal Rankine Cycle with   list,dict,function

The ideal rankine cycle as 
   
    ┌─── Node 0 ── Turbine ── Node 1   ──┐
    │                                    │
  Boiler                            Condenser
    │                                    │
    └─── Node 3  ──  Pump  ──  Node 2 ───┘  

 Michael J . Moran. 
     Fundamentals of Engineering Thermodynamics(7th Edition). John Wiley & Sons, Inc. 2011
         Chapter 8 : Vapour Power Systems 
         Example 8.1:Analyzing an Ideal Rankine Cycle  Page 438

Run:

>python rankine.py

License: this code is in the public domain

Cheng Maohua(cmh@seu.edu.cn)

"""
import pprint
from seuif97 import *

from plotTS import *


def FixeStates(States):

    # State  1, Node 0
    States[0]['p'] = 8.0
    p = States[0]['p']
    States[0]['t'] = px2t(p, 1)
    States[0]['h'] = px2h(p, 1)
    States[0]['s'] = px2s(p, 1)

    # State  2, Node 1
    States[1]['p'] = 0.008
    States[1]['s'] = States[0]['s']
    p = States[1]['p']
    s = States[1]['s']
    States[1]['t'] = ps2t(p, s)
    States[1]['h'] = ps2h(p, s)

    # State 3 , Node 2 saturated liquid at 0.008 MPa
    States[2]['p'] = 0.008
    p = States[2]['p']
    States[2]['t'] = px2t(p, 0)
    States[2]['h'] = px2h(p, 0)  # kj/kg
    States[2]['s'] = px2s(p, 0)

    # State 4 , Node 3
    States[3]['p'] = States[0]['p']
    States[3]['s'] = States[2]['s']
    p = States[3]['p']
    s = States[3]['s']
    States[3]['h'] = ps2h(p, s)
    States[3]['t'] = ps2t(p, s)

    return States


def SetDevices(States):
    Boiler = {'min': States[3], 'mout': States[0], 'qindot': None}
    Turbine = {'min': States[0], 'mout': States[1], 'wdot': None}
    Pump = {'min': States[2], 'mout': States[3], 'wdot': None}
    return Boiler, Turbine, Pump


def CalDevices(Boiler, Turbine, Pump):
    Boiler['qindot'] = Boiler['mout']['h']-Boiler['min']['h']
    Turbine['wdot'] = Turbine['min']['h'] - Turbine['mout']['h']
    Pump['wdot'] = Pump['mout']['h'] - Pump['min']['h']


def CalCycle(Boiler, Turbine, Pump, Cycle):
    # thermal efficiency
    Cycle['eta'] = (Turbine['wdot'] - Pump['wdot']) / Boiler['qindot']
    # Part(b)
    Cycle['bwr'] = Turbine['wdot']/Pump['wdot']
    # Part(c)
    Cycle['mdot'] = (Cycle['Wdot']*10**3*3600)/(Turbine['wdot'] -
                                                Pump['wdot'])       # mass flow rate in kg/h
    # Part(d)
    Boiler['Qindot'] = Cycle['mdot']*Boiler['qindot'] / \
        (3600*10**3)                     # in MW
    Cycle['Qindot'] = Boiler['Qindot']


def main():
    States = [{} for i in range(4)]
    States = FixeStates(States)

    Boiler, Turbine, Pump = SetDevices(States)
    CalDevices(Boiler, Turbine, Pump)

    Cycle = {'Wdot': 100.0}
    CalCycle(Boiler, Turbine, Pump, Cycle)

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(Cycle)
    pp.pprint(Boiler)
    pp.pprint(Turbine)
    pp.pprint(Pump)

  # plot T-S
    PlotTSDiagram(States)


if __name__ == '__main__':
    main()
