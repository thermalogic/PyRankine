"""
 Step5: The General Simulator of Rankine Cycle with the  base class of components

 The  base class of components
 
 Author:Cheng Maohua  Email: cmh@seu.edu.cn

"""
from .node import *


class BComponent():

    energy = None
    devTYPE = None

    def __init__(self, dictDev):
        """ Initializes the Component"""
        self.nodes = []
        raise NotImplementedError

    def state(self, Nodes):
        """  State """
        raise NotImplementedError

    # _fdotok_
    def _fdotok_(self, nodes):
        """ _fdotok_ """
        self.fdotok = nodes[self.nodes[0]].fdot != None
        for node in range(1, len(self.nodes)):
            self.fdotok = self.fdotok and (nodes[node].fdot != None)

    def fdot(self, nodes):
        """ mass and energy balance"""
        raise NotImplementedError

    def simulate(self, nodes):
        """  Simulates   """
        raise NotImplementedError

    def sm_energy(self, nodes):
        """  energy """
        raise NotImplementedError

    def export(self, nodes):
        """ export results """
        raise NotImplementedError
