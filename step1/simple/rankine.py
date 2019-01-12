
"""
Step 1: Simple Abstraction of The Ideal Rankine Cycle
                    
       list,dict,function

The ideal rankine cycle as 
   
    ┌─── Node 0 ── Turbine ── Node 1   ──┐
    │                                    │
  Boiler                            Condenser
    │                                    │
    └─── Node 3  ──  Pump  ──  Node 2 ───┘  

 Michael J . Moran. Fundamentals of Engineering Thermodynamics(7th Edition). John Wiley & Sons, Inc. 2011
     Chapter 8 : Vapour Power Systems 
       Example 8.1:Analyzing an Ideal Rankine Cycle  Page 438

Running:

>python rankine.py

License: this code is in the public domain

Author:Cheng Maohua
Email: cmh@seu.edu.cn
"""

from calstate import CalState
from calcycle import CalCycle, CalCondenser

Wcycledot = 100.00     # the net power output of the cycle in MW
p,t,h,s=CalState()  
cycleResults=CalCycle(h,Wcycledot)
cycleResults['mcwdot']=CalCondenser(cycleResults['Qoutdot'])

# Results
print('Example 8.1:Analyzing an Ideal Rankine Cycle') 
print('\t(a) The thermal efficiency for the cycle is %.3f '%(cycleResults['eta']*100),'%')
print('\t(b) The back work ratio is %.3f' %(cycleResults['bwr']*100),'%')
print('\t(c) The mass flow rate of the steam is %.2f' %cycleResults['mdot'],'kg/h.')
print('\t(d) The rate of heat transfer,Qindotinto the working fluid as \
      \n\t\t it passes through the boiler is %.2f' %cycleResults['qindot'],'MW.')
print('\t(e) The rate of heat transfer,Qoutdot from the condensing steam as \
       \n\t\t it passes through the condenser, %.2f' %cycleResults['Qoutdot'],'MW.')
print('\t(f) The mass flow rate of the condenser cooling water is %.2f'%cycleResults['mcwdot'],'kg/h.')