
cycle = {}
cycle["name"] = "Rankine81"
cycle["nodes"] = [{
    "name": "Main Steam",
            "id": 0,
            "p": 8.0,
            "t": None,
            "x": 1.0,
            "fdot": 1.0
},
    {
    "name": "Outlet Steam of HP",
            "id": 1,
            "p": 0.008,
            "t": None,
            "x": None,
            "fdot": None
},
    {
    "name": "Condenser Water",
            "id": 2,
            "p": 0.008,
            "t": None,
            "x": 0.0,
            "fdot": None
},
    {
    "name": "Main FeedWater",
            "id": 3,
            "p": 8.0,
            "t": None,
            "x": None,
            "fdot": None
}
]

cycle["comps"] = [
    {
        "name": "TurbineEx0",
        "devtype": "TURBINE-EX0",
        "ef": 1.0,
        "iNode": 0,
        "oNode": 1
    },
    {
        "name": "Condenser",
        "devtype": "CONDENSER",
        "iNode": 1,
        "oNode": 2
    },
    {
        "name": "Feedwater Pump",
        "devtype": "PUMP",
        "ef": 1.0,
        "iNode": 2,
        "oNode": 3
    },
    {
        "name": "Boiler",
        "devtype": "BOILER",
        "iNode": 3,
        "oNode": 0
    }
]
