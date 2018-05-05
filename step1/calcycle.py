"""
Step 1  

Step-by-step codes of the ideal rankine cycle simulator to demonstrate: 

   Data Structures+ Algorithms = Programs

    list, dict,function

The ideal rankine cycle as 
   
    ┌─── Node 0 ── Turbine ── Node 1   ──┐
    │                                    │
  Boiler                            Condenser
    │                                    │
    └─── Node 3  ──  Pump  ──  Node 2 ───┘  

 Michael J . Mora. 
     Fundamentals of Engineering Thermodynamics(7th Edition). John Wiley & Sons, Inc. 2011
     Chapter 8 : Vapour Power Systems Example 8.1:Analyzing an Ideal Rankine Cycle  Page 438

License: this code is in the public domain

Author:Cheng Maohua
Email: cmh@seu.edu.cn
"""
from seuif97 import *

def CalCycle(h,Wcycledot):
    
    results={}
    
    # Part(a)
    # Mass and energy rate balances for control volumes 
    # around the turbine and pump give, respectively

    # turbine
    results['wtdot'] = h[0] - h[1]
    # pump
    results['wpdot'] = h[3]-h[2]

    # The rate of heat transfer to the working fluid as it passes 
    # through the boiler is determined using mass and energy rate balances as
    results['qindot'] = h[0]-h[3]

    # thermal efficiency
    results['eta'] = ( results['wtdot'] -results['wpdot'])/ results['qindot']    

    # Part(b)
    # back work ratio：bwr, defined as the ratio of the pump work input to the work 
    # developed by the turbine.
    results['bwr'] =results['wpdot']/results['wtdot']                                   # 

    # Part(c)
    results['mdot'] = (Wcycledot*10**3*3600)/((h[0]-h[1])-(h[3]-h[2]))       # mass flow rate in kg/h
 
    # Part(d)
    results['Qindot'] = results['mdot']*results['qindot']/(3600*10**3)                     # in MW

    # Part(e)
    results['Qoutdot'] = results['mdot']*(h[1]-h[2])/(3600*10**3)                   # in MW
    return results

def CalCondenser(Qoutdot):
    # Part(f)
    # Given: 
    tcwin=15
    tcwout=35

    hcwout=tx2h(tcwout,0)   # From table A-2,hcwout= 146.68  kj/kg  
    hcwin= tx2h(tcwin,0)    # hcwin 62.99  
    mcwdot= (Qoutdot*10**3*3600)/(hcwout-hcwin)              
    return  mcwdot        
