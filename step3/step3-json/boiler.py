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


class Boiler:
    """
    The boiler class
    """

    def __init__(self, name, inletNode, exitNode):
        """
        Initializes the boiler 
        """
        self.inletNode = inletNode
        self.exitNode = exitNode
        self.name = name

    def state(self, nodes):
        pass

    def simulate(self, nodes):
        self.heatAdded = nodes[self.exitNode].h - nodes[self.inletNode].h

    def mdotenergy(self, mdot):
        self.Qindot = mdot * self.heatAdded / (3600 * 1000)
