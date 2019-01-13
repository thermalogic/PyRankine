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

import matplotlib.pyplot as plt
import numpy as np


def PlotTSDiagram(States):

    plt.figure(figsize=(10.0, 5.0))  # figsize :set figure size

    # saturated vapor and liquid entropy lines
    npt = np.linspace(10, 647.096-273.15, 200)  # range of temperatures
    # saturated vapor tx2s(t, 1),x=1
    svap = [s for s in [tx2s(t, 1) for t in npt]]
    # saturated liquid tx2s(t, 0),x=0
    sliq = [s for s in [tx2s(t, 0) for t in npt]]
    plt.plot(svap, npt, 'r-')
    plt.plot(sliq, npt, 'b-')

    t = [States[i]['t'] for i in range(4)]
    s = [States[i]['s'] for i in range(4)]
    
    # States[3]['t'] is slightly larger than States[2]['t'] , points States[2] and States[3] are almost overlap if drawing with real values
    # so,adjust the value of States[3]['t'] ,using the virtual values to eliminate drawing overlap
    t[3] = States[3]['t']+8

    t.append(px2t(States[0]['p'], 0))
    s.append(px2s(States[0]['p'], 0))

    t.append(States[0]['t'])
    s.append(States[0]['s'])

    plt.plot(s, t, 'go-')

    plt.annotate('1 ({:.2f},{:.2f})'.format(s[0], t[0]),
                 xy=(s[0], t[0]), xycoords='data',
                 xytext=(+2, +5), textcoords='offset points', fontsize=12)

    plt.annotate('2 ({:.2f},{:.2f})'.format(s[1], t[1]),
                 xy=(s[1], t[1]), xycoords='data',
                 xytext=(+2, +5), textcoords='offset points', fontsize=12)

    plt.annotate('3 ({:.2f},{:.2f})'.format(s[2], t[2]),
                 xy=(s[2], t[2]), xycoords='data',
                 xytext=(+10, +5), textcoords='offset points', fontsize=12)

    plt.annotate('4 ({:.2f},{:.2f})'.format(s[3], t[3]-8),
                 xy=(s[3], t[3]), xycoords='data',
                 xytext=(+10, +25), textcoords='offset points', fontsize=12)

    plt.annotate('5 ({:.2f},{:.2f})'.format(s[4], t[4]),
                 xy=(s[4], t[4]), xycoords='data',
                 xytext=(-60, +5), textcoords='offset points', fontsize=12)


    tist=[t[1],t[1]]
    sist=[s[1],px2s(States[1]['p'],1)]
    plt.plot(sist, tist, 'y-')
    
    plt.title('T-s: Ideal Rankine Cycle')
    plt.xlabel('Entropy(kJ/(kg.K)')
    plt.ylabel('Temperature(°C)')
    plt.grid()
    plt.show()
