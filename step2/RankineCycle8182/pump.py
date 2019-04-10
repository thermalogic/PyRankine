"""
step 2 : Object-Orientation Abstraction and CSV Textual Representation The Rankine Cycle(Example 8.1,8.2)

License: this code is in the public domain
Cheng Maohua(cmh@seu.edu.cn)

"""

from seuif97 import ps2h
from node import  *

class Pump:
    """
    Pump class

    Represents a pump in the Rankine cycle

                ┌───────┐
                │       │
     exitNode ← ┼───────┼← inletNode
                │       │
                └───────┘  

    """
    energy = "workRequired"

    def __init__(self, inletNode, exitNode, eta=1.0):
        """
        Initializes the pump with nodes
        """
        self.inletNode = inletNode
        self.exitNode = exitNode
        self.eta = eta

    def simulate(self, nodes):
        """
        Simulates the pump 
        """

        sout_s = nodes[self.inletNode].s
        hout_s = ps2h(nodes[self.exitNode].p, sout_s)
        nodes[self.exitNode].h = nodes[self.inletNode].h + \
            (hout_s - nodes[self.inletNode].h)/self.eta
        nodes[self.exitNode].ph()

        self.workRequired = nodes[self.exitNode].h - nodes[self.inletNode].h
