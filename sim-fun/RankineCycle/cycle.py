
"""
 The Simulator 1: General Abstraction and CSV Textual Model of Rankine Cycle 

 Author:Cheng Maohua  Email: cmh@seu.edu.cn

"""
from .node import CalNodeProperties
from .device import CalDevices


def CalCycle(Devices, Cycle):
    """cycle performance """
    totalWin = 0
    totalWout = 0
    totalQin = 0
    for dev in Devices.values():
        if dev["energy"] == "Qin":
            totalQin += dev["qindot"]
        if dev["energy"] == "Wout":
            totalWout += dev['wdot']
        if dev["energy"] == "Win":
            totalWin += dev['wdot']

    # performance
    Cycle['eta'] = (totalWout - totalWin) / totalQin
    Cycle['HeatRate'] = 3600.0 / Cycle['eta']
    Cycle['SteamRate'] = Cycle['HeatRate'] / totalQin
    Cycle['mdot'] = (Cycle['Wdot']*10**3*3600)/(totalWout - totalWin)
    Cycle['Win'] = Cycle['mdot']*totalWin/(1000.0 * 3600.0)
    Cycle['Wout'] = Cycle['mdot']*totalWout/(1000.0 * 3600.0)
    Cycle['Qin'] = Cycle['mdot']*totalQin / (1000.0 * 3600.0)


def RankineCycle(Nodes, Devices, Cycle):
    """cycle all in one """
    CalNodeProperties(Nodes)
    CalDevices(Devices, Nodes)
    CalCycle(Devices, Cycle)
