"""
The PyRankine: the  hybrid steady-state simulator of Rankine Cycle

class Connector

Author:Cheng Maohua  Email: cmh@seu.edu.cn 

"""

from .port import *


class Connector:

    def __init__(self):
        self.nodes = []
        self.id = 0

    def combined_node_value(self, node, port):
        """ 
           the node is the connector of two ports ,so the node may get values from all of two ports
            the values is the union set of the not-none values within two ports 
        """
        for key in node[0].__dict__.keys():
            nodevalue = getattr(node[0], key)
            portvalue = getattr(port[0], key)
        if nodevalue is None and portvalue is not None:
            setattr(node[0], key, portvalue)

    def add_node(self, tupConnector, comps):
        comp0, port0 = tupConnector[0]
        comp1, port1 = tupConnector[1]

        comp_port0 = comps[comp0].portdict[port0]
        comp_port1 = comps[comp1].portdict[port1]
        # 1 get the index of port in nodes
        comp_port0[0].id = self.id
        comp_port0[0].desc = comp0 + \
            "."+port0 + " = " + comp1+"."+port1
        # 2 add port0 into nodes
        self.nodes.append(comp_port0)
        # 3 join port1 info into  nodes[self.id]
        self.combined_node_value(self.nodes[self.id], comp_port1)
        # 4 send back nodes[self.id] to port1
        comp_port1[0] = self.nodes[self.id][0]

        self.id += 1
