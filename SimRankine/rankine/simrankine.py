
"""
 The PyRankine: the  hybrid steady-state simulator of Rankine Cycle

* Sequential-modular(SM)： Simulator_SM(self)

* equation-oriented(EO)： Simulator_EO(self)

"""
from .rankineobj import RankineCycle
from .utils import OutFiles
from platform import os


class SimRankineCycle:
    """ Input :rankine dict"""

    def __init__(self, rankinecycle):
        self.idictcycle = rankinecycle
        self.cycle = RankineCycle(self.idictcycle)
        curpath = os.path.abspath(os.path.dirname(__file__))
        self.prefixResultFileName = curpath+'\\' + \
            '../result/'+self.idictcycle['name']

    def simulator_eo(self):
        self.cycle.simulator_eo()

    def simulator_em(self):
        self.cycle.simulator_sm()

    def simulator_performance(self):
        self.cycle.simulator_performance()

    def specified_simulator(self, set_power=None, set_mass=None):
        # Specified Simulating： Power or Mass Flow
        self.cycle.specified_simulator(set_power, set_mass)

        # output to files
        if set_power is not None:
            outprefix = self.prefixResultFileName + '-sp'
        else:
            outprefix = self.prefixResultFileName + '-sm'
        # output to text
        OutFiles(self.cycle)
        OutFiles(self.cycle, outprefix + '.txt')
