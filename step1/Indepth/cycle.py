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

License: this code is in the public domain

Author:Cheng Maohua
Email: cmh@seu.edu.cn
"""


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
