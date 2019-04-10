"""
step 2 : Object-Orientation Abstraction and CSV Textual Representation The Rankine Cycle(Example 8.1,8.2)

The rankine cycle as 
   
    ┌─── Node 0 ── Turbine ── Node 1   ──┐
    │                                    │
  Boiler                            Condenser
    │                                    │
    └─── Node 3  ──  Pump  ──  Node 2 ───┘  

 Michael J . Moran.  Fundamentals of Engineering Thermodynamics(7th Edition). John Wiley & Sons, Inc. 2011
    
    Chapter 8 : Vapour Power Systems 
    
        Example 8.1: Analyzing an Ideal Rankine Cycle  Page 438
        Example 8.2: Analyzing a Rankine Cycle with Irreversibilities Page 444

Run:

>python rankine.py

License: this code is in the public domain

Cheng Maohua(cmh@seu.edu.cn)

"""

import glob

from rankine_cycle import *

nds_filesname = glob.glob(r'./data/rankine8[0-9]-nds.csv')
dev_filesname = glob.glob(r'./data/rankine??-des.csv')

cycle = []
for i in range(len(nds_filesname)):
    cycle.append(SimRankineCycle(nds_filesname[i], dev_filesname[i]))
    cycle[i].CycleSimulator()
    # Specified Net Output Power

for i in range(len(nds_filesname)):
    cycle[i].SimulatorOutput()