
"""
The Simulator 1: General Abstraction and CSV Textual Model of Rankine Cycle 

- Using List,Dict and Function 

- CSV Textual Model of Rankine Cycle Flowsheet 

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
from RankineCycle.createitems import CreateNodeFromCSV,CreateDeviceFromCSV
from RankineCycle.cycle import  RankineCycle
from RankineCycle.output import OutFiles
import glob

def RankineSimulator(nds_filename,des_filename):
    Nodes = CreateNodeFromCSV(nds_filename)
    Devices =CreateDeviceFromCSV(des_filename)
    Cycle = {'Wdot': 100.0}
    RankineCycle(Nodes,Devices,Cycle)

    cyclename = nds_filename[0:nds_filename.find('-')]
    OutFiles(Nodes, Cycle)
    OutFiles(Nodes, Cycle, cyclename + '-sp.txt')     

if __name__ == '__main__':
    nds_filenames = glob.glob(r'./data/rankine8[0-9]-nds.csv')
    des_filenames = glob.glob(r'./data/rankine??-des.csv')

    for i in range(len(nds_filenames)):
        RankineSimulator(nds_filenames[i],des_filenames[i])