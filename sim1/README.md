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
        if (i > devCounts+1 or keys.count == 0):
            fdotok = True
```

## Notes on Python

### 1 Packages
   
   https://docs.python.org/3/tutorial/modules.html#packages

   Packages are a way of structuring Python’s module namespace by using **“dotted module names”**.
   The ` __init__.py  `files are required to make Python treat the **directories** as containing **packages**; 
   this is done to **prevent directories with a common name**, such as string, from unintentionally hiding valid modules that occur later on the module search path. 
   
   In the simplest case, ` __init__.py ` can just be an **empty** file, but it can also execute initialization code for the package or set the ` __all__ ` variable

```bash   
   RankineCycle/                RankineCycle package
      __init__.py               Initialize the  package
      createitem.py
      cycle.py
     ...
```

Users of the package can import **individual modules** from the package, for example:

```python
from RankineCycle.createitems import CreateNodeFromCSV,CreateDeviceFromCSV
from RankineCycle.cycle import  RankineCycle
from RankineCycle.output import OutFiles
```

### 2 Redirect **stdout** to a file

29.1. sys — System-specific parameters and functions

https://docs.python.org/3/library/sys.html

This module provides access to some variables used or maintained by the **interpreter** and to functions that interact strongly with the interpreter. It is always available.

File objects used by the interpreter for standard input, output and errors:

* sys.stdin ： is used for all interactive input (including calls to input());

* sys.stdout ：is used for the output of print() and expression statements and for the prompts of input();

* sys.stderr：The interpreter’s own prompts and its error messages go to stderr.

These streams are regular **text** files like those returned by the open() function. 

```python
import sys
sys.stdout = open('Redirect2file.txt', 'w')
print('Test: redirect sys.stdout to file')
```

### 3 glob — Unix style pathname pattern expansion

https://docs.python.org/3/library/glob.html

The `glob` module finds all the pathnames matching a specified pattern according to the rules used by the Unix shell, although results are returned in arbitrary order. No tilde(~) expansion is done, but `*`, `?`, and character `ranges` expressed with `[]` will be correctly matched

```python
import glob

json_filesname_str='./txtcycle/rankine8[0-9].json'
json_filesname=glob.glob(json_filesname_str)
```

