"""
Step 0：Zero Abstraction of The Rankine Cycle with Irreversibilitiesas
                    
        simple data type and expression  only 

The Rankine Cycle with Irreversibilitiesas 
   
    ┌─── State 1 ── Turbine ── State 2 ──┐
    │                                    │
  Boiler                            Condenser
    │                                    │
    └─── State 4 ──  Pump  ──  State 3───┘  

 Michael J . Moran. Fundamentals of Engineering Thermodynamics(7th Edition). John Wiley & Sons, Inc. 2011
    Chapter 8 : Vapour Power Systems 
       Example 8.2: Analyzing a Rankine Cycle with Irreversibilities Page 444
       
Running:

>python rankine82.py

License: this code is in the public domain

Author:Cheng Maohua
Email: cmh@seu.edu.cn

"""
from seuif97 import *

# State  1
p1 = 8.0  # in MPa
t1 = px2t(p1, 1)
h1 = px2h(p1, 1)          # h1 = 2758.0    From table A-3  kj/kg
s1 = px2s(p1, 1)          # s1 = 5.7432    From table A-3  kj/kg.k

# State  2 ,p2=0.008
p2 = 0.008
s2s = s1
h2s = ps2h(p2, s2s)
t2s = ps2t(p2, s2s)
etat_t = 0.85
h2 = h1-etat_t*(h1-h2s)
t2 = ph2t(p2, h2)
s2 = ph2s(p2, h2)

# State 3 is saturated liquid at 0.008 MPa
p3 = 0.008
t3 = px2t(p3, 0)
h3 = px2h(p3, 0)  # kj/kg
s3 = px2s(p3, 0)

# State 4
p4 = p1
s4s = s3
h4s = ps2h(p4, s4s)
t4s = ps2t(p4, s4s)
etat_p = 0.85
h4 = h3+(h4s-h3)/etat_p
t4 = ph2t(p4, h4)
s4 = ph2s(p4, h4)

# Part(a)
eta = ((h1-h2)-(h4-h3))/(h1-h4)             # thermal efficiency

# Result for part (a)
print('Thermal efficiency is: %.3f' % (100*eta), '%')

# Part(b)
Wcycledot = 100                             # given,a net power output of 100 MW
# Calculations
mdot = (Wcycledot*(10**3)*3600)/((h1-h2)-(h4-h3))
# Result for part (b)
print('The mass flow rate of steam, in kg/h, for a net power output of 100 MW is %.3f' % mdot, 'kg/h.')

# Part(c)
Qindot = mdot*(h1-h4)/(3600 * 10**3)
# Result
print('The rate of heat transfer Qindot into the working fluid as it passes through the boiler, is %.3f' % Qindot, 'MW.')

# Part(d)
Qoutdot = mdot*(h2-h3)/(3600*10**3)
# Result
print('The rate of heat transfer  Qoutdotfrom the condensing steam as it passes through the condenser, is %.3f' % Qoutdot, 'MW.')

# Part(e)
tcwin = 15
tcwout = 35
hcwout = tx2h(tcwout, 0)   # From table A-2,hcwout= 146.68  kj/kg
hcwin = tx2h(tcwin, 0)    # hcwin 62.99
mcwdot = (Qoutdot*10**3*3600)/(hcwout-hcwin)
# Result
print('The mass flow rate of the condenser cooling water, is: %.3f' %
      mcwdot, 'kg/h.')
