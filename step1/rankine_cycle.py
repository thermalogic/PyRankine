
"""

Rankine Cycle Module

Step 1 :The Simple Abstraction of The Rankine Cycle 8.1,8.2  with list,dict,function

License: this code is in the public domain

Cheng Maohua(cmh@seu.edu.cn)

"""

def CalCycle(Boiler, Turbine, Pump,Condenser, Cycle):
    Cycle['eta'] = (Turbine['wdot'] - Pump['wdot']) / Boiler['qindot']
    Cycle['bwr'] = Turbine['wdot']/Pump['wdot']
    
    Cycle['mdot'] = (Cycle['Wdot']*10**3*3600)/(Turbine['wdot'] -Pump['wdot'])       # mass flow rate in kg/h
    
    Boiler['Qindot'] = Cycle['mdot']*Boiler['qindot']/(3600*10**3)
    Cycle['Qindot'] = Boiler['Qindot']
    
    Condenser['Qoutdot']= Cycle['mdot']* Condenser['qoutdot']/(3600*10**3)
    Cycle['Qoutdot']=Condenser['Qoutdot']
    
    Cycle['HeatRate']=3600.0 /  Cycle['eta']
    Cycle['SteamRate'] =  Cycle['HeatRate'] /  Boiler['qindot']