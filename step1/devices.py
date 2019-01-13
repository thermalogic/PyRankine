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


def SetDevices(States):
    Boiler = {'min': States[3], 'mout': States[0], 'qindot': None}
    Turbine = {'min': States[0], 'mout': States[1], 'wdot': None}
    Pump = {'min': States[2], 'mout': States[3], 'wdot': None}
    return Boiler, Turbine, Pump


def CalDevices(Boiler, Turbine, Pump):
    Boiler['qindot'] = Boiler['mout']['h']-Boiler['min']['h']
    Turbine['wdot'] = Turbine['min']['h'] - Turbine['mout']['h']
    Pump['wdot'] = Pump['mout']['h'] - Pump['min']['h']
