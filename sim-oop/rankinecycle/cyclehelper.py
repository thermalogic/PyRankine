"""
General Object-oriented Abstraction of Rankine Cycle 

 - OutFiles(cycle, outfilename=None)

Author:Cheng Maohua  Email: cmh@seu.edu.cn

"""
import sys
from components.node import Node

def OutFiles(cycle, outfilename=None):
    savedStdout = sys.stdout
    # redirect to the outfilename
    if outfilename is not None:
        datafile = open(outfilename, 'w', encoding='utf-8')
        sys.stdout = datafile

    # 1 output cycle performance
    print(cycle)
   
    # 2 output nodes
    print(Node.title)
    for key in cycle.nodes:
        print(cycle.nodes[key])
    # 3 output devices
    for key in cycle.comps:
        print(cycle.comps[key])
    
    # return to sys.stdout
    if (outfilename != None):
        datafile.close()
        sys.stdout = savedStdout


def SpecifiedSimulator(cycle, prefixResultFileName, SetPower=None, SetMass=None):
    # Specified Simulating： Power or Mass Flow
    cycle.SpecifiedSimulator(SetPower, SetMass)

    # output to files
    if SetPower != None:
        outprefix = prefixResultFileName + '-sp'
    else:
        outprefix = prefixResultFileName + '-sm'
    # output to text
    OutFiles(cycle)
    OutFiles(cycle, outprefix + '.txt')