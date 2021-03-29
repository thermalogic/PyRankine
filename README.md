# PyRankine

[![DOI](https://zenodo.org/badge/85393590.svg)](https://zenodo.org/badge/latestdoi/85393590)

The PyRankine is the general Rankine Cycle simulator of Steady-State Mass and Energy Balance in Python.

Two kind of simulation approachs are provided in the the simulator 

* sequential-modular approach

* equation-oriented approach

## Dependencies：SEUIF97

IAPWS-IF97 high-speed shared library

* https://github.com/PySEE/SEUIF97

Install with pip

```bash
python -m pip install seuif97
```

## The Example Rankine Cycle

The condensing steam cycle of a supercritical pressure 600 MW generating unit.

The condensing steam cycle has

*  three turbines with four-exhaust steams

*  one sealing, four low pressure , one open feedwater heater/de-aerator, and three high pressure closed feedwater heaters.

### The Schematic of Example Cycle

![N600](.//img/N600.jpg)

### The File of example cycle's Flowsheet and Data

The Json file is used to representate the example cycle's flowsheet and data

* [The Json file of the example cycle's flowsheet and data](./SimRankine/rankinejson/N600_1.json)

## Run

* simulation based on 1kg mass:
 
```bash
 python rankinesim.py
```

* simulation on specified power/mass

```bash
 python rankinesim_spec.py
```

## Cite as

Cheng Maohua. (2021, March 29). PySEE/PyRankine: The Open Source General Rankine Cycle Simulator of Steady-State Mass and Energy Balance in Python (Version 2.0). Zenodo. http://doi.org/10.5281/zenodo.4644278

