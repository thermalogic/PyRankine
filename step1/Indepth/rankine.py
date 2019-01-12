"""
Step 1 :The In-depth Abstraction of The Ideal Rankine Cycle

       list,dict,function

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

Author:Cheng Maohua
Email: cmh@seu.edu.cn
"""
import pprint

from cycle import *
from devices import *
from wstates import FixeStates

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
