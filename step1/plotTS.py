"""

Step 1 : Abstraction and Textual Representation of The Rankine Cycle(Example 8.1,8.2)

T-S Diagram of the Rankine Cycle 

The rankine cycle as 
   
    ┌─── Node 0 ── Turbine ── Node 1   ──┐
    │                                    │
  Boiler                            Condenser
    │                                    │
    └─── Node 3  ──  Pump  ──  Node 2 ───┘  


License: this code is in the public domain

Cheng Maohua(Email: cmh@seu.edu.cn)

"""
import matplotlib.pyplot as plt
import numpy as np

from seuif97 import *

def PlotTSDiagram(Nodes):

    plt.figure(figsize=(10.0, 5.0))  # figsize :set figure size

    # saturated vapor and liquid entropy lines
    npt = np.linspace(10, 647.096-273.15, 200)  # range of temperatures
    # saturated vapor tx2s(t, 1),x=1
    svap = [s for s in [tx2s(t, 1) for t in npt]]
    # saturated liquid tx2s(t, 0),x=0
    sliq = [s for s in [tx2s(t, 0) for t in npt]]
    plt.plot(svap, npt, 'r-')
    plt.plot(sliq, npt, 'b-')

    t = [Nodes[i]['t'] for i in range(4)]
    s = [Nodes[i]['s'] for i in range(4)]

    # Nodes[3]['t'] is slightly larger than Nodes[2]['t'] , points Nodes[2] and Nodes[3] are almost overlap if drawing with real values
    # so,adjust the value of Nodes[3]['t'] ,using the virtual values to eliminate drawing overlap
    t[3] = Nodes[3]['t']+8

    t.append(px2t(Nodes[0]['p'], 0))
    s.append(px2s(Nodes[0]['p'], 0))

    t.append(Nodes[0]['t'])
    s.append(Nodes[0]['s'])

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

    tist = [t[1], t[1]]
    sist = [s[1], px2s(Nodes[1]['p'], 1)]
    plt.plot(sist, tist, 'y-')

    plt.title('T-s: The Rankine Cycle')
    plt.xlabel('Entropy(kJ/(kg.K)')
    plt.ylabel('Temperature(°C)')
    plt.grid()
    plt.show()
