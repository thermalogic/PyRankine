"""
  Step 3-csv ：Basic Object-Orientation Abstraction  and Data Representation of The Ideal Rankine Cycle
 
   class  Condenser 

                    ↓   inletNode exhausted steam
                ┌───┴───┐
                │       │ 
                │       │
                │       │
                └───┬───┘  
                    ↓ exitNode condensate water 



   Author:Cheng Maohua  Email: cmh@seu.edu.cn                   
"""

import node


class Condenser:
    """
    The condenser class
    """

    def __init__(self, name, inletNode, exitNode):
        """
        Initializes the condenser with nodes
        """
        self.inletNode = inletNode
        self.exitNode = exitNode
        self.name = name

    def state(self, nodes):
        pass

    def simulate(self, nodes):
        self.heatExtracted = nodes[self.inletNode].h - nodes[self.exitNode].h

    def mdotenergy(self, mdot):
        self.Qoutdot = mdot * self.heatExtracted / (3600 * 1000)

    def cw_nodes(self, inletNodeW, exitNodeW):
        self.inletNodeW = inletNodeW
        self.exitNodeW = exitNodeW

    def cw_simulate(self, nodew):
        """
        Simulates the Condenser 
        """
        self.mcwdot = (self.Qoutdot * 1000 * 3600) / \
            (nodew[self.exitNodeW].h - nodew[self.inletNodeW].h)
