"""

Devices Module

Step 1 :The Simple Abstraction of The Rankine Cycle 8.1,8.2  with list,dict,function

License: this code is in the public domain

Cheng Maohua(cmh@seu.edu.cn)

"""

from seuif97 import *


def CalBoiler(Boiler, Nodes):
    """Boiler {'minID':None, 'moutID': None, 'qindot': None}"""
    iID = Boiler['minID']
    oID = Boiler['moutID']
    # 1 Energy
    Boiler['qindot'] = Nodes[oID]['h']-Nodes[iID]['h']


def CalTurbine(Turbine, Nodes):
    """Turbine {'minID':None, 'moutID': None,'eta':None, 'wdot': None}"""
    iID = Turbine['minID']
    oID = Turbine['moutID']
    # 1 Nodes[oID]
    sout_s = Nodes[iID]['s']
    hout_s = ps2h(Nodes[oID]['p'], sout_s)
    Nodes[oID]['h'] = Nodes[iID]['h'] - Turbine['eta']*(Nodes[iID]['h']-hout_s)
    Nodes[oID]['t'] = ph2t(Nodes[oID]['p'], Nodes[oID]['h'])
    Nodes[oID]['s'] = ph2s(Nodes[oID]['p'], Nodes[oID]['h'])
    Nodes[oID]['x'] = ph2x(Nodes[oID]['p'], Nodes[oID]['h'])
    # 2 Energy
    Turbine['wdot'] = Nodes[iID]['h'] - Nodes[oID]['h']


def CalCondenser(Condenser, Nodes):
    """Condenser {'minID':None, 'moutID': None, 'qoutdot': None}"""
    iID = Condenser['minID']
    oID = Condenser['moutID']
    # 1 Energy
    Condenser['qoutdot'] = Nodes[iID]['h']-Nodes[oID]['h']


def CalPump(Pump, Nodes):
    """Pump {'minID': None, 'moutID': None, 'eta':None,'wdot': None}"""
    iID = Pump['minID']
    oID = Pump['moutID']
    # 1 Nodes[oID]
    sout_s = Nodes[iID]['s']
    hout_s = ps2h(Nodes[oID]['p'], sout_s)
    Nodes[oID]['h'] = Nodes[iID]['h']+(hout_s - Nodes[iID]['h'])/Pump['eta']
    Nodes[oID]['t'] = ph2t(Nodes[oID]['p'], Nodes[oID]['h'])
    Nodes[oID]['s'] = ph2s(Nodes[oID]['p'], Nodes[oID]['h'])
    Nodes[oID]['x'] = ph2x(Nodes[oID]['p'], Nodes[oID]['h'])
    # 2 Energy
    Pump['wdot'] = Nodes[oID]['h'] - Nodes[iID]['h']


def CalDevices(Boiler, Turbine, Pump, Condenser, Nodes):
    CalTurbine(Turbine, Nodes)
    CalPump(Pump, Nodes)
    CalBoiler(Boiler, Nodes)
    CalCondenser(Condenser, Nodes)
