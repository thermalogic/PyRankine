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

    def __combined_node_value(self, node, port):
        """ 
           the node is the connector of two ports ,so the node may get values from all of two ports
            the values is the union set of the not-none values within two ports 
        """
        for key,portvalue in port[0].__dict__.items():
            nodevalue = node[0].__dict__[key]
            if  portvalue is not None and nodevalue is None:
                node[0].__dict__[key] = portvalue
  
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
        # 3 merge port1 info into  nodes[self.id]
        self.__combined_node_value(self.nodes[self.id], comp_port1)
        # 4 ser port1 to the aliad of nodes[self.id]
        comp_port1[0] = self.nodes[self.id][0]

        self.id += 1
