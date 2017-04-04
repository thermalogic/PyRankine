# -*- coding: utf-8 -*-
"""

Step 2 ：

Step by step codes of the ideal rankine cycle simulator to demonstrate: 

    Data Structures+ Algorithms = Programs

The ideal rankine cycle as 
   
    ┌─── Node 0 ── Turbine ── Node 1 ──┐
    |                                  |
  Boiler                            Condenser
    |                                  |
    └─── Node 3 ──   Pump  ── Node 2 ──┘  

 Michael J . Mora. 
     Fundamentals of Engineering Thermodynamics(7th Edition). John Wiley & Sons, Inc. 2011
     Chapter 8 : Vapour Power Systems Example 8.1:Analyzing an Ideal Rankine Cycle  Page 438

Author:Cheng Maohua
Email: cmh@seu.edu.cn

"""
import csv

import node
import turbine
import pump
import condenser
import boiler


def read_nodesfile(filename):
    """ nodes in the  csv file"""
    countNodes = len(open(filename, 'r').readlines()) - 1
    nodes = [None for i in range(countNodes)]
    csvfile = open(filename, 'r')
    reader = csv.DictReader(csvfile)
    for line in reader:
        i = int(line['NID'])
        nodes[i] = node.Node(line['NAME'], i)
        try:
            nodes[i].p = float(line['p'])
        except:
            nodes[i].p = None
        try:
            nodes[i].t = float(line['t'])
        except:
            nodes[i].t = None
        try:
            nodes[i].x = float(line['x'])
        except:
            nodes[i].x = None

        if line['p'] != '' and line['t'] != '':
            nodes[i].pt()
        elif line['p'] != '' and line['x'] != '':
            nodes[i].px()
        elif line['t'] != '' and line['x'] != '':
            nodes[i].tx()

    return nodes, countNodes


def read_devicefile(filename):
    devFile = open(filename, 'r')
    discardHeader = devFile.readline()
    Comps = {}
    i = 0
    begId = 2
    for line in devFile:
        dev = line.split(',')
        if dev[1] == "TURBINE":
            Comps[dev[0]] = turbine.Turbine(dev[0], int(dev[begId]),  int(dev[begId + 1]))
        elif dev[1] == "BOILER":
            Comps[dev[0]] = boiler.Boiler(
                dev[0], int(dev[begId]), int(dev[begId + 1]))
        elif dev[1] == "CONDENSER":
            Comps[dev[0]] = condenser.Condenser(
                dev[0], int(dev[begId]), int(dev[begId + 1]))
        elif dev[1] == "PUMP":
            Comps[dev[0]] = pump.Pump(dev[0], int(dev[begId]),  int(dev[begId + 1]))
      
        i = i + 1

    DevNum = i
    return Comps, DevNum

class RankineCycle(object):
    
      def __init__(self,name,nodefilename,devfilename):
          self.name=name
          self.nodes=[]
          self.devs={}
          self.nodes, self.NodeNum = read_nodesfile(nodefilename)
          self.devs, self.DevNum = read_devicefile(devfilename)

     
      def state(self):
          for key in  self.devs:
              self.devs[key].state(self.nodes)
    
      def simulate(self):
          for key in  self.devs:
              self.devs[key].simulate(self.nodes)

          self.bwr = self.devs['Pump'].workRequired / self.devs['Turbine'].workExtracted
          self.efficiency = (self.devs['Turbine'].workExtracted - self.devs['Pump'].workRequired) / (self.devs['Boiler'].heatAdded)              

      def spower_simulate(self,Wcycledot):
          self.Wcycledot=Wcycledot   
          self.mdot = Wcycledot * 1000.0* 3600.0 / (self.devs['Turbine'].workExtracted -self.devs['Pump'].workRequired)
          for key in  self.devs:
              self.devs[key].mdotenergy(self.mdot)                  
  
      def cw_simulate(self):
          # condenser cooling water
          self.nodew = []
          self.nodew.append(node.Node('CW-Inlet',0))
          self.nodew.append(node.Node('CW-Outlet',1))

          self.nodew[0].t = 15
          self.nodew[0].x = 0
          self.nodew[1].t = 35
          self.nodew[1].x = 0
          self.nodew[0].tx()
          self.nodew[1].tx()

          self.devs['Condenser'].cw_nodes( 0, 1)
          self.devs['Condenser'].cw_simulate(self.nodew)

      def export(self):
          print(" \n --------  %s   ----------------------------------"%self.name)
          print("The net power output of the cycle: ", self.Wcycledot, "MW")
          print("Efficiency: ", '%.2f' % (self.efficiency * 100), "%")
          print("The back work ratio: ", '%.2f' % (self.bwr * 100), "%")
          print("The mass flow rate: ",  '%.2f' % self.mdot, "kg/h")
          print('The rate of heat transfer as the fluid passes the boiler: ',
          '%.2f' % self.devs['Boiler'].Qindot, 'MW')
          print(" \n ------- The Condenser Cooling Water  --------------")
          print("Cooling water enters the condenser T:", self.nodew[0].t, u'°C')
          print("Cooling water exits  the condenser T:", self.nodew[1].t, u'°C')
          print('The rate of heat transfer from the condensing steam: ',
          '%.2f' % self.devs['Condenser'].Qoutdot, 'MW')
          print('The mass flow rate of the condenser cooling water: ', '%.2f' %
          self.devs['Condenser'].mcwdot, 'kg/h')
          print(" \n -------- NODES  -----------------------------------")
          print("\nNodeID\tName\tP\tT\tH\tS\tV\tX")
          for node in self.nodes:
              print(node)


if __name__ == '__main__':
    nds_filename = 'rankine81-nds.csv'
    dev_filename = 'rankine81-dev.csv'
    c81=RankineCycle("Rankine81", nds_filename,  dev_filename)
    c81.state()
    c81.simulate()
    # Specified Net Output Power
    Wcycledot = 100
    c81.spower_simulate(Wcycledot)  
    c81.cw_simulate()    
    c81.export()