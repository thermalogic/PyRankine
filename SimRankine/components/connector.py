"""

class Connector

"""

from .port import *

class Connector:

    def __init__(self):
        self.nodes=[]
        self.id=0
       
    def getnodevalue(self, node,port):
        """ 
           the node is the connector of two ports ,so the node may get values from all of two ports
            the values is the union set of the not-none values within two ports 
        """
        if node[0].id is None and port.id is not None:
            node[0].id = port.id
        if node[0].p is None and port.p is not None:
            node[0].p = port.p
        if node[0].t is None and port.t is not None:
            node[0].t = port.t
        if node[0].h is None and port.h is not None:
            node[0].h = port.h
        if node[0].s is None and port.s is not None:
            node[0].s = port.s
        if node[0].x is None and port.x is not None:
            node[0].x = port.x
        if node[0].mdot is None and port.mdot is not None:
            node[0].mdot = port.mdot
        if node[0].fdot is None and port.fdot is not None:
            node[0].fdot = port.fdot


    def AddConnector(self, tupConnector,comps):
        comp0, port0 =tupConnector[0] 
        comp1, port1 =tupConnector[1]
        # 1 get the index of port in nodes
        comps[comp0].portdict[port0][0].id = self.id
        comps[comp0].portdict[port0][0].desc = comp0+"."+port0 +" & " + comp1+"."+port1 
        # 2 add port0 into nodes
        self.nodes.append(comps[comp0].portdict[port0])
        # 3 join port1 info into  nodes[self.id]
        self.getnodevalue(self.nodes[self.id],comps[comp1].portdict[port1][0])
        # 4 send back nodes[self.id] to port1
        comps[comp1].portdict[port1][0] =self.nodes[self.id][0]

        self.id += 1
