"""
The PyRankine: the  hybrid steady-state simulator of Rankine Cycle

class Connector

Author:Cheng Maohua  Email: cmh@seu.edu.cn 

"""

from components.port import Port


class Connector:

    def __init__(self, connectors, comps):
        self.nodes = []
        for i, tupconnector in enumerate(connectors):
            self.__add_node(i, tupconnector, comps)

    def __combined_node_value(self, node, port):
        """ 
           the node is the connector of two ports ,so the node may get values from all of two ports
            the values is the union set of the not-none values within two ports 
        """
        for key, portvalue in port.__dict__.items():
            nodevalue = node.__dict__[key]
            if portvalue is not None and nodevalue is None:
                node.__dict__[key] = portvalue

    def __add_node(self, i, tupConnector, comps):
        comp0, port0 = tupConnector[0]
        comp1, port1 = tupConnector[1]

        # 1 get the index of port in nodes
        comps[comp0].__dict__[port0].id = i
        comps[comp0].__dict__[
            port0].desc = "("+comp0 + "."+port0 + "," + comp1+"."+port1+")"
        # 2 add port0 into nodes
        self.nodes.append(comps[comp0].__dict__[port0])
        # 3 merge port1 info into  nodes[i]
        self.__combined_node_value(self.nodes[i], comps[comp1].__dict__[port1])
        # 4 ser port1 to the aliad of nodes[i]
        comps[comp0].__dict__[port0] = self.nodes[i]
        comps[comp1].__dict__[port1] = self.nodes[i]
