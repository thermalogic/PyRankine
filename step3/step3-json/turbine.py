"""
Step 3-json ：Basic Object-Orientation Abstraction  and Data Representation of The Ideal Rankine Cycle

 
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

class Turbine(object):

    """
    Turbine class:   Represents a turbine in the Rankine cycle
    """

    def __init__(self,  dictDev):
        """
        Initializes the turbine with nodes
        """
        self.name = dictDev['name']
        self.inletNode = dictDev['inNode']
        self.exitNode = dictDev['exNode']
    
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