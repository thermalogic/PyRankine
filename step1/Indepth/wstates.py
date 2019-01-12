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

from seuif97 import *


def FixeStates(States):

    # State  1, Node 0
    States[0]['p'] = 8.0
    p = States[0]['p']
    States[0]['t'] = px2t(p, 1)
    States[0]['h'] = px2h(p, 1)
    States[0]['s'] = px2s(p, 1)

    # State  2, Node 1
    States[1]['p'] = 0.008
    States[1]['s'] = States[0]['s']
    p = States[1]['p']
    s = States[1]['s']
    States[1]['t'] = ps2t(p, s)
    States[1]['h'] = ps2h(p, s)

    # State 3 , Node 2 saturated liquid at 0.008 MPa
    States[2]['p'] = 0.008
    p = States[2]['p']
    States[2]['t'] = px2t(p, 0)
    States[2]['h'] = px2h(p, 0)  # kj/kg
    States[2]['s'] = px2s(p, 0)

    # State 4 , Node 3
    States[3]['p'] = States[0]['p']
    States[3]['s'] = States[2]['s']
    p = States[3]['p']
    s = States[3]['s']
    States[3]['h'] = ps2h(p, s)
    States[3]['t'] = ps2t(p, s)

    return States
