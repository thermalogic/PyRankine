"""
Step 3-json ：Basic Object-Orientation Abstraction  and Data Representation of The Ideal Rankine Cycle

class Boiler

                    ↑    exitNode main steam
                ┌───┼───┐
                │   │   │
                │   │   │
                │   │   │
                └───┼───┘  
                    ↑    inletNode main feedwater   

 Author:Cheng Maohua  Email: cmh@seu.edu.cn    

"""

import node


class Boiler(object):
    """
    The boiler class
    """

    def __init__(self,dictDev):
        """
        Initializes the boiler 
        """
        self.name = dictDev['name']
        self.inletNode = dictDev['inNode']
        self.exitNode = dictDev['exNode']

    def state(self, nodes):
        pass

    def simulate(self, nodes):
        self.heatAdded = nodes[self.exitNode].h - nodes[self.inletNode].h

    def mdotenergy(self, mdot):
        self.Qindot = mdot * self.heatAdded / (3600 * 1000)
