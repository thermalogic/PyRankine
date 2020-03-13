# PyRankine

[![DOI](https://zenodo.org/badge/85393590.svg)](https://zenodo.org/badge/latestdoi/85393590)

The PyRankine is the general Rankine Cycle simulator provided in the different data structures 

We wish that PyRankine may be a helpful vehicle for you to understand **Computational Thinking** and improve programming skills.

### [The Simulator : List,Dict and Function](./sim-fun)

* CSV Textual Model of the Rankine Cycle Flowsheet 
     
### [The Simulator : Object-oriented programming](./sim-oop)

* JSON Textual Model of Rankine Cycles Flowsheet 
     
   **The UML Class Diagram: Association**

   ![The UML Class Diagram: Association](./sim-oop/uml/packages.svg)  
 
## Dependencies：SEUIF97

IAPWS-IF97 high-speed shared library

* https://github.com/PySEE/SEUIF97

Install with pip
```bash
python -m pip install seuif97
```

## The Example Rankine Cycles

The Rankine Cycles used in these general simulators are Example 8.1, 8.2 and 8,5 of **Michael J. Moran. Fundamentals of Engineering Thermodynamics(7th Edition)**. John Wiley & Sons, Inc. 2011

Chapter 8 : Vapour Power Systems 

### The Jupyter Notebooks of Example Rankine Cycles

* [EXAMPLE 8.1: The Ideal Rankine Cycle, P438](http://nbviewer.jupyter.org/github/PySEE/PyRankine/blob/master/notebook/RankineCycle81-82.ipynb)

* [EXAMPLE 8.2: Analyzing a Rankine Cycle with Irreversibilities,  P444](http://nbviewer.jupyter.org/github/PySEE/PyRankine/blob/master/notebook/RankineCycle81-82.ipynb)
  
* [EXAMPLE 8.3: Evaluating Performance of an Ideal Reheat Cycle, P449-451](http://nbviewer.jupyter.org/github/PySEE/PyRankine/blob/master/notebook/RankineCycle83-84.ipynb)

* [EXAMPLE 8.4: Evaluating Performance of a Reheat Cycle with Turbine Irreversibility, P451](http://nbviewer.jupyter.org/github/PySEE/PyRankine/blob/master/notebook/RankineCycle83-84.ipynb)

* [EXAMPLE 8.5: The Regenerative Cycle with Open Feedwater Heater, P456](http://nbviewer.jupyter.org/github/PySEE/PyRankine/blob/master/notebook/RankineCycle85.ipynb)

* [EXAMPLE 8.6: The Reheat–Regenerative Cycle with Two Feedwater Heaters, P460-463](http://nbviewer.jupyter.org/github/PySEE/PyRankine/blob/master/notebook/RankineCycle86.ipynb)

**Start the notebooks**

```bash
>start.bat
```

**Schematic of Example Rankine Cycles**

![rankines](./notebook/img/rankines.jpg)


## Cite as

Cheng Maohua. (2020, March 13). PySEE/PyRankine: First Release of PyRankine (Version V1.0.0). Zenodo. http://doi.org/10.5281/zenodo.3709393

## Reference

* Computational thinking

  * [wikipedia: Computational thinking]( https://en.wikipedia.org/wiki/Computational_thinking)

  * Jeannette M. Wing. [Computational Thinking Benefits Society]( http://socialissues.cs.toronto.edu/index.html%3Fp=279.html)

* Modeling and Simulation of Engineering Systems

  * R Sinha, Christiaan J. J. Paredis. etc. **Modeling and Simulation Methods for Design of Engineering Systems**. Transactions of the ASME[J]. 2001.03(1):84-91

  * Modelica
  
    * OpenModelica: [An open-source Modelica-based modeling and simulation environment](https://openmodelica.org/)

      * https://github.com/OpenModelica

    * Michael M.Tiller：[Introduction to Physical Modeling with Modelica](https://github.com/mtiller/FirstBookExamples)
    
      *  刘俊堂等译. Modelica多领域物理系统建模入门与提高, 航空工业出版社(第1版),2017.05

    * Michael M.Tiller：[Learn Modelica by Example](http://book.xogeny.com/)
      
  * MATLAB：Simscape https://cn.mathworks.com/products/simscape.html  

* ThermoCycle Simulator 

    * Maarten Winter: pyDNA https://github.com/mwoc/pydna

    * ORC Modeling Kit: https://github.com/orcmkit/ORCmKit

    * ACHP: https://github.com/TSTK/ACHP 

    * Rankine Cycle(Steam Turbine) http://cn.mathworks.com/help/physmod/simscape/examples/rankine-cycle-steam-turbine.html

*  Electronic circuit simulator 

   * Jan M. Rabaey: SPICE http://bwrcs.eecs.berkeley.edu/Classes/IcBook/SPICE/

      * SPICE: https://en.wikipedia.org/wiki/SPICE

   * ahkab：a SPICE-like electronic circuit simulator written in Python https://github.com/ahkab/ahkab

   * 杨华中等. 电子电路的计算机辅助分析和设计方法（第二版），清华大学出版社，北京，2008.02

