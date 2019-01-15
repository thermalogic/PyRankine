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


def FixeNodesState(Nodes):

    # State  1, Node 0
    Nodes[0]['p'] = 8.0
    p = Nodes[0]['p']
    Nodes[0]['t'] = px2t(p, 1)
    Nodes[0]['h'] = px2h(p, 1)
    Nodes[0]['s'] = px2s(p, 1)

    # State  2, Node 1
    Nodes[1]['p'] = 0.008
    Nodes[1]['s'] = Nodes[0]['s']
    p = Nodes[1]['p']
    s = Nodes[1]['s']
    Nodes[1]['t'] = ps2t(p, s)
    Nodes[1]['h'] = ps2h(p, s)

    # State 3 , Node 2 saturated liquid at 0.008 MPa
    Nodes[2]['p'] = 0.008
    p = Nodes[2]['p']
    Nodes[2]['t'] = px2t(p, 0)
    Nodes[2]['h'] = px2h(p, 0)  # kj/kg
    Nodes[2]['s'] = px2s(p, 0)

    # State 4 , Node 3
    Nodes[3]['p'] = Nodes[0]['p']
    Nodes[3]['s'] = Nodes[2]['s']
    p = Nodes[3]['p']
    s = Nodes[3]['s']
    Nodes[3]['h'] = ps2h(p, s)
    Nodes[3]['t'] = ps2t(p, s)

    return Nodes

def CalDevices(Nodes):
    # Boiler
    Boiler={'min':Nodes[3],'mout':Nodes[0],'qindot':None}
    Boiler['qindot']=Boiler['mout']['h']-Boiler['min']['h']
    
    # Turbine
    Turbine={'min':Nodes[0],'mout':Nodes[1],'wdot':None}       
    Turbine['wdot']=  Turbine['min']['h']- Turbine['mout']['h']        
    
    # Pump
    Pump = {'min': Nodes[2], 'mout': Nodes[3], 'wdot': None}
    Pump['wdot']=  Pump['mout']['h']- Pump['min']['h'] 
    return Boiler,Turbine,Pump 


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
    Nodes = [{} for i in range(4)]
    Nodes = FixeNodesState(Nodes)

    Boiler, Turbine, Pump = CalDevices(Nodes)
  
    Cycle = {'Wdot': 100.0}
    CalCycle(Boiler, Turbine, Pump, Cycle)

    print('{:^6}\t {:^7}  {:^7}  {:^7}  {:^7}'.format("Node", "P(MPa)", "T(°C)", "H(kJ/kg)", "S(kJ/kg.K)"))
    i=0
    for node in  Nodes:
        print('{:^6d} \t {:>5.3f} {:>9.2f} {:>10.2f} {:>9.3f}'.format(i, node['p'],  node['t'],  node['h'],  node['s']))
        i+=1
    
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(Cycle)
    pp.pprint(Boiler)
    pp.pprint(Turbine)
    pp.pprint(Pump)

  # plot T-S
    PlotTSDiagram(Nodes)


if __name__ == '__main__':
    main()
