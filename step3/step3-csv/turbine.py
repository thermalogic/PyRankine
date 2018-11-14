"""
Step 3-csv ：Basic Object-Orientation Abstraction  and Data Representation of The Ideal Rankine Cycle

 
        inletNode inlet steam   
                 ┌────────┐
              ↓ ╱         │ 
               ┤          │
                ╲         │
                 └────────┤
                          ↓  exitNode exhausted steam   
    

 Author:Cheng Maohua  Email: cmh@seu.edu.cn    

"""

import node

class Turbine():

    """
    Turbine class:   Represents a turbine in the Rankine cycle
    """

    def __init__(self, name,inletNode,exitNode):
        """
        Initializes the turbine with nodes
        """
        self.inletNode = inletNode
        self.exitNode=exitNode
        self.name=name
    
    def state(self,nodes):
        nodes[self.exitNode].s=nodes[self.inletNode].s
        nodes[self.exitNode].ps()
 
    def simulate(self,nodes):
        """
        Simulates the turbine 
        """
        self.workExtracted = nodes[self.inletNode].h- nodes[self.exitNode].h 
    
    def mdotenergy(self,mdot):
        self.WExtracted=mdot* self.workExtracted 