"""
Step 1 : Abstraction and Textual Representation of The Rankine Cycle(Example 8.1,8.2)

The rankine cycle as 
   
    ┌─── Node 0 ── Turbine ── Node 1   ──┐
    │                                    │
  Boiler                            Condenser
    │                                    │
    └─── Node 3  ──  Pump  ──  Node 2 ───┘  

 Michael J . Moran.  Fundamentals of Engineering Thermodynamics(7th Edition). John Wiley & Sons, Inc. 2011
    
    Chapter 8 : Vapour Power Systems 
    
        Example 8.1: Analyzing an Ideal Rankine Cycle  Page 438
        Example 8.2: Analyzing a Rankine Cycle with Irreversibilities Page 444

Run:

>python rankine.py

License: this code is in the public domain

Cheng Maohua(cmh@seu.edu.cn)

"""

from nodes import *
from devices import *
from cycle import *
from plotTS import *


def OutFiles(Nodes, Cycle, outfilename=None):
    savedStdout = sys.stdout
    if (outfilename != None):
        datafile = open(outfilename, 'w', encoding='utf-8')
        sys.stdout = datafile

    # output the Cycle Performance
    print('\n-------------------------')
    print('Net Power is %.3f' % Cycle['Wdot'], 'MW.')
    print('Mass flow rate is %.3f' % Cycle['mdot'], 'kg/h.')
    print('The thermal efficiency is %.3f' % (Cycle['eta']*100), '%')
    print('Heat Rate is %.3f' % Cycle['HeatRate'], 'kJ/kWh.')
    print('Steam Rate is %.3f' % Cycle['SteamRate'], 'kg/kWh')
    print('totalWExtracted is  %.3f' % Cycle['Wout'], 'MW.')
    print('totalWRequired is  %.3f' % Cycle['Win'], 'MW.')
    print('totalQadded is  %.3f' % Cycle['Qin'], 'MW.')

    # output nodes
    print('\n{:10}\t {:^6}\t {:^7}  {:^7}  {:^7}  {:^7} {:^7} {:^7}'.format(
        "NAME", "Node", "P(MPa)", "T(°C)", "H(kJ/kg)", "S(kJ/kg.K)", "X", "FDOT"))
    i = 0
    for node in Nodes:
        print('{:10}\t {:^6d}\t {:>5.3f} {:>9.2f} {:>10.2f} {:>9.3f} {:>9.3f}  {:>9.3f}'.format(
            node['NAME'], i, node['p'],  node['t'],  node['h'],  node['s'],  node['x'], node['fdot']))
        i += 1
    
    if (outfilename != None):
        datafile.close()
        sys.stdout = savedStdout


def RankineCycle(nds_filenames,des_filenames):
    # 1 nodes
    for i in range(len(nds_filenames)):
        CurNodes=[]
        CurNodes=read_nodesfile(nds_filenames[i])
        Nodes.append(CurNodes)

    # 2 devices
    for i in range(len(des_filenames)):
        CurDevices={}
        CurDevices=read_DevicesFile(des_filenames[i])
        CalDevices(CurDevices,Nodes[i])
        Devices.append(CurDevices)

    # 3 cycle
    for i in range(len(des_filenames)):    
        CurCycle = {'Wdot': 100.0}
        CalCycle(Devices[i],   CurCycle)
        Cycle.append(CurCycle)

    # 4 output
    for i in range(len(des_filenames)):    
        cyclename = nds_filenames[i][0:nds_filenames[i].find('-')]
        OutFiles(Nodes[i],Cycle[i])
        OutFiles(Nodes[i], Cycle[i],cyclename +'-sp.txt')


nds_filenames = ['./data/rankine81-nds.csv', './data/rankine82-nds.csv']
des_filenames = ['./data/rankine81-des.csv', './data/rankine82-des.csv']

Nodes = []
Devices = []
Cycle = []
RankineCycle(nds_filenames,des_filenames )
for node in Nodes:
    PlotTSDiagram(node)

