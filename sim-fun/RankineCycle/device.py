
"""
 The Simulator 1: General Abstraction and CSV Textual Model of Rankine Cycle 

 Author:Cheng Maohua  Email: cmh@seu.edu.cn

"""
from seuif97 import ps2t, ps2h, ps2x, ph2t, ph2s, ph2x


def CalBoiler(Boiler, Nodes, Task):
    """ 
      "BOILER": {'minID': None, 'moutID': None, 
                'qindot': None, 
                "energy": "Qin", 
                "fun": CalBoiler}
    """
    iND = Nodes[Boiler['minID']]
    oND = Nodes[Boiler['moutID']]
    if (Task == "State"):
        pass

    if (Task == "Balance"):
        # 2 Mass and Energy Balance
        if iND['fdot'] != None:
            oND['fdot'] = iND['fdot']
        if oND['fdot'] != None:
            iND['fdot'] = oND['fdot']

        Boiler['qindot'] = oND['fdot'] * oND['h']-iND['fdot']*iND['h']


def CalTurbineEx0(TurbineEx0, Nodes, Task):
    """
     "TURBINE-EX0": {'minID': None, 'moutID': None, 'eta': None, 
                    'wdot': None,
                    "energy": "Wout", 
                    "fun": CalTurbineEx0}

    """
    iND = Nodes[TurbineEx0['minID']]
    oND = Nodes[TurbineEx0['moutID']]
    if (Task == "State"):
        # 1 oND
        if TurbineEx0['eta'] == 1.0:
            oND['s'] = iND['s']
            oND['t'] = ps2t(oND['p'], oND['s'])
            oND['h'] = ps2h(oND['p'], oND['s'])
            oND['x'] = ps2x(oND['p'], oND['s'])
        else:
            sout_s = iND['s']
            hout_s = ps2h(oND['p'], sout_s)
            oND['h'] = iND['h'] - TurbineEx0['eta']*(iND['h']-hout_s)
            oND['t'] = ph2t(oND['p'], oND['h'])
            oND['s'] = ph2s(oND['p'], oND['h'])
            oND['x'] = ph2x(oND['p'], oND['h'])

    if (Task == "Balance"):
        # 2 Mass and Energy Balance
        if iND['fdot'] != None:
            oND['fdot'] = iND['fdot']
        if oND['fdot'] != None:
            iND['fdot'] = oND['fdot']

        TurbineEx0['wdot'] = iND['fdot'] * (iND['h'] - oND['h'])


def CalPump(Pump, Nodes, Task):
    """
    "PUMP": {'minID': None, 'moutID': None, 'eta': None, 
             'wdot': None,
             "energy": "Win",
             "fun": CalPump}
    """
    iND = Nodes[Pump['minID']]
    oND = Nodes[Pump['moutID']]
    if Task == "State":
        # 1 oND
        sout_s = iND['s']
        hout_s = ps2h(oND['p'], sout_s)
        oND['h'] = iND['h'] + (hout_s - iND['h'])/Pump['eta']
        oND['t'] = ph2t(oND['p'], oND['h'])
        oND['s'] = ph2s(oND['p'], oND['h'])
        oND['x'] = ph2x(oND['p'], oND['h'])

    if Task == "Balance":
        # 2 Mass and Energy Balance
        if iND['fdot'] != None:
            oND['fdot'] = iND['fdot']
        if oND['fdot'] != None:
            iND['fdot'] = oND['fdot']

        Pump['wdot'] = oND['fdot']*oND['h'] - iND['fdot']*iND['h']


def CalTurbineEx1(TurbineEx1, Nodes, Task):
    """
      "TURBINE-EX1":{'minID': None, 'moutID': None, 'mexID': None ,'eta': None,
                   'wdot': None,
                   "energy": "Wout",
                   "fun": CalTurbineEx1},

    """
    iND = Nodes[TurbineEx1['minID']]
    oND = Nodes[TurbineEx1['moutID']]
    eND = Nodes[TurbineEx1['mexID']]
    if Task == "State":
        # 1 oND
        if TurbineEx1['eta'] == 1.0:
            eND['s'] = iND['s']
            eND['t'] = ps2t(eND['p'], eND['s'])
            eND['h'] = ps2h(eND['p'], eND['s'])
            eND['x'] = ps2x(eND['p'], eND['s'])

            oND['s'] = iND['s']
            oND['t'] = ps2t(oND['p'], oND['s'])
            oND['h'] = ps2h(oND['p'], oND['s'])
            oND['x'] = ps2x(oND['p'], oND['s'])

        else:
            isoh = ps2h(eND['p'], iND['s'])
            eND['h'] = iND['h'] - TurbineEx1['eta']*(iND['h'] - isoh)
            eND['t'] = ph2t(eND['p'], eND['h'])
            eND['s'] = ph2s(eND['p'], eND['h'])
            eND['x'] = ph2x(eND['p'], eND['h'])

            isoh = ps2h(oND['p'], eND['s'])
            oND['h'] = eND['h'] - TurbineEx1['eta']*(eND['h'] - isoh)
            oND['t'] = ph2t(oND['p'], oND['h'])
            oND['s'] = ph2s(oND['p'], oND['h'])
            oND['x'] = ph2x(oND['p'], oND['h'])

    if Task == "Balance":
        # 2 Mass and Energy Balance
        oND['fdot'] = iND['fdot'] - eND['fdot']
        TurbineEx1['wdot'] = eND['fdot'] * (iND['h'] - eND['h'])
        TurbineEx1['wdot'] += oND['fdot'] * (iND['h'] - oND['h'])


def CalOpenFWHDw0(Heater, Nodes, Task):
    """
      "FWH-OPEN-DW0":{'stminID': None, 'fwinID': None, 'fwoutID': None, 'eta': None,
                    'qAdded': None, 
                    "energy": "internel", 
                    "fun": CalOpenFWHDw0}
    """
    siND = Nodes[Heater['stminID']]
    fwiND = Nodes[Heater['fwinID']]
    fwoND = Nodes[Heater['fwoutID']]
    if Task == "State":
        pass

    if Task == "Balance":
        # Mass and Energy Balance
        heatAdded = fwoND['fdot'] * (fwoND['h'] - fwiND['h'])
        heatExtracted = heatAdded
        siND['fdot'] = heatExtracted / (siND['h'] - fwiND['h'])
        # mass blance equation
        fwiND['fdot'] = fwoND['fdot'] - siND['fdot']


def CalCondenser(Condenser, Nodes, Task):
    """
     "CONDENSER": {'minID': None, 'moutID': None, 
                  'qoutdot': None,
                  "energy": "Qout",
                  "fun": CalCondenser}
    """
    iND = Nodes[Condenser['minID']]
    oND = Nodes[Condenser['moutID']]

    if Task == "State":
        pass

    if Task == "Balance":
        # 2 Mass and Energy Balance
        if iND['fdot'] != None:
            oND['fdot'] = iND['fdot']
        if oND['fdot'] != None:
            iND['fdot'] = oND['fdot']

        Condenser['qoutdot'] = iND['fdot'] * \
            iND['h'] - oND['fdot']*oND['h']


def CalDevices(Devices, Nodes):
    """ Cal Devices """ 
    # 1 Task: States
    for dev in Devices.keys():
        Devices[dev]["fun"](Devices[dev], Nodes, "State")

    # 2 In Order！
    keys = list(Devices.keys())
    devCounts = len(keys)
    i = 0
    fdotok = False
    while fdotok == False:
        for curdev in keys:
            try:
                Devices[curdev]["fun"](Devices[curdev], Nodes, "Balance")
                keys.remove(curdev)
            except:
                pass
        i += 1
        if (i > devCounts+1 or len(keys) == 0): 
            fdotok = True
