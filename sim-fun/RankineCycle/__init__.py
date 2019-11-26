
"""
 The Simulator 1: General Abstraction and CSV Textual Model of Rankine Cycle 

 Author:Cheng Maohua  Email: cmh@seu.edu.cn

"""
from .device import *

# Jume Table and The devices dict prototype in the cycle
compdict = {
    "BOILER": {'minID': None, 'moutID': None,
               'qindot': None,
               "energy": "Qin",
               "fun": CalBoiler},
    "TURBINE-EX0": {'minID': None, 'moutID': None, 'eta': None,
                    'wdot': None,
                    "energy": "Wout",
                    "fun": CalTurbineEx0},
    "PUMP": {'minID': None, 'moutID': None, 'eta': None,
             'wdot': None,
             "energy": "Win",
             "fun": CalPump},
    "CONDENSER": {'minID': None, 'moutID': None,
                  'qoutdot': None,
                  "energy": "Qout",
                  "fun": CalCondenser},
    "TURBINE-EX1": {'minID': None, 'moutID': None, 'mexID': None, 'eta': None,
                    'wdot': None,
                    "energy": "Wout",
                    "fun": CalTurbineEx1},
    "FWH-OPEN-DW0": {'stminID': None, 'fwinID': None, 'fwoutID': None, 'eta': None,
                     'qAdded': None,
                     "energy": "internel",
                     "fun": CalOpenFWHDw0}
}
