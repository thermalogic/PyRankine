"""

Nodes Module

Step 1 :The Simple Abstraction of The Rankine Cycle 8.1,8.2  with list,dict,function

License: this code is in the public domain

Cheng Maohua(cmh@seu.edu.cn)

"""


from seuif97 import *

def FixeNodesState(Nodes):
    for node in Nodes:     
        if node['p'] != None and node['t'] != None:
            node['h'] = pt2h(node['p'], node['t'])
            node['s'] = pt2s(node['p'], node['t'])
            node['x'] = pt2x(node['p'], node['t'])
        elif node['p'] != None and node['x'] != None:
            node['t'] = px2t(node['p'], node['x'])
            node['h'] = px2h(node['p'], node['x'])
            node['s'] = px2s(node['p'], node['x'])
        elif node['t'] != None and  node['x'] != None:
            node['p'] = tx2p(node['t'], node['x'])
            node['h'] = tx2h(node['t'], node['x'])
            node['s'] = tx2s(node['t'], node['x'])
    
    return Nodes