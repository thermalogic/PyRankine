
"""
General Object-oriented  Abstraction and JSON Textual Model of Rankine Cycle 

 Example Rankine Cycles:
    Michael J . Moran. Fundamentals of Engineering Thermodynamics(7th Edition). John Wiley & Sons, Inc. 2011
    Chapter 8 : Vapour Power Systems Example

         EXAMPLE 8.1 ：An Ideal Regenerative Cycle, Page 438
         EXAMPLE 8.2: Analyzing a Rankine Cycle with Irreversibilities，Page 444
         EXAMPLE 8.5 ：A Regenerative Cycle with Open Feedwater Heater,Page 456

Run: 

python rankine.py
  
Last updated: 2018.05.10

Author:Cheng Maohua  Email: cmh@seu.edu.cn

"""
import glob
from rankinecycle.simcycle import SimRankineCycle

json_filesname_str='./data/txtcycle/rankine8[0-9].json'
#json_filesname_str='./data/txtcycle/rankine85.json'
json_filesname=glob.glob(json_filesname_str)

Wcycledot = 100 # MW
mdot= 150*3600 # kg/h  
for i in range(len(json_filesname)):
   cycle=SimRankineCycle(json_filesname[i])
   cycle.CycleSimulator()
 
   # Specified Net Output Power(MW)
   cycle.CycleSpecifiedSimulator(SetPower=Wcycledot)      
 
   # Specified Mass Flow(kg/h)
   cycle.CycleSpecifiedSimulator(SetMass=mdot)   
   