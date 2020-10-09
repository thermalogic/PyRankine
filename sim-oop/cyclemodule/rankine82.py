cycle={}
cycle["name"]="Rankine82"
cycle["nodes"] = [
        {
            "name": "Main Steam",
            "id": 0,
            "p": 8.0,
            "t": None,
            "x": 1,
            "fdot": 1
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
            "x": 0,
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
            "name": "Turbine Ex0",
            "devtype": "TURBINE-EX0",
            "ef": 0.85,
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
            "ef": 0.85,
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
