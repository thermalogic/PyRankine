
"""
General Object-oriented Abstraction  of Rankine Cycle 

The Simulator of Rankine Cycle 

  * Input :rankine cycle dict module  

  * output: txt file

 Example Rankine Cycles:
    Michael J . Moran. Fundamentals of Engineering Thermodynamics(7th Edition). John Wiley & Sons, Inc. 2011
    Chapter 8 : Vapour Power Systems Example

         EXAMPLE 8.1 ：An Ideal Regenerative Cycle, Page 438
         EXAMPLE 8.2: Analyzing a Rankine Cycle with Irreversibilities，Page 444
         EXAMPLE 8.5 ：A Regenerative Cycle with Open Feedwater Heater,Page 456

Run: 

python rankine.py
  
Author:Cheng Maohua  Email: cmh@seu.edu.cn

"""
from rankinecycle.cycleobj import RankineCycle
from rankinecycle.cyclehelper import SpecifiedSimulator
from platform import *

if __name__ == "__main__":
    from cyclemodule import rankine81 as r81
    #from cyclemodule import rankine82 as r82
    #from cyclemodule import rankine85 as r85
    Wcycledot = 100  # MW
    mdot = 150*3600  # kg/h

    cycles=[r81]
    #cycles=[r81,r82,r85]
    for curcycle in cycles:
        curpath = os.path.abspath(os.path.dirname(__file__))
        prefixResultFileName= curpath+'\\'+'./result/'+curcycle.cycle['name']

        cycle = RankineCycle(curcycle.cycle)
        # 1 1kg
        cycle.simulator()

        # 2 Specified Net Output Power(MW)
        SpecifiedSimulator(cycle,prefixResultFileName, SetPower=Wcycledot)

        # 3 Specified Mass Flow(kg/h)
        SpecifiedSimulator(cycle,prefixResultFileName,SetMass=mdot)
