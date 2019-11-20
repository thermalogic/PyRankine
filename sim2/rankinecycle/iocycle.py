"""
General Object-oriented Abstraction and JSON Textual Model of Rankine Cycle 

Input datefile to the objects

output  objects to data file
  
Last updated: 2018.05.10

Author:Cheng Maohua  Email: cmh@seu.edu.cn

"""
import json
import sys


from components.node import Node

from components.boiler import Boiler
from components.condenser import Condenser
from components.openedheaterdw0 import OpenedheaterDw0
from components.pump import Pump
from components.turbineex0 import TurbineEx0
from components.turbineex1 import TurbineEx1
from components import compdict

def create_dictcycle_from_jsonfile(filename):
    """ create dict cycle from json file"""
    with open(filename, 'r') as f:
        dictcycle = json.loads(f.read())
    return dictcycle

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


def OutToJSONFiles(dictcycle, filename):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(dictcycle, json_file)
