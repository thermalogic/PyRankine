# -*- coding: utf-8 -*-
"""
Step4-csv: General Abstraction and Data Representation of Rankine Cycle
                
    object-oriented programming,general module

The General Simulator of Rankine Cycle

  * Examples of Rankine Cycle
 
    Michael J . Moran. Fundamentals of Engineering Thermodynamics(7th Edition). John Wiley & Sons, Inc. 2011

    Chapter 8 : Vapour Power Systems Example

       * EXAMPLE 8.1 ：An Ideal Regenerative Cycle, Page 438

       * EXAMPLE 8.5 ：A Regenerative Cycle with Open Feedwater Heater,Page 456

Runner of the General Simulator of Rankine Cycle 

python rankine.py

Last updated: 2017.05.05

Author:Cheng Maohua  Email: cmh@seu.edu.cn

"""
import glob
import rankine_cycle as rkc

nds_filesname_str=r'./cyclefile/rankine?[0-9]-nds.csv'
dev_filesname_str=r'./cyclefile/rankine??-dev.csv'

#nds_filesname_str=r'./cyclefile/rankine85-nds.csv'
#dev_filesname_str=r'./cyclefile/rankine85-dev.csv'
    
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