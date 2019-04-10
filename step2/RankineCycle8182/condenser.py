"""
step 2 : Object-Orientation Abstraction and CSV Textual Representation The Rankine Cycle(Example 8.1,8.2)

License: this code is in the public domain
Cheng Maohua(cmh@seu.edu.cn)

"""

from node import  *

class Condenser:
    """
    The Condenser class
                    ↓   inletNode exhausted steam
                ┌───┴───┐
                │       │ 
    exitNodeW  ←┼───────┼← inletNodeW  
                │       │
                └───┬───┘  
                    ↓    exitNode condensate water 

    """
    energy = "heatOuted"

    def __init__(self, inletNode, exitNode):
        """
        Initializes the condenser with nodes
        """
        self.inletNode = inletNode
        self.exitNode = exitNode

    def simulate(self, nodes):
        """
        Simulates the Condenser 
        """
        self.heatExtracted = nodes[self.inletNode].h - nodes[self.exitNode].h
