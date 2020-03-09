## The Object-oriented programming and JSON Textual Representation of Rankine Cycle Flowsheet

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

```
        <sim=oop>
          │ 
          |── rankine.py  #  main app
          |
          |── <components> components package
          │    |
          │    │ ── node.py
          │    |
          │    │ ── boiler.py
          │         .... 
          │
          |── <rankinecycle> cycle package
          │    |
          │    │ ─  iocycle.py # read json to the object; output the class to json  
          │    │     
          │    │ ─  objcycle.py # the objects of rankine object
          │    │
          │    │ ─  simcycle.py  # ana;ysis the rankine cycle
          │
          |── <data> json files
                 |
                 │──<txtcyxle> The Textual Representation Files of Rankine Cycle
                 │     │
                 │     │ ──rankine??.json 
                 │  
                 │──<output> The Output Files of Rankine Cycle
                       │
                       │ ── rankine??-sm.txt # the Specified Mass Flow
                       │
                       │ ── rankine??-sp.txt`: the Specified Net Output Power
```

## The UML Class diagram 

### The Class Diagram： Association

![Package UML](./uml/packages.svg)

### The Class Diagram : Composition

All component classes have: 
* class variables:  `energy`, `type`
* methods:`__init__`,`state`, `balance`, `sm_energy`,`__str__`, `__iter__`

  ![Class UML](./uml/classes.svg)

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
  def ComponentBalance(self):
        keys = list(self.comps.keys())
        deviceok = False
        
        i = 0  # i: the count of deviceok to avoid endless loop
        while (deviceok == False and i <= self.DevNum):
            
            for curdev in keys:
                try:
                    self.comps[curdev].balance()
                    keys.remove(curdev)
                except:
                    pass
            
            i += 1
            if (len(keys) == 0):
                deviceok = True
        
        # for debug: check the failed devices
        if (len(keys) >0): 
            print(keys)  
```
