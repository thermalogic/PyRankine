# PyRankine

Step by step codes of the ideal rankine cycle simulator to demonstrate: 

  * **Data Structures + Algorithms = Programs** 
  * **Computational Thinking** 

     * step 0 :    Zero @  Data Structures,Program architecture, Algorithms
     * step 1 :   Basic @  Data Structures,Program architecture, Algorithms
     * step 2 : Forward @  Data Structures,Program architecture, Algorithms

You do not need to do programming step0，1，2. 
 
**You need to**
 
*  reading the codes
*  understanding computational thinking and programming skills
*  programing one solution to the  rankine cycle 

## Dependencies：libseuif97

* IF97 high-speed shared library (Windows/Linux)
  * https://github.com/PySEE/SEUIF97

## Step by step Codes

* Jupyter Notebook

  * Step0 http://nbviewer.jupyter.org/github/PySEE/PyRankine/blob/master/notebook/IdealRankineCycle-Step0.ipynb

  * Step1 http://nbviewer.jupyter.org/github/PySEE/PyRankine/blob/master/notebook/IdealRankineCycle-Step1.ipynb

```bash
StartNB.bat
```
* Python

```bash
cd step0
python rankine.py
``` 

```bash
cd step1
python rankine.py
``` 

```bash
cd step2
python rankine.py
```

## Example Rankine Cycle

* Michael J . Mora. Fundamentals of Engineering Thermodynamics(7th Edition). John Wiley & Sons, Inc. 2011

      Chapter 8 : Vapour Power Systems Example 8.1:Analyzing an Ideal Rankine Cycle  Page 438

   * Steam is the working fluid in an ideal Rankine cycle. 

   * Saturated vapor enters the turbine at 8.0 MPa 
   
   * Saturated liquid exits the condenser at a pressure of 0.008 MPa. 

   * The net power output of the cycle is 100 MW.

   * Cooling water enters the condenser at 15°C and exits at 35°C.

![rankine](./notebook/vps-fig81.png)

* Determine for the cycle

  * the thermal efficiency, %

  * the back work ratio,  %

  * the mass flow rate of the steam,in kg/h,

  * the rate of heat transfer, Qin, into the working fluid as it passes through the boiler, in MW,

  * the rate of heat transfer, Qout, from the condensing steam as it passes through the condenser, in MW,

  * the mass flow rate of the condenser cooling water, in kg/h

## Reference

* Algorithms + Data Structures = Programs: https://en.wikipedia.org/wiki/Algorithms_%2B_Data_Structures_%3D_Programs

* Computational thinking: https://en.wikipedia.org/wiki/Computational_thinking

* R Sinha, Christiaan J. J. Paredis. etc. Modeling and Simulation Methods for Design of Engineering Systems. Transactions of the ASME[J]. 2001.03(1):84-91

* Process simulation：https://en.wikipedia.org/wiki/Process_simulation

* ASCEND4: The ASCEND Modelling and Simulation Environment  http://ascend4.org/ 

* OpenMDAO: An open-source MDAO framework written in Python  http://openmdao.org/

* OpenModelica: An open-source Modelica-based modeling and simulation environment https://openmodelica.org/

* Jeffrey Kantor: Introduction to Chemical Engineering Analysis https://github.com/jckantor/CBE20255

* Maarten Winter: pyDNA https://github.com/mwoc/pydna

* Jan M. Rabaey: SPICE http://bwrcs.eecs.berkeley.edu/Classes/IcBook/SPICE/

* SPICE: https://en.wikipedia.org/wiki/SPICE

* ahkab：a SPICE-like electronic circuit simulator written in Python https://github.com/ahkab/ahkab


