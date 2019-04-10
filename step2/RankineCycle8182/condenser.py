from node import  *

class Condenser:
    """
    The Condenser class
                        ↓   inletNode exhausted steam
                ┌───┴───┐
                │              │ 
   exitNodeW  ←┼───────┼← inletNodeW  
                │              │
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
