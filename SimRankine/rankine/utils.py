"""
The PyRankine: the  hybrid steady-state simulator of Rankine Cycle

 - create_dictcycle_from_jsonfile(filename):
 - OutFiles(cycle, outfilename=None)
 - OutDevsFiles(cycle, outfilename=None)

Author: Cheng Maohua, Email:cmh@seu.edu.cn

"""
import sys
import json
from components.port import Port

def create_dictcycle_from_jsonfile(filename):
    """ create dict cycle from json file"""
    with open(filename, 'r') as f:
        dictcycle = json.loads(f.read())
    
    # convection dict of conn pair  to the tuple in python
    for i in range(len(dictcycle["connectors"])):
        curconnpairdict = dictcycle["connectors"][i]
        keys=list(curconnpairdict.keys())
        values = list(curconnpairdict.values())
        dictcycle["connectors"][i] = ((keys[0], values[0]), (keys[1], values[1]))
    return dictcycle

def OutFiles(cycle, outfilename=None):
    savedStdout = sys.stdout
    # redirect to the outfilename
    if outfilename is not None:
        datafile = open(outfilename, 'w', encoding='utf-8')
        sys.stdout = datafile

    # 1 output cycle performance
    print(cycle)
   
    # 2 output devices
    print("\n--- DEVICES ---")
    for key in cycle.comps:
        print(cycle.comps[key])

    # 3 output connectors
    print("\n--- CONNECTORS ---\n")
    print(Port.title)
    for item in cycle.nodes:
        print(item)

    # return to sys.stdout
    if (outfilename != None):
        datafile.close()
        sys.stdout = savedStdout

def OutDevsFiles(cycle, outfilename=None):
    """ devices only"""
    savedStdout = sys.stdout
    # redirect to the outfilename
    if outfilename is not None:
        datafile = open(outfilename, 'w', encoding='utf-8')
        sys.stdout = datafile

    # 1 output connectors
    print("\n--- CONNTERORS ---")
    print(Port.title)
    for item in cycle.curcon.nodes:
        print(item[0])
    # 2 output devices
    print("\n--- DEVICES ---")
    for key in cycle.comps:
        print(cycle.comps[key])
    
    # return to sys.stdout
    if (outfilename != None):
        datafile.close()
        sys.stdout = savedStdout
