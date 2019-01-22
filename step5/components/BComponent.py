"""
 Step5: The General Simulator of Rankine Cycle with the  base class of components

 The  base class of components
 
 Author:Cheng Maohua  Email: cmh@seu.edu.cn

"""
from .node import Node


class BComponent():

    energy = None
    devTYPE = None

    def __init__(self, dictDev):
        """ Initializes the Component"""
        self.name = None
        self.nodes = []
        #self.__dict__.update(dictDev)
        
        self.fdotok = False

    def state(self, nodes):
        """  State """
        raise NotImplementedError

    # _fdotok_
    def _fdotok_(self, nodes):
        """ _fdotok_ """
        self.fdotok = nodes[self.nodes[0]].fdot != None
        for node in range(1, len(self.nodes)):
            self.fdotok = self.fdotok and (nodes[node].fdot != None)

    def fdot(self, nodes):
        """ mass and energy balance: innode->[]->outnode"""
        if (self.fdotok == False):
            try:
                if (nodes[self.inNode].fdot != None):
                    nodes[self.outNode].fdot = nodes[self.inNode].fdot
                elif (nodes[self.outNode].fdot != None):
                    nodes[self.inNode].fdot = nodes[self.outNode].fdot

                # modified self.fdotok
                self._fdotok_(nodes)
            except:
                self.fdotok == False

    def simulate(self, nodes):
        """  Simulates   """
        raise NotImplementedError

    def sm_energy(self, nodes):
        """  energy """
        raise NotImplementedError

    def export(self, nodes):
        """ export results: name,nodes """
        result = '\n' + self.name
        result += '\n' + Node.title
        for i in self.nodes:
           result +='\n' + nodes[i].__str__()
        return result
