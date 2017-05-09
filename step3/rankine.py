# -*- coding: utf-8 -*-
"""
Runner of the General Simulator of Rankine Cycle 
  
Last updated: 2017.05.05

Author:Cheng Maohua  Email: cmh@seu.edu.cn

"""
import glob
import rankine_cycle as rkc

#nds_filesname_str=r'./cyclefile/rankine?[0-9]-nds.csv'
#dev_filesname_str=r'./cyclefile/rankine??-dev.csv'

nds_filesname_str=r'./cyclefile/rankine85-nds.csv'
dev_filesname_str=r'./cyclefile/rankine85-dev.csv'
    
nds_filesname=glob.glob(nds_filesname_str)
dev_filesname=glob.glob(dev_filesname_str)

cycle=[]
for i in range(len(nds_filesname)):
    cycle.append(rkc.SimRankineCycle(nds_filesname[i],dev_filesname[i]))
    cycle[i].CycleSimulator()

# Specified Net Output Power(MW)
Wcycledot = 100
for i in range(len(nds_filesname)):
    cycle[i].SpecifiedNetOutputPowerSimulatorAndOutput(Wcycledot)      

#  Specified Mass Flow (kg/h)   
mdot= 150*3600 # kg/h   
for i in range(len(nds_filesname)):
    cycle[i].SpecifiedMassFlowSimulatorAndOutput(mdot)        