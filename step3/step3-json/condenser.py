"""
  Step 3-json ：Basic Object-Orientation Abstraction  and Data Representation of The Ideal Rankine Cycle
 
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

    def __init__(self,dictDev):
        """
        Initializes the condenser with nodes
        """
        self.name = dictDev['name']
        self.inletNode = dictDev['inNode']
        self.exitNode = dictDev['exNode']
       
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
