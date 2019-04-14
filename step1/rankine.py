"""
Step 1 :The Simple Abstraction of The Rankine Cycle 8.1,8.2  with list,dict,function

 Michael J . Moran. Fundamentals of Engineering Thermodynamics(7th Edition). John Wiley & Sons, Inc. 2011
    
    Chapter 8 : Vapour Power Systems 
         1 EXAMPLE 8.1 Analyzing an Ideal Rankine Cycle P438
         2 EXAMPLE 8.2 Analyzing a Rankine Cycle with Irreversibilities P444

The  rankine cycle as 
   
    ┌─── Node 0 ── Turbine ── Node 1   ──┐
    │                                    │
  Boiler                            Condenser
    │                                    │
    └─── Node 3  ──  Pump  ──  Node 2 ───┘  

Run:

>python rankine.py

License: this code is in the public domain

Cheng Maohua(cmh@seu.edu.cn)

"""


from nodes import *
from devices import *
from rankine_cycle import *
from plotTS import *

Nodes = [{'p': 8.0,  't': None, 'x': 1.0,   'h': None, 's': None},
         {'p': 0.008, 't': None, 'x': None, 'h': None, 's': None},
         {'p': 0.008, 't': None, 'x': 0.0,  'h': None, 's': None},
         {'p': 8.0,  't': None, 'x': 0.0,  'h': None, 's': None}
         ]

Nodes = FixeNodesState(Nodes)

# The Devices of Rankine Cycle
Boiler = {'minID': 3, 'moutID': 0, 'qindot': None}
# -- Example 8.1
Turbine = {'minID': 0, 'moutID': 1, 'eta': 1.0, 'wdot': None}
Pump = {'minID': 2, 'moutID': 3, 'eta': 1.0, 'wdot': None}
#  -- Example 8.2
#Turbine = {'minID': 0, 'moutID': 1, 'eta': 0.85, 'wdot': None}
#Pump = {'minID': 2, 'moutID': 3, 'eta': 0.85, 'wdot': None}
Condenser = {'minID': 1, 'moutID': 2, 'qindot': None}

CalDevices(Boiler, Turbine, Pump, Condenser, Nodes)

# Performance
Cycle = {'Wdot': None, 'eta': None, 'bwr': None, 'mdot': None, 'Qindot': None, 'Qoutdot': None,
         'HeatRate': None, 'SteamRate': None}
Cycle = {'Wdot': 100.0}
CalCycle(Boiler, Turbine, Pump, Condenser, Cycle)

print('The Rankine Cycle')

print('\tThe thermal efficiency for the cycle is {:>.2f}%'.format(
    Cycle['eta']*100))
print('\tHeat Rate is {:>.2f}kJ/kWh.'.format(Cycle['HeatRate']))
print('\tSteam Rate is {:>.2f}kg/kWh'.format(Cycle['SteamRate']))

print('\n{:^6}\t {:^8}  {:^7}  {:^7}  {:^7}  {:^7}'.format(
    "Node", "P(MPa)", "T(°C)", "H(kJ/kg)", "S(kJ/kg.K)", "X"))
for i, node in enumerate(Nodes):
    print('{:^6d} \t {:>6.3f} {:>9.2f} {:>10.2f} {:>9.3f} {:>10.2f}'.format(
        i, node['p'],  node['t'],  node['h'],  node['s'], node['x']))

# plot T-S
PlotPrettyTSDiagram(Nodes)