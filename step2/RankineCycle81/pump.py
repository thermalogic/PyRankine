
"""
Step 2：Basic Object-Orientation Abstraction of The Ideal Rankine Cycle

Pump

                ┌───────┐
                │       │
    exitNode  ← ┼───────┼← inletNode
                │       │
                └───────┘  
  
License: this code is in the public domain

Author:Cheng Maohua
Email: cmh@seu.edu.cn

"""
import node


class Pump():

    """
    Pump class

    Represents a pump in the Rankine cycle
    """

    def __init__(self, inletNode, exitNode):
        """
        Initializes the pump with nodes
        """
        self.inletNode = inletNode
        self.exitNode = exitNode

    def simulate(self, nodes):
        """
        Simulates the pump 
        """
        nodes[self.exitNode].s = nodes[self.inletNode].s
        nodes[self.exitNode].h = nodes[self.inletNode].h+nodes[self.inletNode].v * \
            (nodes[self.exitNode].p-nodes[self.inletNode].p)*1000
        nodes[self.exitNode].hs()

        self.workRequired = nodes[self.exitNode].h - nodes[self.inletNode].h
