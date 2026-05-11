# PyRankine 软件设计文档

## 1. 项目概述

PyRankine 是一个基于 Python 的混合式朗肯循环稳态仿真器，支持两种仿真方法：顺序模块法（Sequential-Modular, SM）和面向方程法（Equation-Oriented, EO）。该项目用于火力发电厂热力系统的建模与仿真，特别针对超临界压力发电机组的工况分析。

### 1.1 项目特性
- 混合仿真架构：同时提供顺序模块法和面向方程法两种求解方案
- 基于 IAPWS-IF97 水和水蒸气性质标准
- 支持多种热力设备类型（锅炉、汽轮机、给水泵、回热加热器、凝汽器等）
- JSON 格式配置文件驱动的工作流定义
- 支持指定功率或指定质量流量的变工况仿真
- 完整的性能指标计算（循环效率、热耗率、汽耗率等）

---

## 2. 技术栈

| 技术组件 | 版本/说明 |
|---------|----------|
| 编程语言 | Python 3.x |
| 工质物性库 | seuif97 (基于 IAPWS-IF97) |
| 数值计算 | NumPy |
| 数据格式 | JSON |
| 运行环境 | Windows/Linux/macOS |

---

## 3. 系统架构设计

### 3.1 总体分层架构

```
┌─────────────────────────────────────────────────────────────┐
│                    用户交互层 (User Interface)               │
│  rankinesim.py / rankinesim_spec.py / SimRankineCycle        │
├─────────────────────────────────────────────────────────────┤
│                    循环核心层 (Cycle Core)                   │
│            RankineCycle (rankineobj.py)                     │
├─────────────────────────────────────────────────────────────┤
│                    热力组件层 (Components)                    │
│  Boiler / Pump / TurbineExs / Condenser / 各种加热器等        │
├─────────────────────────────────────────────────────────────┤
│                    端口节点层 (Port Node)                     │
│              Port (port.py) - 工质状态节点                    │
├─────────────────────────────────────────────────────────────┤
│                    工具支持层 (Utilities)                    │
│    utils.py - JSON 解析 / 结果输出 / 重定向输出               │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 核心设计理念

1. **面向对象抽象**：将所有热力设备抽象为具有端口的组件对象
2. **双仿真范式**：同一套组件实现同时支持 SM 和 EO 两种仿真模式
3. **节点共享机制**：通过连接器实现设备间端口的共享，自动构建节点网络
4. **通用物性接口**：Port 类封装所有 IAPWS-IF97 的状态计算方法

---

## 4. 模块详细设计

### 4.1 端口模块 (port.py)

**文件路径**：`SimRankine/components/port.py`

#### 4.1.1 职责描述
- 封装工质（水和水蒸气）的完整状态属性
- 提供基于 IAPWS-IF97 的多种状态方程求解方法
- 实现质量流量缩放计算
- 统一格式化输出接口

#### 4.1.2 数据结构

```python
class Port:
    id: int                 # 节点编号
    desc: str               # 节点描述（连接关系）
    p: float                # 压力 (MPa)
    t: float                # 温度 (°C)
    x: float                # 干度
    h: float                # 比焓 (kJ/kg)
    s: float                # 比熵 (kJ/kg·K)
    v: float                # 比容 (m³/kg)
    fdot: float             # 相对质量流量（以 1kg 总工质为基准）
    mdot: float             # 绝对质量流量 (kg/h)
```

#### 4.1.3 关键方法

| 方法 | 功能 |
|-----|------|
| `pt()` | 通过 (p, t) 计算 h, s, v, x |
| `ph()` | 通过 (p, h) 计算 t, s, v, x |
| `ps()` | 通过 (p, s) 计算 t, h, v, x |
| `hs()` | 通过 (h, s) 计算 t, p, v, x |
| `px()` | 通过 (p, x) 计算 t, h, s, v |
| `tx()` | 通过 (t, x) 计算 p, h, s, v |
| `th()` | 通过 (t, h) 计算 p, x, s, v |
| `hx()` | 通过 (h, x) 计算 t, p, v, s |
| `calmdot(totalmass)` | 将 fdot 转换为 mdot |

---

### 4.2 组件模块 (Components)

所有组件类都遵循统一的接口规范，支持 6 个核心方法：

| 方法签名 | 功能描述 |
|---------|---------|
| `state()` | 设备状态计算（基于已知端口参数求解未知状态） |
| `balance()` | 质量和能量平衡（顺序模块法 SM） |
| `equation_rows()` | 生成面向方程法 EO 的线性方程组行数据 |
| `energy_fdot()` | 基于求解得到的 fdot 计算能量项 |
| `calmdot(totalmass)` | 将相对流量 fdot 转换为绝对流量 mdot |
| `sm_energy()` | 基于 mdot 计算实际功率/热功率 |

#### 4.2.1 锅炉 (boiler.py)
- 能量类型：`energy = "heatAdded"`
- 功能：给水加热为过热蒸汽
- 质量守恒：`iPort.fdot = oPort.fdot`
- 热负荷：`heatAdded = fdot * (oPort.h - iPort.h)`

#### 4.2.2 给水泵 (pump.py)
- 能量类型：`energy = "workRequired"`
- 功能：提高凝结水压力
- 等熵效率公式：`h_out = h_in + (h_isentropic - h_in)/eta`

#### 4.2.3 汽轮机 (turbineexs.py)
- 能量类型：`energy = "workExtracted"`
- 功能：蒸汽膨胀做功，支持 0-3 级抽汽
- 等熵膨胀效率计算
- 输出接口：iPort → ePort0/1/2/3 → oPort

#### 4.2.4 凝汽器 (condenser.py)
- 能量类型：`energy = "heatExtracted"`
- 功能：排汽冷凝为饱和水
- 支持多股排汽入口

#### 4.2.5 回热加热器系列
| 组件 | 类型 | 说明 | 文件 |
|-----|------|-----|------|
| OpenedHeaterDw0 | 混合式加热器（无疏水入口） | 开式除氧器类型 | openedheaterdw0.py |
| OpenedHeaterDw1 | 混合式加热器（带疏水入口） | 开式带疏水 | openedheaterdw1.py |
| ClosedHeaterDw0 | 表面式加热器（无疏水出口） | 闭式无疏水 | closedheaterdw0.py |
| ClosedHeaterDw1 | 表面式加热器（带疏水出口） | 闭式带疏水 | closedheaterdw1.py |
| CombinedHeater | 组合式加热器（含 SG/CWP/WELL） | 集成式回热组件 | combinedheater.py |

#### 4.2.6 管道类组件
- `pipeilevel.py` - 仅保持入口出口参数不变
- `pipemloss.py` - 仅有质量损失
- `pipeploss.py` - 仅有压力损失
- `pipeptloss.py` - 压力和温度损失

---

### 4.3 循环核心模块 (rankineobj.py / RankineCycle)

**文件路径**：`SimRankine/rankine/rankineobj.py`

#### 4.3.1 职责
- 从 JSON 字典实例化所有热力组件对象
- 解析连接器配置，构建共享节点网络
- 实现两种仿真求解算法（SM 和 EO）
- 计算循环整体性能指标

#### 4.3.2 核心数据结构

```python
class RankineCycle:
    name: str                    # 循环名称
    etam: float                  # 机械效率
    etag: float                  # 发电机效率
    comps: dict                  # 组件字典 {设备名: 组件对象}
    nodes: list[Port]            # 共享端口节点列表
    # 1kg 基准性能指标
    totalworkExtracted: float    # 总输出功 (kJ/kg)
    totalworkRequired: float     # 总输入功 (kJ/kg)
    totalheatAdded: float        # 总吸热量 (kJ/kg)
    efficiency_cycle: float      # 循环效率
    # 指定工况性能指标
    Specified: bool              # 是否为指定工况
    mdot: float                  # 总质量流量 (kg/h)
    Wcycledot: float             # 循环输出功率 (MW)
```

#### 4.3.3 节点构建机制 - `__add_node()`

**关键算法**：
1. 为每对连接器分配全局节点 ID
2. 创建共享 Port 对象
3. 将两个设备的端口引用指向同一节点对象
4. 属性合并：如果其中一个端口有值，自动赋值到共享节点

> 这一设计巧妙实现了热流网络的隐式连接，任意一个设备端口修改共享节点属性，所有连接该节点的设备都能感知。

#### 4.3.4 顺序模块法求解 - `__component_analysis_sm()`

**算法流程**：
1. 设备列表入队，循环尝试逐个调用 `state()` 或 `balance()`
2. 成功执行的设备从队列移除
3. 最多迭代 DevNum 次（避免死循环）
4. 全部设备完成即求解成功

#### 4.3.5 面向方程法求解 - `__equation_eo()`

**核心实现**：
```python
A = np.zeros((connum, connum))   # 系数矩阵
b = np.zeros(connum)              # 右端向量
# 从各组件收集方程行
for key in self.comps:
    self.comps[key].equation_rows()
    for row in self.comps[key].rows:
        for col in row["a"]:
            A[currow, col[0]] = col[1]
        b[currow] = row["b"]
# 求解线性方程组 Ax = b
fdot = np.linalg.solve(A, b)
```

---

### 4.4 仿真调度模块 (simrankine.py / SimRankineCycle)

**文件路径**：`SimRankine/rankine/simrankine.py`

提供高层 API 封装，简化调用流程：
```python
simulator_eo()              # EO 方法仿真
simulator_sm()              # SM 方法仿真
simulator_performance()     # 性能计算
specified_simulator(power, mass)  # 指定功率/质量仿真
```

---

### 4.5 工具模块 (utils.py)

**文件路径**：`SimRankine/rankine/utils.py`

#### 4.5.1 `create_dictcycle_from_jsonfile(filename)`
- 读取 JSON 配置文件
- 将字典形式的连接器对转换为 Python 元组格式
- 返回完整的循环配置字典

#### 4.5.2 `OutFiles(cycle, outfilename=None)`
- 重定向标准输出到指定文件
- 输出内容：循环性能 → 所有设备 → 所有连接器节点
- UTF-8 编码确保中文兼容性

---

## 5. 关键数据流设计

### 5.1 标准 1kg 基准仿真流程

```
  JSON 配置文件
      ↓
create_dictcycle_from_jsonfile()
      ↓
RankineCycle.__init__()
  ├─ 实例化所有组件对象
  └─ __add_node() 构建共享节点网络
      ↓
  simulator_eo()
  ├─ component_analysis_sm("STATE")  # 状态初始化
  ├─ __equation_eo()                # 线性方程组求解 fdot
  └─ energy_fdot() 遍历组件计算能量项
      ↓
  simulator_performance()
  └─ 聚合所有组件能量 → 计算效率、热耗率等
      ↓
    OutFiles() 输出结果
```

### 5.2 指定功率变工况仿真流程

```
  1kg 基准仿真（已完成）
      ↓
specified_simulator(set_power=600MW)
  ├─ 计算 SteamRate_power_generation
  ├─ 由目标功率反算总质量流量 mdot
  ├─ 遍历所有节点调用 calmdot(mdot)
  ├─ 遍历所有组件调用 calmdot(mdot)
  └─ sm_energy() 计算 MW 级实际功率
      ↓
  输出带 MW/kg/h 单位的全量结果
```

### 5.3 能量指标聚合逻辑

组件按 `energy` 属性分类聚合：

| 分类 | 聚合变量 |
|-----|---------|
| workExtracted | 汽轮机总输出功 |
| workRequired | 泵类总消耗功 |
| heatAdded | 锅炉总吸热量 |

性能指标计算公式：
```
efficiency_cycle = totalworkExtracted / totalheatAdded
efficiency_power_generation = efficiency_cycle * etam * etag
HeatRate = 3600 / efficiency_power_generation    (kJ/kWh)
SteamRate = HeatRate / totalheatAdded           (kg/kWh)
netpoweroutput = totalworkExtracted * etam * etag - totalworkRequired
```

---

## 6. JSON 配置文件格式规范

**参考文件**：`SimRankine/jsonmodel/N600.json`

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

字段说明：
- `name` - 循环标识名称
- `etam` - 机械效率（0~1）
- `etag` - 发电机效率（0~1）
- `components` - 组件数组，每个组件需指定 `devtype` 用于类型映射
- `connectors` - 连接关系数组，每项定义两个设备端口的连接

---

## 7. 组件类型注册表

**文件路径**：`SimRankine/components/__init__.py` 中的 `compdict` 字典

| devtype 值 | 组件类名 |
|-----------|---------|
| BOILER | Boiler |
| PUMP | Pump |
| TURBINEEXS | TurbineExs |
| CONDENSER | Condenser |
| FWH-OPEN-DW0 | OpenedheaterDw0 |
| FWH-OPEN-DW1 | OpenedheaterDw1 |
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

## 8. 关键技术创新点

### 8.1 双范式统一架构
同一组件代码无需修改即可同时支持 SM（顺序模块）和 EO（面向方程）两种仿真模式，兼顾了工程易用性和数值鲁棒性。

### 8.2 隐式节点共享机制
通过 Python 对象引用赋值实现端口节点的自动共享，避免复杂的图论算法，用极其简洁的代码构建大规模热流网络。

### 8.3 线性方程组自动组装
所有组件各自贡献局部质量平衡方程，主循环自动组装全局系数矩阵 `A`，最终调用 numpy.linalg.solve() 一次求解所有未知相对流量 fdot。

---

## 9. 目录结构

```
PyRankine/
├── SimRankine/
│   ├── components/          # 热力组件库
│   ├── rankine/             # 循环核心与仿真引擎
│   │   ├── __init__.py
│   │   ├── rankineobj.py    # RankineCycle 主类
│   │   ├── simrankine.py    # 高层仿真调度 API
│   │   └── utils.py         # 工具函数
│   ├── jsonmodel/
│   │   └── N600.json        # 600MW 示例循环配置
│   ├── result/              # 输出结果目录
│   ├── rankinesim.py        # 1kg 基准仿真入口
│   └── rankinesim_spec.py   # 指定功率/质量仿真入口
├── img/
│   └── N600.jpg             # 系统流程图
├── uml/                     # UML 类图
└── README.md
```

---

## 10. 运行示例

### 10.1 基础 1kg 仿真
```bash
cd SimRankine
python rankinesim.py
```

### 10.2 指定功率仿真
```bash
python rankinesim_spec.py
```

### 10.3 代码片段调用
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

**文档版本**：V2.0.0  
**最后更新**：2026-05-12  
**作者**：Cheng Maohua
