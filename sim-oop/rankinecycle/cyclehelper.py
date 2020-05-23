"""
General Object-oriented Abstraction and JSON Textual Model of Rankine Cycle 

 - OutFiles(cycle, outfilename=None)

Author:Cheng Maohua  Email: cmh@seu.edu.cn

"""
import sys
from components.node import Node

def OutFiles(cycle, outfilename=None):
    savedStdout = sys.stdout
    # redirect to the outfilename
    if (outfilename != None):
        datafile = open(outfilename, 'w', encoding='utf-8')
        sys.stdout = datafile

    # 1 output cycle performance
    print(cycle)
   
    # 2 output nodes
    print(Node.title)
    for node in cycle.nodes:
        print(node)
    # 3 output devices
    for key in cycle.comps:
        print(cycle.comps[key])
    
    # return to sys.stdout
    if (outfilename != None):
        datafile.close()
        sys.stdout = savedStdout


