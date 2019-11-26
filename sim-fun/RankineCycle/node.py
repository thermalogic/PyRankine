

"""
 The Simulator 1: General Abstraction and CSV Textual Model of Rankine Cycle 

 Author:Cheng Maohua  Email: cmh@seu.edu.cn

"""
from seuif97 import pt2h, pt2s, pt2x, px2t, px2h, px2s, tx2p, tx2h, tx2s


def CalNodeProperties(nodes):
    """ get node properties using seuif97 """
    for node in nodes:
        if node['p'] != None and node['t'] != None:
            node['h'] = pt2h(node['p'], node['t'])
            node['s'] = pt2s(node['p'], node['t'])
            node['x'] = pt2x(node['p'], node['t'])
        elif node['p'] != None and node['x'] != None:
            node['t'] = px2t(node['p'], node['x'])
            node['h'] = px2h(node['p'], node['x'])
            node['s'] = px2s(node['p'], node['x'])
        elif node['t'] != None and node['x'] != None:
            node['p'] = tx2p(node['t'], node['x'])
            node['h'] = tx2h(node['t'], node['x'])
            node['s'] = tx2s(node['t'], node['x'])