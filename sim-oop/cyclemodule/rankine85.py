cycle = {}
cycle["name"] = "Rankine85"
cycle["nodes"] = [
    {
        "name": "Boiler to Turbine",
        "id": 0,
        "p": 8.0,
        "t": 480.0,
        "x": None,
        "fdot": 1
    },
    {
        "name": "Extracted Steam To Opened FWH",
        "id": 1,
        "p": 0.7,
        "t": None,
        "x": None,
        "fdot": None
    },
    {
        "name": "Exhausted Steam to CD",
        "id": 2,
        "p": 0.008,
        "t": None,
        "x": None,
        "fdot": None
    },
    {
        "name": "Condensate Water to CDW Pump",
        "id": 3,
        "p": 0.008,
        "t": None,
        "x": 0,
        "fdot": None
    },
    {
        "name": "CDW Pump to Opened FWH",
        "id": 4,
        "p": 0.7,
        "t": None,
        "x": 0,
        "fdot": None
    },
    {
        "name": "Opened FWH to FW Pump",
        "id": 5,
        "p": 0.7,
        "t": None,
        "x": 0,
        "fdot": None
    },
    {
        "name": "FW Pump to Boiler",
        "id": 6,
        "p": 8.0,
        "t": None,
        "x": None,
        "fdot": None
    }
]

cycle["comps"] = [
    {
        "name": "Turbine Ex1",
        "devtype": "TURBINE-EX1",
        "ef": 0.85,
        "iNode": 0,
        "oNode": 2,
        "eNode": 1
    },
    {
        "name": "Condenser",
        "devtype": "CONDENSER",
        "iNode": 2,
        "oNode": 3
    },
    {
        "name": "Condensate Pump",
        "devtype": "PUMP",
        "ef": 1.00,
        "iNode": 3,
        "oNode": 4
    },
    {
        "name": "Opened Feedwater Heater",
        "devtype": "FWH-OPEN-DW0",
        "iNode": 1,
        "iNode_fw": 4,
        "oNode_fw": 5
    },
    {
        "name": "Feedwater Pump",
        "devtype": "PUMP",
        "ef": 1.00,
        "iNode": 5,
        "oNode": 6
    },
    {
        "name": "Boiler",
        "devtype": "BOILER",
        "iNode": 6,
        "oNode": 0
    }
]
