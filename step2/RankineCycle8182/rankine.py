import glob

from rankine_cycle import *

nds_filesname = glob.glob(r'./data/rankine8[0-9]-nds.csv')
dev_filesname = glob.glob(r'./data/rankine??-des.csv')

cycle = []
for i in range(len(nds_filesname)):
    cycle.append(SimRankineCycle(nds_filesname[i], dev_filesname[i]))
    cycle[i].CycleSimulator()
    # Specified Net Output Power

for i in range(len(nds_filesname)):
    cycle[i].SimulatorOutput()