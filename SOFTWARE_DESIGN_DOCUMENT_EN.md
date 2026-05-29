# PyRankine Software Design Document

## 1. Project Overview

PyRankine is a hybrid steady-state simulator for Rankine Cycle systems based on Python, supporting two simulation methods: Sequential-Modular (SM) and Equation-Oriented (EO). This project is designed for modeling and simulation of thermal systems in thermal power plants, especially for off-design analysis of supercritical pressure power generation units.

### 1.1 Project Features
- Hybrid simulation architecture: Provides both Sequential-Modular and Equation-Oriented solving schemes
- Based on IAPWS-IF97 (Industrial Formulation 1997) for water and steam properties
- Supports multiple types of thermal equipment (Boiler, Turbine, Feedwater Pump, Regenerative Heater, Condenser, etc.)
- JSON configuration file-driven workflow definition
- Supports variable-condition simulation with specified power or specified mass flow rate
- Complete performance indicator calculations (cycle efficiency, heat rate, steam rate, etc.)

---

## 2. Technology Stack

| Technology Component | Version/Description |
|---------------------|-------------------|
| Programming Language | Python 3.x |
| Thermophysical Properties Library | seuif97 (based on IAPWS-IF97) |
| Numerical Computing | NumPy |
| Data Format | JSON |
| Runtime Environment | Windows/Linux/macOS |

---

## 3. System Architecture Design

### 3.1 Overall Layered Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    User Interface Layer                        │
│  rankinesim.py / rankinesim_spec.py / SimRankineCycle        │
├─────────────────────────────────────────────────────────────────┤
│                    Cycle Core Layer                           │
│            RankineCycle (rankineobj.py)                      │
├─────────────────────────────────────────────────────────────────┤
│                    Thermal Component Layer                     │
│  Boiler / Pump / TurbineExs / Condenser / Various Heaters     │
├─────────────────────────────────────────────────────────────────┤
│                    Port Node Layer                             │
│              Port (port.py) - Working Fluid State Node        │
├─────────────────────────────────────────────────────────────────┤
│                    Utility Layer                               │
│    utils.py - JSON Parsing / Result Output / Redirected Output │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Core Design Philosophy

1. **Object-Oriented Abstraction**: All thermal equipment is abstracted as component objects with ports
2. **Dual-Paradigm Architecture**: The same component implementation supports both SM and EO simulation modes simultaneously
3. **Node Sharing Mechanism**: Automatically build node networks through connectors that share ports between devices
4. **Universal Property Interface**: The Port class encapsulates all IAPWS-IF97 state calculation methods

---

## 4. Module Detailed Design

### 4.1 Port Module (port.py)

**File Path**: `SimRankine/components/port.py`

#### 4.1.1 Responsibilities
- Encapsulates complete state properties of the working fluid (water and steam)
- Provides multiple state equation solving methods based on IAPWS-IF97
- Implements mass flow scaling calculations
- Unified formatted output interface

#### 4.1.2 Data Structure

```python
class Port:
    id: int                 # Node ID
    desc: str               # Node description (connection relationship)
    p: float                # Pressure (MPa)
    t: float                # Temperature (°C)
    x: float                # Quality (dryness fraction)
    h: float                # Specific enthalpy (kJ/kg)
    s: float                # Specific entropy (kJ/kg·K)
    v: float                # Specific volume (m³/kg)
    fdot: float             # Relative mass flow rate (based on 1kg total working fluid)
    mdot: float             # Absolute mass flow rate (kg/h)
```

#### 4.1.3 Key Methods

| Method | Function |
|--------|----------|
| `pt()` | Calculate h, s, v, x from (p, t) |
| `ph()` | Calculate t, s, v, x from (p, h) |
| `ps()` | Calculate t, h, v, x from (p, s) |
| `hs()` | Calculate t, p, v, x from (h, s) |
| `px()` | Calculate t, h, s, v from (p, x) |
| `tx()` | Calculate p, h, s, v from (t, x) |
| `th()` | Calculate p, x, s, v from (t, h) |
| `hx()` | Calculate t, p, v, s from (h, x) |
| `calmdot(totalmass)` | Convert fdot to mdot |

---

### 4.2 Components Module

All component classes follow a unified interface specification, supporting 6 core methods:

| Method Signature | Function Description |
|-----------------|---------------------|
| `state()` | Equipment state calculation (solve unknown states from known port parameters) |
| `balance()` | Mass and energy balance (Sequential-Modular SM) |
| `equation_rows()` | Generate linear equation row data for Equation-Oriented EO method |
| `energy_fdot()` | Calculate energy terms based on solved fdot |
| `calmdot(totalmass)` | Convert relative flow fdot to absolute flow mdot |
| `sm_energy()` | Calculate actual power/thermal power based on mdot |

#### 4.2.1 Boiler (boiler.py)
- Energy type: `energy = "heatAdded"`
- Function: Heat feedwater into superheated steam
- Mass conservation: `iPort.fdot = oPort.fdot`
- Heat load: `heatAdded = fdot * (oPort.h - iPort.h)`

#### 4.2.2 Feedwater Pump (pump.py)
- Energy type: `energy = "workRequired"`
- Function: Increase condensate pressure
- Isentropic efficiency formula: `h_out = h_in + (h_isentropic - h_in)/eta`

#### 4.2.3 Turbine (turbineexs.py)
- Energy type: `energy = "workExtracted"`
- Function: Steam expansion work, supporting 0-3 extraction stages
- Isentropic expansion efficiency calculation
- Output interface: iPort → ePort0/1/2/3 → oPort

#### 4.2.4 Condenser (condenser.py)
- Energy type: `energy = "heatExtracted"`
- Function: Condense exhaust steam into saturated water
- Supports multiple exhaust steam inlets

#### 4.2.5 Regenerative Heater Series
| Component | Type | Description | File |
|-----------|------|-------------|------|
| OpenedHeaterDw0 | Open-type heater (no drain inlet) | Open-type deaerator | openedheaterdw0.py |
| OpenedHeaterDw1 | Open-type heater (with drain inlet) | Open-type with drain | openedheaterdw1.py |
| ClosedHeaterDw0 | Closed-type heater (no drain outlet) | Closed-type no drain | closedheaterdw0.py |
| ClosedHeaterDw1 | Closed-type heater (with drain outlet) | Closed-type with drain | closedheaterdw1.py |
| CombinedHeater | Combined heater (with SG/CWP/WELL) | Integrated regenerative component | combinedheater.py |

#### 4.2.6 Pipe Components
- `pipeilevel.py` - Only keeps inlet and outlet parameters unchanged
- `pipemloss.py` - Only mass loss
- `pipeploss.py` - Only pressure loss
- `pipeptloss.py` - Pressure and temperature loss

---

### 4.3 Cycle Core Module (rankineobj.py / RankineCycle)

**File Path**: `SimRankine/rankine/rankineobj.py`

#### 4.3.1 Responsibilities
- Instantiate all thermal component objects from JSON dictionary
- Parse connector configuration, build shared node network
- Implement both simulation solving algorithms (SM and EO)
- Calculate overall cycle performance metrics

#### 4.3.2 Core Data Structure

```python
class RankineCycle:
    name: str                    # Cycle name
    etam: float                  # Mechanical efficiency
    etag: float                  # Generator efficiency
    comps: dict                  # Component dictionary {device name: component object}
    nodes: list[Port]            # Shared port node list
    # 1kg baseline performance metrics
    totalworkExtracted: float    # Total work output (kJ/kg)
    totalworkRequired: float     # Total work input (kJ/kg)
    totalheatAdded: float        # Total heat addition (kJ/kg)
    efficiency_cycle: float      # Cycle efficiency
    # Specified condition performance metrics
    Specified: bool              # Whether it is a specified condition
    mdot: float                  # Total mass flow rate (kg/h)
    Wcycledot: float             # Cycle output power (MW)
```

#### 4.3.3 Node Building Mechanism - `__add_node()`

**Key Algorithm**:
1. Assign a global node ID to each connector pair
2. Create shared Port object
3. Point both devices' port references to the same shared node object
4. Attribute merging: If one port has a value, automatically assign it to the shared node

> This design cleverly implements implicit connection of the heat flow network. Any device port modifying a shared node property is perceived by all devices connected to that node.

#### 4.3.4 Sequential-Modular Method Solver - `__component_analysis_sm()`

**Algorithm Flow**:
1. Device list enqueued, iteratively try to call `state()` or `balance()` one by one
2. Successfully executed devices are removed from the queue
3. Maximum DevNum iterations (to avoid infinite loops)
4. Solution is successful when all devices are completed

#### 4.3.5 Equation-Oriented Method Solver - `__equation_eo()`

**Core Implementation**:
```python
A = np.zeros((connum, connum))   # Coefficient matrix
b = np.zeros(connum)              # Right-hand side vector
# Collect equation rows from all components
for key in self.comps:
    self.comps[key].equation_rows()
    for row in self.comps[key].rows:
        for col in row["a"]:
            A[currow, col[0]] = col[1]
        b[currow] = row["b"]
# Solve linear system Ax = b
fdot = np.linalg.solve(A, b)
```

---

### 4.4 Simulation Scheduling Module (simrankine.py / SimRankineCycle)

**File Path**: `SimRankine/rankine/simrankine.py`

Provides high-level API encapsulation to simplify the calling process:
```python
simulator_eo()              # EO method simulation
simulator_sm()              # SM method simulation
simulator_performance()     # Performance calculation
specified_simulator(power, mass)  # Specified power/mass simulation
```

---

### 4.5 Utilities Module (utils.py)

**File Path**: `SimRankine/rankine/utils.py`

#### 4.5.1 `create_dictcycle_from_jsonfile(filename)`
- Read JSON configuration file
- Convert dictionary-style connector pairs to Python tuple format
- Return complete cycle configuration dictionary

#### 4.5.2 `OutFiles(cycle, outfilename=None)`
- Redirect standard output to specified file
- Output content: Cycle Performance → All Devices → All Connector Nodes
- UTF-8 encoding ensures Chinese character compatibility

---

## 5. Key Data Flow Design

### 5.1 Standard 1kg Baseline Simulation Flow

```
  JSON Configuration File
      ↓
create_dictcycle_from_jsonfile()
      ↓
RankineCycle.__init__()
  ├─ Instantiate all component objects
  └─ __add_node() Build shared node network
      ↓
  simulator_eo()
  ├─ component_analysis_sm("STATE")  # State initialization
  ├─ __equation_eo()                # Linear system solve for fdot
  └─ energy_fdot() Traverse components to calculate energy terms
      ↓
  simulator_performance()
  └─ Aggregate all component energy → Calculate efficiency, heat rate, etc.
      ↓
    OutFiles() Output results
```

### 5.2 Specified Power Off-Design Simulation Flow

```
  1kg baseline simulation (already completed)
      ↓
specified_simulator(set_power=600MW)
  ├─ Calculate SteamRate_power_generation
  ├─ Back-calculate total mass flow mdot from target power
  ├─ Traverse all nodes calling calmdot(mdot)
  ├─ Traverse all components calling calmdot(mdot)
  └─ sm_energy() Calculate MW-level actual power
      ↓
  Output full results with MW/kg/h units
```

### 5.3 Energy Metrics Aggregation Logic

Components are aggregated by `energy` attribute classification:

| Category | Aggregation Variable |
|----------|---------------------|
| workExtracted | Turbine total output work |
| workRequired | Pump total consumed work |
| heatAdded | Boiler total heat addition |

Performance metrics calculation formulas:
```
efficiency_cycle = totalworkExtracted / totalheatAdded
efficiency_power_generation = efficiency_cycle * etam * etag
HeatRate = 3600 / efficiency_power_generation    (kJ/kWh)
SteamRate = HeatRate / totalheatAdded           (kg/kWh)
netpoweroutput = totalworkExtracted * etam * etag - totalworkRequired
```

---

## 6. JSON Configuration File Format Specification

**Reference File**: `SimRankine/jsonmodel/N600.json`

```json
{
  "name": "N600",
  "etam": 0.995,
  "etag": 0.985,
  "components": [
    {
      "name": "BO",
      "devtype": "BOILER",
      "iPort": {"p": 30.0},
      "oPort": {"p": 30.0, "t": 600.0}
    }
  ],
  "connectors": [
    {"BO.iPort": "FWP.oPort"},
    {"BO.oPort": "TU.iPort"}
  ]
}
```

Field descriptions:
- `name` - Cycle identifier name
- `etam` - Mechanical efficiency (0~1)
- `etag` - Generator efficiency (0~1)
- `components` - Component array, each component must specify `devtype` for type mapping
- `connectors` - Connection relationship array, each item defines the connection of two device ports

---

## 7. Component Type Registry

**File Path**: `SimRankine/components/__init__.py` `compdict` dictionary

| devtype Value | Component Class Name |
|---------------|----------------------|
| BOILER | Boiler |
| PUMP | Pump |
| TURBINEEXS | TurbineExs |
| CONDENSER | Condenser |
| FWH-OPEN-DW0 | OpenedHeaterDw0 |
| FWH-OPEN-DW1 | OpenedHeaterDw1 |
| FWH-CLOSE-DW0 | ClosedHeaterDw0 |
| FWH-CLOSE-DW1 | ClosedHeaterDw1 |
| FWH-CLOSE-DW1-SG-CWP-WELL | CombinedHeater |
| PIPE-ILEVEL | PipeILevel |
| PIPE-MLOSS | PipeMLoss |
| PIPE-PLOSS | PipePLoss |
| PIPE-PTLOSS | PipePTLoss |
| SPLIT-ONE2TWO | SplitOne2Two |
| REHEATER | Reheater |

---

## 8. Key Technical Innovations

### 8.1 Dual-Paradigm Unified Architecture
The same component code simultaneously supports two simulation modes, SM (Sequential-Modular) and EO (Equation-Oriented), without modification, balancing engineering usability and numerical robustness.

### 8.2 Implicit Node Sharing Mechanism
Through Python object reference assignment, automatic sharing of port nodes is realized, avoiding complex graph theory algorithms, and building large-scale heat flow networks with extremely concise code.

### 8.3 Automatic Linear Equation System Assembly
Each component contributes local mass balance equations, the main loop automatically assembles the global coefficient matrix `A`, and finally calls numpy.linalg.solve() to solve all unknown relative flows fdot in one pass.

---

## 9. Directory Structure

```
PyRankine/
├── SimRankine/
│   ├── components/          # Thermal Component Library
│   ├── rankine/             # Cycle Core and Simulation Engine
│   │   ├── __init__.py
│   │   ├── rankineobj.py    # RankineCycle Main Class
│   │   ├── simrankine.py    # High-level Simulation Scheduling API
│   │   └── utils.py         # Utility Functions
│   ├── jsonmodel/
│   │   └── N600.json        # 600MW Example Cycle Configuration
│   ├── result/              # Output Results Directory
│   ├── rankinesim.py        # 1kg Baseline Simulation Entry
│   └── rankinesim_spec.py   # Specified Power/Mass Simulation Entry
├── img/
│   └── N600.jpg             # System Flow Diagram
├── uml/                     # UML Class Diagrams
└── README.md
```

---

## 10. Running Examples

### 10.1 Basic 1kg Simulation
```bash
cd SimRankine
python rankinesim.py
```

### 10.2 Specified Power Simulation
```bash
python rankinesim_spec.py
```

### 10.3 Code Snippet Call
```python
from rankine.utils import create_dictcycle_from_jsonfile
from rankine.simrankine import SimRankineCycle

dictcycle = create_dictcycle_from_jsonfile('N600.json')
cycle = SimRankineCycle(dictcycle)
cycle.simulator_eo()
cycle.simulator_performance()
cycle.specified_simulator(set_power=600)
```

---

**Document Version**: V2.0.0  
**Last Updated**: 2026-05-12  
**Author**: Cheng Maohua
