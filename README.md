# PyRankine

`PyRankine` is  a demo simulator of ideal rankine cycle based on [libseuif97](https://github.com/PySEE/SEUIF97) for Windows/Linux(64).

## Dependencies：libseuif97

* IF97 high-speed shared library (Windows64, Linux64)
  * https://github.com/PySEE/SEUIF97

## Run

```bash
python rankine.py
```

## Example Rankine Cycle

* Michael J . Mora. Fundamentals of Engineering Thermodynamics(7th Edition). John Wiley & Sons, Inc. 2011

      Chapter 8 : Vapour Power Systems Example 8.1:Analyzing an Ideal Rankine Cycle  Page 438

   * Steam is the working fluid in an ideal Rankine cycle. 

   * Saturated vapor enters the turbine at 8.0 MPa 
   
   * Saturated liquid exits the condenser at a pressure of 0.008 MPa. 

   * The net power output of the cycle is 100 MW.

   * Cooling water enters the condenser at 15C and exits at 35C.

![rankine](./vps-fig81.png)

* Determine for the cycle

  * the thermal efficiency, %

  * the back work ratio,  %

  * the mass flow rate of the steam,in kg/h,

  * the rate of heat transfer, Qin, into the working fluid as it passes through the boiler, in MW,

  * the rate of heat transfer, Qout, from the condensing steam as it passes through the condenser, in MW,

  * the mass flow rate of the condenser cooling water, in kg/h

## Reference

*	ASCEND4: The ASCEND Modelling and Simulation Environment  http://ascend4.org/ 

* OpenMDAO: An open-source MDAO framework written in Python  http://openmdao.org/

* OpenModelica: An open-source Modelica-based modeling and simulation environment https://openmodelica.org/

* Jeffrey Kantor: Introduction to Chemical Engineering Analysis https://github.com/jckantor/CBE20255




