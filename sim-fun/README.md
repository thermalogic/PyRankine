#  The Simulator 1: General Abstraction and CSV Textual Model of Rankine Cycle 

* List,Dict and Function

**Run**

```bash
>python rankine.py
```

## Example Rankine Cycles

Michael J. Moran, Howard N. Shapiro, Daisie D. Boettner, Margaret B. Bailey. Fundamentals of Engineering Thermodynamics(7th Edition). John Wiley & Sons, Inc. 2011

Chapter 8 : Vapour Power Systems 

* [EXAMPLE 8.1: Analyzing an Ideal Rankine Cycle, P438](http://nbviewer.jupyter.org/github/PySEE/PyRankine/blob/master/notebook/RankineCycle81-82.ipynb)

* [EXAMPLE 8.2: Analyzing a Rankine Cycle with Irreversibilities, P444](http://nbviewer.jupyter.org/github/PySEE/PyRankine/blob/master/notebook/RankineCycle81-82.ipynb)    

* [EXAMPLE 8.5: The Regenerative Cycle with Open Feedwater Heater, P456](http://nbviewer.jupyter.org/github/PySEE/PyRankine/blob/master/notebook/RankineCycle85.ipynb)

## The Projects 

##  Data Files in path `./data` 

[The Textual Representation Files of Rankine Cycle](./data)

* Devices: `rankine??-des.csv`

* Nodes:   `rankine??-nds.csv`

[The Output Files of Rankine Cycle](./data) 

* `rankine??-sp.txt`: the output of the Specified Net Output Power

### The RankineCycle Package in path `./RankineCycle` 

[Modules in the package](./RankineCycle)

* `__init__`

* createitems

* device

* node

* cycle

* output

## The Methods to check and analysis the mass flow rate

There are dependencies in the mass float rate calculation.

e.g: [EXAMPLE 8.5: The Regenerative Cycle with Open Feedwater Heater, P456](http://nbviewer.jupyter.org/github/PySEE/PyRankine/blob/master/notebook/RankineCycle85.ipynb)

If the Open Feedwater Heater is not calculated, the fraction of extraction steam flow from turbine is not obtained, then the
fraction of the total flow passing through the second-stage turbine is also no value, The turbine work calculation cannot be carried out.

That is to say that the Open Feedwater Heater must be calculated **before** the Turbine.

There is a problem of **equipment calculation order** in the mass float rate of Rankine Cycle

What is the solution? **Hard-coded** Calculation Order? No, It is not the general solution.

In the example codes, we provide one simple general solution:

```python
 def CalDevices(Devices, Nodes):
    # 1 Task: States
    for dev in Devices.keys():
        Devices[dev]["fun"](Devices[dev], Nodes, "State")

    # 2 In Order！
    keys = list(Devices.keys())
    devCounts = len(keys)
    i = 0
    fdotok = False
    while (fdotok == False):
        for curdev in keys:
            try:
                Devices[curdev]["fun"](Devices[curdev], Nodes, "Balance")
                keys.remove(curdev)
            except:
                pass
        i += 1
        if (i > devCounts+1 or len(keys) == 0):
            fdotok = True
```

