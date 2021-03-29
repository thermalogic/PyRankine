
"""
python rankinesim_n600_1.py

"""
from platform import os
from rankine.utils import OutFiles, create_dictcycle_from_jsonfile
from rankine.simrankine import SimRankineCycle

curpath = os.path.abspath(os.path.dirname(__file__))
rankinefilename = curpath+'\\'+'./rankinejson/N600_1.json'
dictcycle = create_dictcycle_from_jsonfile(rankinefilename)

cycle600 = SimRankineCycle(dictcycle)
# 1 1kg
cycle600.simulator_eo()
cycle600.simulator_performance()


# 2 Specified Net Output Power(MW)
Wcycledot = 600  # MW
cycle600.specified_simulator(set_power=Wcycledot)

# 3 Specified Mass Flow(kg/h)
mdot = cycle600.cycle.mdot  # 1709996  kg/h
cycle600.specified_simulator(set_mass=mdot)

# 4 Variable parameters: add the (p,t) of boiler output
# 4.1 init
curcycle = cycle600.cycle
obPort = curcycle.comps["BO"].oPort[0]
bp = obPort.p
bt = obPort.t
beta = curcycle.efficiency_cycle
# 4.2 to change parameters
obPort.p = bp+1
obPort.t = bt+1
obPort.pt()
curcycle.simulator_eo()
print("\n--- Variable parameters: add the (p,t) of boiler output  ---\n")
print("p,    t,       eta")
print(bp, bt, beta)
print(obPort.p, obPort.t, curcycle.efficiency_cycle)
