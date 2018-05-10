# -*- coding: utf-8 -*-
"""
Step4-json-dict: Advanced @  Data Structures,Program architecture, Algorithms
                
        object-oriented programming,general module

  The General Simulator of Rankine Cycle

  * Examples of Rankine Cycle
 
    Michael J . Mora. Fundamentals of Engineering Thermodynamics(7th Edition). John Wiley & Sons, Inc. 2011
     
    Chapter 8 : Vapour Power Systems Example

    * EXAMPLE 8.1 ：An Ideal Regenerative Cycle, Page 438

    * EXAMPLE 8.5 ：A Regenerative Cycle with Open Feedwater Heater,Page 456

Runner of the General Simulator of Rankine Cycle 
  
Last updated: 2018.05.10
Author:Cheng Maohua  Email: cmh@seu.edu.cn

"""
import glob
import rankine_cycle as rkc

json_filesname_str=r'./cyclefile/rankine8[0-9].json'

#json_filesname_str=r'./cyclefile/rankine85.jsonv'
    
json_filesname=glob.glob(json_filesname_str)


cycle=[]
for i in range(len(json_filesname)):
    cycle.append(rkc.SimRankineCycle(json_filesname[i]))
    cycle[i].CycleSimulator()

# Specified Net Output Power(MW)
Wcycledot = 100
for i in range(len(json_filesname)):
    cycle[i].SpecifiedNetOutputPowerSimulatorAndOutput(Wcycledot)      

#  Specified Mass Flow (kg/h)   
mdot= 150*3600 # kg/h   
for i in range(len(json_filesname)):
    cycle[i].SpecifiedMassFlowSimulatorAndOutput(mdot)        