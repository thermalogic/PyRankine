
"""
The PyRankine: the  hybrid steady-state simulator of Rankine Cycle

run:

python rankinesim.py

Author: Cheng Maohua, Email:cmh@seu.edu.cn
"""
from platform import os
from rankine.utils import OutFiles, create_dictcycle_from_jsonfile
from rankine.rankineobj import RankineCycle


curpath = os.path.abspath(os.path.dirname(__file__))
rankinefilename = curpath+'\\'+'./jsonmodel/N600.json'
dictcycle = create_dictcycle_from_jsonfile(rankinefilename)

# 1kg only
curcycle = RankineCycle(dictcycle)

curcycle.simulator_sm() # use sequential-modular approach
#curcycle.simulator_eo()   # use equation-oriented approach
curcycle.simulator_performance()
OutFiles(curcycle)
OutFiles(curcycle, curpath+'\\'+'./result/N600-1.txt')

