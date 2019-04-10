"""
Step 1 : Abstraction and Textual Representation of The Rankine Cycle(Example 8.1,8.2)

nodes Module

License: this code is in the public domain

Cheng Maohua(cmh@seu.edu.cn)

"""

import csv
from seuif97 import *

def read_nodesfile(filename):
    """ nodes in the  csv file"""
    
    # readlines() to the end of file
    countNodes = len(open(filename, 'r').readlines()) - 1
    nodes = [{'NAME':None,'p':None,'t':None,'h':None,'s':None,'x':None,'fdot':None} for i in range(countNodes)]

    #  re-open the file to its head 
    csvfile = open(filename, 'r')
    reader = csv.DictReader(csvfile)
    for line in reader:
        i = int(line['NID'])
        nodes[i]['NAME'] = line['NAME']
        try:
            nodes[i]['p'] = float(line['p'])
        except:
            nodes[i]['p'] = None
        try:
            nodes[i]['t'] = float(line['t'])
        except:
            pass
        try:
            nodes[i]['x'] = float(line['x'])
        except:
            pass
        try:
            nodes[i]['fdot'] = float(line['fdot'])
        except:
            pass    
        
        if line['p'] != '' and line['t'] != '':
            nodes[i]['h'] = pt2h(nodes[i]['p'], nodes[i]['t'])
            nodes[i]['s'] = pt2s(nodes[i]['p'], nodes[i]['t'])
        elif line['p'] != '' and line['x'] != '':
            nodes[i]['t'] = px2t(nodes[i]['p'], nodes[i]['x'])
            nodes[i]['h'] = px2h(nodes[i]['p'], nodes[i]['x'])
            nodes[i]['s'] = px2s(nodes[i]['p'], nodes[i]['x'])
        elif line['t'] != '' and line['x'] != '':
            nodes[i]['p'] = tx2p(nodes[i]['t'], nodes[i]['x'])
            nodes[i]['h'] = tx2h(nodes[i]['t'], nodes[i]['x'])
            nodes[i]['s'] = tx2s(nodes[i]['t'], nodes[i]['x'])
    
    csvfile.close()
    return nodes