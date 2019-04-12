"""
Step 3-json ：Basic Object-Orientation Abstraction  and Data Representation of The Ideal Rankine Cycle
     
        object-oriented programming and json file

The ideal rankine cycle as 
   
    ┌─── Node 0 ── Turbine ── Node 1 ──┐
    │                                  │
  Boiler                            Condenser
    │                                  │
    └─── Node 3 ──   Pump  ── Node 2 ──┘  

 Michael J . Moran. Fundamentals of Engineering Thermodynamics(7th Edition). John Wiley & Sons, Inc. 2011
       Chapter 8 : Vapour Power Systems 
          Example 8.1:Analyzing an Ideal Rankine Cycle  Page 438

Running:

python rankine.py


License: this code is in the public domain

Author:Cheng Maohua
Email: cmh@seu.edu.cn

"""
import json

import node
import boiler
import condenser
import pump
import turbine

# -------------------------------------------------------------------
# compdict
#  1: key:value-> Type String: class  name
#  2  add the new key:value to the dict after you and the new device class/type
# --------------------------------------------------------------------------

compdict = {
    "BOILER": boiler.Boiler,
    "CONDENSER": condenser.Condenser,
    "TURBINE": turbine.Turbine,
    "PUMP":  pump.Pump
}


def read_jsonfile(filename):
    """ rankine cycle in json file"""

    # 1 read json file to dict
    with open(filename, 'r') as f:
        rkcyc = json.loads(f.read())

    # print(rkcyc)
    name = rkcyc["name"]
    dictnodes = rkcyc["nodes"]
    dictcomps = rkcyc["comps"]

    # 2 convert dict nodes to the object nodes
    countNodes = len(dictnodes)
    nodes = [None for i in range(countNodes)]
    for curnode in dictnodes:
        i = int(curnode['id'])
        nodes[i] = node.Node(curnode)

    # 3 convert dict Comps to the object Comps
    DevNum = len(dictcomps)
    Comps = {}
    for curdev in dictcomps:
        Comps[curdev['name']] = compdict[curdev['type']](curdev)

    return name, nodes, countNodes, Comps, DevNum


class RankineCycle(object):

    def __init__(self, rankinefile):
        self.nodes = []
        self.devs = {}
        self.name, self.nodes, self.NodeNum, self.devs, self.DevNum = read_jsonfile(
            rankinefile)

    def state(self):
        for key in self.devs:
            self.devs[key].state(self.nodes)

    def simulate(self):
        for key in self.devs:
            self.devs[key].simulate(self.nodes)

        self.bwr = self.devs['Pump'].workRequired / \
            self.devs['Turbine'].workExtracted
        self.efficiency = (self.devs['Turbine'].workExtracted - self.devs[
                           'Pump'].workRequired) / (self.devs['Boiler'].heatAdded)

    def spower_simulate(self, Wcycledot):
        self.Wcycledot = Wcycledot
        self.mdot = Wcycledot * 1000.0 * 3600.0 / \
            (self.devs['Turbine'].workExtracted -
             self.devs['Pump'].workRequired)
        for key in self.devs:
            self.devs[key].mdotenergy(self.mdot)

    def cw_simulate(self):
        """ Circulating water system：Condenser Cooling Water"""
        cwin = {'name': 'CW-In',
                'id': 0,
                't': 15.0,
                "x": 0}
        cwout = {'name': 'CW-Out',
                 'id': 1,
                 't': 35.0,
                 "x": 0}
        self.nodew = []
        self.nodew.append(node.Node(cwin))
        self.nodew.append(node.Node(cwout))

        self.devs['Condenser'].cw_nodes(0, 1)
        self.devs['Condenser'].cw_simulate(self.nodew)

    def export(self):
        print(" \n --------  {} ----------------------------------".format(self.name))
        print("The net power output: ", self.Wcycledot, "MW")
        print("Efficiency: {:>.2f}%".format(self.efficiency * 100))
        print("The back work ratio: {:>.2f}%".format(self.bwr * 100))
        print("The mass flow rate: {:>.2f}kg/h".format(self.mdot))
        print("The rate of heat transfer as the fluid passes the boiler:{:>.2f}MW".format(
            self.devs['Boiler'].Qindot))
        print(" \n -------  Circulating Water System  --------------")
        print("Cooling water enters the condenser T:", self.nodew[0].t, u'°C')
        print("Cooling water exits  the condenser T:", self.nodew[1].t, u'°C')
        print("The rate of heat transfer from the condensing steam: {:>.2f}MW".format(self.devs['Condenser'].Qoutdot))
        print("The mass flow rate of the condenser cooling water: {:>.2f}kg/h".format(self.devs['Condenser'].mcwdot))
        print(" \n -------- NODES  -----------------------------------")
        print("\nNodeID\tName\tP\tT\tH\tS\tV\tX")
        for inode in self.nodes:
            print(inode)


if __name__ == '__main__':
    rankine_filename = 'rankine81.json'
    c81 = RankineCycle(rankine_filename)
    c81.state()
    c81.simulate()
    # Specified Net Output Power
    Wcycledot = 100
    c81.spower_simulate(Wcycledot)
    c81.cw_simulate()
    c81.export()
