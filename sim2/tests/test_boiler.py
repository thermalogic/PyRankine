import unittest

import sys
sys.path.append('../')
from components.node import Node
from components.boiler import Boiler

class BoilerTest (unittest.TestCase):

    def setUp(self):

        self.samplenodes = [
            {"name": "Boiler to Turbine",
                "id": 0,
                "p": 8.0,
                "t": 480.0,
                "x": 1.0,
                "fdot": 1.0,
                "h": 3349.5266902175404,
                "s": 6.661057438926857,
                "v": 0.040364941230239954,
                "mdot": 368813.0888854596
             }, {
                "name": "FW Pump to Boiler",
                "id": 1,
                "p": 8.0,
                "t": 165.85457047406948,
                "x": 0.0,
                "fdot": 1.0,
                "h": 705.2157182424864,
                "s": 1.9920831369740433,
                "v": 0.0011036643191215912,
                "mdot": 368813.0888854596
            }]

        self.samplecase = {
            "name": "Boiler",
            "inNode": 1,
            "outNode": 0,
            "heatAdded": 2644.3109719750537,
            "QAdded": 270.9045826521754
        }

        self.nodes = [None for i in range(len(self.samplenodes))]
        oID=0
        iID=1
        self.nodes[iID] = Node(self.samplenodes[iID])
        self.nodes[oID] = Node(self.samplenodes[oID])

        self.dictDev = {"name": "Boiler1", "inNode": iID, "outNode": oID}
        self.testcase = Boiler(self.dictDev)

    def test_state(self):
        self.testcase.state(self.nodes)

    def test_balance(self):
        places = 6
        self.testcase.state(self.nodes)
        self.testcase.balance()
        self.assertAlmostEqual(self.testcase.heatAdded,
                               self.samplecase["heatAdded"], places)

    def test_sm_energy(self):
        places = 6
        self.testcase.state(self.nodes)
        self.testcase.balance()
        self.testcase.sm_energy()
        self.assertAlmostEqual(self.testcase.QAdded,
                               self.samplecase["QAdded"], places)

if __name__ == '__main__':
    unittest.main()
