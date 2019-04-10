from seuif97 import ps2h
from node import  *

class Turbine:

    """
    Turbine class

    Represents a turbine in the Rankine cycle

      inletNode inlet steam   
                 ┌────────┐
              ↓ ╱                │ 
 workExtracted ┤                  │
                ╲                 │
                 └────────┤
                                   ↓  exitNode exhausted steam   

    """
    energy = 'workExtracted'

    def __init__(self, inletNode, exitNode, eta=1.0):
        """
        Initializes the turbine with nodes
        """
        self.inletNode = inletNode
        self.exitNode = exitNode
        self.eta = eta

    def simulate(self, nodes):
        """
        Simulates the turbine 
        """
        nodes[self.exitNode].s = nodes[self.inletNode].s
        hout_s = ps2h(nodes[self.exitNode].p, nodes[self.exitNode].s)

        nodes[self.exitNode].h = nodes[self.inletNode].h - \
            self.eta*(nodes[self.inletNode].h-hout_s)
        nodes[self.exitNode].ph()

        self.workExtracted = nodes[self.inletNode].h - nodes[self.exitNode].h
