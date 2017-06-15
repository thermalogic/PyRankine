
"""
Step 1  

Step by step codes of the ideal rankine cycle simulator to demonstrate: 

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

# Analysis: fix each of 
#     the principal states   （1,2,3,4) 
#               ->   Nodes    (0,1,2,3)

def CalState():
    p=[]
    t=[]
    h=[]
    s=[]
    v=[]
    x=[]

    numNodes=4

    for node in range(numNodes):
        p.append(None)
        t.append(None)
        h.append(None)
        s.append(None)
        v.append(None)
        x.append(None)
   

    # Given:-
    p[0] = 8.0               #  in MPa
    p[2] = 0.008             # pressure of saturated liquid exiting the condenser in MPa

    # State  1, Node 0
    t[0]=px2t(p[0],1)
    h[0]=px2h(p[0],1)        
    s[0]=px2s(p[0],1)         

    # State  2, Node 1
    t[1]=px2t(p[2],0)
    s[1] = s[0]

    # quality at state 2
    sf=px2s(p[2],0)         # sf = 0.5926   kj/kg.k
    sg=px2s(p[2],1)         # sg = 8.2287   kj/kg.k
    x[1]=(s[1]-sf)/(sg-sf)

    hf=px2h(p[2],0)        
    hg=px2h(p[2],1)         
    h[1] = hf + x[1]*(hg-hf)     

    # State 3 , Node 2
    #   saturated liquid at 0.008 MPa
    t[2]=t[1]
    s[2]=tx2s(t[2],0)
    h[2] = hf                                         #  kj/kg
    v[2] =px2v(p[2],0)                # m^3/kg

    #State 4 , Node 3
    p[3] = p[0]
    s[3]=s[2]
    t[3]=ps2t(p[3],s[3]) 
    h[3] = h[2] + v[2]*(p[3]-p[2])*10**6*10**-3    # kj/kg
    
    return (p,t,h,s,v,x)
