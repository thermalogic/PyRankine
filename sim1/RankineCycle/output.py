
"""
 The Simulator 1: General Abstraction and CSV Textual Model of Rankine Cycle 

 Author:Cheng Maohua  Email: cmh@seu.edu.cn

"""
import sys
import time

def OutFiles(Nodes, Cycle, outfilename=None):
    savedStdout = sys.stdout
    if (outfilename != None):
        datafile = open(outfilename, 'w', encoding='utf-8')
        sys.stdout = datafile

    # output the Cycle Performance
    str_curtime=time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(time.time()))
    print("\n ----- Rankine Cycle at Time: {} ----- ".format(str_curtime))
    print('\tNet Power: {:>.2f}MW.'.format(Cycle['Wdot']))
    print('\tMass flow rate: {:>.2f}kg/h'.format(Cycle['mdot']))
    print('\tThe thermal efficiency: {:>.2f}%'.format(Cycle['eta']*100))
    print('\tHeat Rate: {:>.2f}kg/kWh'.format(Cycle['HeatRate']))
    print('\tSteam Rate: {:>.2f}kg/kWh'.format(Cycle['SteamRate']))
    print('\ttotalWExtracted: {:>.2f}MW.'.format(Cycle['Wout']))
    print('\ttotalWRequired: {:>.2f}MW.'.format(Cycle['Win']))
    print('\ttotalQadded: {:>.2f}MW.'.format(Cycle['Qin']))

    # output nodes
    print('\n{:28}\t {:^6}\t {:^7}  {:^7}  {:^7}  {:^7} {:^7} {:^10}'.format(
        "NAME", "Node", "P(MPa)", "T(°C)", "H(kJ/kg)", "S(kJ/kg.K)", "X", "FDOT"))
    i = 0
    for node in Nodes:
        try:
            print('{:28}\t {:^6d}\t {:>5.3f} {:>9.2f} {:>10.2f} {:>9.3f} {:>9.3f} {:>9.3f}'.format(
            node['NAME'], i, node['p'],  node['t'],  node['h'],  node['s'], node['x'], node['fdot']))
        except:
            print(node['NAME'], i, node['p'],  node['t'],  node['h'],  node['s'], node['x'], node['fdot'])
        i += 1

    if (outfilename != None):
        datafile.close()
        sys.stdout = savedStdout