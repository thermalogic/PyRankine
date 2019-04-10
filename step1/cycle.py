"""
Step 1 : Abstraction and Textual Representation of The Rankine Cycle(Example 8.1,8.2)

cycle Module

License: this code is in the public domain

Cheng Maohua(cmh@seu.edu.cn)

"""
from nodes import * 
from devices import * 


def CalCycle(Devices, Cycle):
    totalWin = 0
    totalWout = 0
    totalQin = 0
    for dev in Devices.values():
        if (dev["energy"] == "Qin"):
            totalQin += dev["qindot"]
        if (dev["energy"] == "Wout"):
            totalWout += dev['wdot']
        if (dev["energy"] == "Win"):
            totalWin += dev['wdot']

    # performance
    Cycle['eta'] = (totalWout - totalWin) / totalQin
    Cycle['HeatRate'] = 3600.0 /  Cycle['eta'] 
    Cycle['SteamRate'] =  Cycle['HeatRate'] / totalQin   
    Cycle['mdot'] = (Cycle['Wdot']*10**3*3600)/(totalWout - totalWin)      
    Cycle['Win']= Cycle['mdot']*totalWin/(1000.0 * 3600.0)
    Cycle['Wout']=Cycle['mdot']*totalWout/(1000.0 * 3600.0)
    Cycle['Qin']=Cycle['mdot']*totalQin /(1000.0 * 3600.0)