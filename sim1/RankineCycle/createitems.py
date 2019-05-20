
"""
 The Simulator 1: General Abstraction and CSV Textual Model of Rankine Cycle 

 Author:Cheng Maohua  Email: cmh@seu.edu.cn

"""
import copy
import csv
from . import compdict


def CreateNodeFromCSV(filename):
    """ nodes in the  csv file"""

    # readlines() to the end of file
    countNodes = len(open(filename, 'r').readlines()) - 1
    nodes = [{'NAME': None, 'NID': None, 'p': None, 't': None, 'h': None,
              's': None, 'x': None, 'fdot': None} for i in range(countNodes)]

    #  re-open the file to its head
    csvfile = open(filename, 'r')
    reader = csv.DictReader(csvfile)
    for line in reader:
        i = int(line['NID'])
        nodes[i]['NAME'] = line['NAME']
        nodes[i]['NID'] = i
        try:
            nodes[i]['p'] = float(line['p'])
        except:
            pass
        try:
            nodes[i]['t'] = float(line['t'])
        except:
            pass
        try:
            nodes[i]['x'] = float(line['x'])
        except:
            pass
        try:
            nodes[i]['fdot'] = float(line['fdot'])
        except:
            pass

    csvfile.close()
    return nodes


def CreateDeviceFromCSV(filename):
    """ devices in the  csv file"""
    csvfile = open(filename, 'r')
    reader = csv.DictReader(csvfile)

    devices = {}
    for row in reader:
        temp = copy.deepcopy(compdict)
        curdev = temp[row['TYPE']]
        # Please code the connection between nodes and device carefully! --
        if row['TYPE'] in ["BOILER", "TURBINE-EX0", "PUMP", "CONDENSER"]:
            curdev['minID'] = int(row['NODE0'])
            curdev['moutID'] = int(row['NODE1'])
        # TURBINE-EX1
        if row['TYPE'] in ["TURBINE-EX1"]:
            curdev['minID'] = int(row['NODE0'])
            curdev['moutID'] = int(row['NODE1'])
            curdev['mexID'] = int(row['NODE2'])
        # FWH-OPENDED-DW0
        if row['TYPE'] in ["FWH-OPEN-DW0"]:
            curdev['stminID'] = int(row['NODE0'])
            curdev['fwinID'] = int(row['NODE1'])
            curdev['fwoutID'] = int(row['NODE2'])

        try:
            curdev['eta'] = float(row['ETA'])
        except:
            pass

        devices[row['NAME']] = curdev

    csvfile.close()
    return devices
