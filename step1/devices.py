"""
Step 1 : Abstraction and Textual Representation of The Rankine Cycle(Example 8.1,8.2)

devices Module

License: this code is in the public domain

Cheng Maohua(cmh@seu.edu.cn)

"""

import csv
import copy
from seuif97 import *
from nodes import * 

def CalTurbine(Turbine, Nodes):
    """Turbine"""
    iID = Turbine['minID']
    oID = Turbine['moutID']
    # 1 Nodes[oID]
    sout_s = Nodes[iID]['s']
    hout_s = ps2h(Nodes[oID]['p'], sout_s)
    Nodes[oID]['h'] = Nodes[iID]['h'] - Turbine['eta']*(Nodes[iID]['h']-hout_s)
    Nodes[oID]['t'] = ph2t(Nodes[oID]['p'], Nodes[oID]['h'])
    Nodes[oID]['s'] = ph2s(Nodes[oID]['p'], Nodes[oID]['h'])
    # 2 Energy
    Turbine['wdot'] = Nodes[iID]['h'] - Nodes[oID]['h']


def CalPump(Pump, Nodes):
    """Pump"""
    iID = Pump['minID']
    oID = Pump['moutID']
    # 1 Nodes[oID]
    sout_s = Nodes[iID]['s']
    hout_s = ps2h(Nodes[oID]['p'], sout_s)
    Nodes[oID]['h'] = Nodes[iID]['h']+(hout_s - Nodes[iID]['h'])/Pump['eta']
    Nodes[oID]['t'] = ph2t(Nodes[oID]['p'], Nodes[oID]['h'])
    Nodes[oID]['s'] = ph2s(Nodes[oID]['p'], Nodes[oID]['h'])
    # 2 Energy
    Pump['wdot'] = Nodes[oID]['h'] - Nodes[iID]['h']


def CalBoiler(Boiler, Nodes):
    """Boiler"""
    iID = Boiler['minID']
    oID = Boiler['moutID']
    # 2 Energy
    Boiler['qindot'] = Nodes[oID]['h']-Nodes[iID]['h']


def CalCondenser(Condenser, Nodes):
    """Condenser"""
    iID = Condenser['minID']
    oID = Condenser['moutID']
    # 2 Energy
    Condenser['qoutdot'] = Nodes[iID]['h']-Nodes[oID]['h']


def CalDevices(Devices, Nodes):
    keys = list(Devices.keys())
    devCounts = len(keys)
    i = 0
    while len(keys) != 0 and i < (devCounts+1):
        i += 1
        for dev in keys:
            try:
                Devices[dev]["fun"](Devices[dev], Nodes)
                keys.remove(dev)
            except:
                pass


compdict = {
    "BOILER": {'minID': None, 'moutID': None, 'qindot': None, "energy": "Qin", "fun": CalBoiler},
    "TURBINE-EX0": {'minID': None, 'moutID': None, 'eta': None, 'wdot': None, "energy": "Wout", "fun": CalTurbine},
    "PUMP": {'minID': None, 'moutID': None, 'eta': None, 'wdot': None, "energy": "Win", "fun": CalPump},
    "CONDENSER": {'minID': None, 'moutID': None, 'qoutdot': None, "energy": "Qout", "fun": CalCondenser}
}


def read_DevicesFile(filename):
    """ devices in the  csv file"""
    csvfile = open(filename, 'r')
    reader = csv.DictReader(csvfile)

    devices = {}
    temp = copy.deepcopy(compdict)
    for row in reader:
        curdev = temp[row['TYPE']]
        curdev['minID'] = int(row['minID'])
        curdev['moutID'] = int(row['moutID'])
        try:
            curdev['eta'] = float(row['eta'])
        except:
            pass

        devices[row['NAME']] = curdev

    csvfile.close()
    return devices
