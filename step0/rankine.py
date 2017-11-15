"""
Step 0： Zero @  Data Structures,Program architecture, Algorithms(The Ideal Rankine Cycle)
                    
        simple data type and expression  only 

The ideal rankine cycle as 
   
    ┌─── State 1 ── Turbine ── State 2 ──┐
    │                                    │
  Boiler                            Condenser
    │                                    │
    └─── State 4 ──  Pump  ──  State 3───┘  

 Michael J . Mora. 
     Fundamentals of Engineering Thermodynamics(7th Edition). John Wiley & Sons, Inc. 2011
     Chapter 8 : Vapour Power Systems Example 8.1:Analyzing an Ideal Rankine Cycle  Page 438

License: this code is in the public domain

Author:Cheng Maohua
Email: cmh@seu.edu.cn

"""
from seuif97 import *

# Given:-
p1 = 8.0  # in MPa
p3 = 0.008             # pressure of saturated liquid exiting the condenser in MPa
Wcycledot = 100.00     # the net power output of the cycle in MW

# Analysis

# State  1
h1 = px2h(p1, 1)         
s1 = px2s(p1, 1)       

# State  2
s2 = s1
# quality at state 2
sf = px2s(p3, 0)        
sg = px2s(p3, 1)        
x2 = (s2 - sf) / (sg - sf)

hf = px2h(p3, 0)     
hg = px2h(p3, 1)
h2 = hf + x2 * (hg - hf) 

# State 3 is saturated liquid at 0.008 MPa, so
h3 = hf  # kj/kg
v3 = px2v(p3, 0)  # 1.0084e-3  m^3/kg

# State 4
p4 = p1
h4 = h3 + v3 * (p4 - p3) * 10**6 * 10**-3    # kj/kg

# Part(a)
# Mass and energy rate balances for control volumes
# around the turbine and pump give, respectively

# turbine
wtdot = h1 - h2
# pump
wpdot = h4 - h3

# The rate of heat transfer to the working fluid as it passes
# through the boiler is determined using mass and energy rate balances as
qindot = h1 - h4
# thermal efficiency
eta = (wtdot - wpdot) / qindot

# Part(b)
# back work ratio：bwr, defined as the ratio of the pump work input to the work
# developed by the turbine.
bwr = wpdot / wtdot                                    #

# Part(c)
# mass flow rate in kg/h
mdot = (Wcycledot * 1000 * 3600) / ((h1 - h2) -  (h4 - h3))      
# Part(d)
Qindot = mdot * qindot / (3600 * 1000)                     # in MW
# Part(e)
Qoutdot = mdot * (h2 - h3) / (3600 * 1000)                   # in MW
# Part(f)
# Given:
tcwin = 15
tcwout = 35

hcwout = tx2h(tcwout, 0)   # From table A-2,hcwout= 146.68  kj/kg

hcwin = tx2h(tcwin, 0)    # hcwin 62.99
mcwdot = (Qoutdot * 1000 * 3600) / (hcwout - hcwin)          # in kg/h

# Results
print("Indeal Rankine Cycle: Net Output Power ",Wcycledot,'MW')
print('\t(a) The thermal efficiency for the cycle is %.2f' %(eta*100), '%')
print('\t(b) The back work ratio is ', round(bwr, 3) * 100, '%')
print('\t(c) The mass flow rate of the steam is', round(mdot, 2), 'kg/h.')
print('\t(d) The rate of heat transfer,Qindot into the working fluid as it passes through the boiler is',
      round(Qindot, 2), 'MW.')
print('\t(e) The rate of heat transfer,Qoutdot from the condensing steam as it passes through the condenser is',
      round(Qoutdot, 2), 'MW.')
print('\t(f) The mass flow rate of the condenser cooling water is',
      round(mcwdot, 2), 'kg/h.')
