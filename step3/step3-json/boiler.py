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
