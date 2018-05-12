# PyRankine 

## Step4: The General Simulator of Rankine Cycle

    step4-csv: csv file

    step4-json: json file

    step4-json-dict: json file and  __init__ device with dict

### Examples of Rankine Cycle
 
Michael J . Mora. Fundamentals of Engineering Thermodynamics(7th Edition). John Wiley & Sons, Inc. 2011

Chapter 8 : Vapour Power Systems Example

* EXAMPLE 8.1 ：An Ideal Regenerative Cycle, Page 438

* EXAMPLE 8.5 ：A Regenerative Cycle with Open Feedwater Heater,Page 456

## Run

```bash
>cd step4-csv/step4-json/step4-json-dict
>python rankine.py
```

## Notes on Python

### 1 Packages
   
   https://docs.python.org/3.6/tutorial/modules.html#packages

   Packages are a way of structuring Python’s module namespace by using **“dotted module names”**.
   The ` __init__.py  `files are required to make Python treat the **directories** as containing **packages**; 
   this is done to **prevent directories with a common name**, such as string, from unintentionally hiding valid modules that occur later on the module search path. 
   
   In the simplest case, ` __init__.py ` can just be an **empty** file, but it can also execute initialization code for the package or set the ` __all__ ` variable

```bash   
   components/                  components package
      __init__.py               Initialize the components package
      boiler.py
      condenser.py
     ...
```

Users of the package can import **individual modules** from the package, for example:

```python
import components.node
```
An alternative way of importing the submodule is:

```python
from components import node
```
Yet another variation is to import **the desired function or variable** directly:

```python
from components.node import Node
```

### 2 Redirect **stdout** to a file

29.1. sys — System-specific parameters and functions

https://docs.python.org/3.6/library/sys.html

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

### 3 r'' raw string literals 

r'' raw string literals produce a string just like a normal string literal does

```python
nds_filesname_str=r'./cyclefile/rankine85-nds.csv'
```

### 4 glob — Unix style pathname pattern expansion

https://docs.python.org/3.6/library/glob.html

The `glob` module finds all the pathnames matching a specified pattern according to the rules used by the Unix shell, although results are returned in arbitrary order. No tilde(~) expansion is done, but `*`, `?`, and character `ranges` expressed with `[]` will be correctly matched

```python
nds_filesname_str=r'./cyclefile/rankine8?-nds.csv
nds_filesname=glob.glob(nds_filesname_str)
```

```python
json_filesname_str=r'./cyclefile/rankine8[0-9].json'
json_filesname=glob.glob(json_filesname_str)
```

## EXAMPLE 8.1 :An Ideal Rankine Cycle  

Steam is the working fluid in an ideal Rankine cycle. 

   * Saturated vapor enters the turbine at 8.0 MPa 
   
   * Saturated liquid exits the condenser at a pressure of 0.008 MPa. 

   * The net power output of the cycle is 100 MW.

   * Cooling water enters the condenser at 15°C and exits at 35°C.

![rankine](./img/rankine81.jpg)

Determine for the cycle

  * the thermal efficiency, %

  * the back work ratio,  %

  * the mass flow rate of the steam,in kg/h,

  * the rate of heat transfer, Qin, into the working fluid as it passes through the boiler, in MW,

  * the rate of heat transfer, Qout, from the condensing steam as it passes through the condenser, in MW,

  * the mass flow rate of the condenser cooling water, in kg/h

## EXAMPLE 8.5 ：A Regenerative Cycle with Open Feedwater Heater

Consider a regenerative vapor power cycle with one open feedwater heater.

* Steam enters the turbine at 8.0 MPa, 480°C and expands to 0.7 MPa, 

* Some of the steam is extracted and diverted to the open feedwater heater operating at 0.7 MPa. 

* The remaining steam expands through the second-stage turbine to the condenser pressure of 0.008 MPa

* Saturated liquid exits the open feedwater heater at 0.7 MPa. 

* The isentropic efficiency of each turbine  stage is 85% and each pump operates isentropically. 

If the net power output of the cycle is 100 MW, determine

* (a) the thermal efficiency  %

* (b) the mass flow rate of steam entering the first turbine stage, in kg/h.

If the mass flow rate of steam entering the first-stage turbine were 150 kg/s 

* (a) what would be the net power, in MW

* (b) the fraction of steam extracted, y? 

![rankine85](./img/rankine85.jpg)

Engineering Model:

1. Each component in the cycle is analyzed as a steady-state control volume. The control volumes are shown in the accompanying sketch by dashed lines.


2. All processes of the working fluid are internally reversible, except for the expansions through the two turbine stages and mixing in the open feedwater heater.


3. The turbines, pumps, and feedwater heater operate adiabatically.


4. Kinetic and potential energy effects are negligible.


5. Saturated liquid exits the open feedwater heater, and saturated liquid exits the condenser.