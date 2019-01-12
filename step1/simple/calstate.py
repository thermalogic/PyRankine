
"""
Step 1  Simple Abstraction of The Ideal Rankine Cycle

    list, dict,function

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


def CalState():
    numNodes = 4

    p = [None for node in range(numNodes)]
    t = [None for node in range(numNodes)]
    h = [None for node in range(numNodes)]
    s = [None for node in range(numNodes)]

    # State  1, Node 0
    p[0] = 8.0  # in MPa
    t[0] = px2t(p[0], 1)
    h[0] = px2h(p[0], 1)
    s[0] = px2s(p[0], 1)

    # State  2, Node 1
    p[1] = 0.008
    s[1] = s[0]
    t[1] = ps2t(p[1], s[1])
    h[1] = ps2h(p[1], s[1])

    # State 3 , Node 2 saturated liquid at 0.008 MPa
    p[2] = 0.008
    t[2] = px2t(p[2], 0)
    h[2] = px2h(p[2], 0)
    s[2] = px2s(p[2], 0)

    # State 4 , Node 3
    p[3] = p[0]
    s[3] = s[2]
    h[3] = ps2h(p[3], s[3])
    t[3] = ps2t(p[3], s[3])

    return (p, t, h, s)
