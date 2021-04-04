"""
The PyRankine: the  hybrid steady-state simulator of Rankine Cycle

Package: components

Author: Cheng Maohua, Email: cmh@seu.edu.cn
"""

from .port import Port
from .connector import Connector
#
from .boiler import Boiler
from .reheater import Reheater
#
from .turbineexs import TurbineExs
#
from .condenser import Condenser
#
from .pump import Pump
#
from .pipeptloss import PipePtloss
from .pipeploss import PipePloss
from .pipemloss import PipeMloss
from .pipeilevel import PipeIlevel

#
from .openedheaterdw0 import OpenedheaterDw0
from .closedheaterdw0 import ClosedHeaterDw0
from .openedheaterdw1 import OpenedheaterDw1
from .closedheaterdw1 import ClosedHeaterDw1
from .combinedheater import CombinedHeater
#
from .split_one2two import Split_One2Two

# ------------------------------------------------------------------------------
# compdict(jump table)
#  1: key:value-> Type String: class  name
#  2    add the new key:value to the dict after you add the new device class/type
# --------------------------------------------------------------------------------

compdict = {
    "BOILER": Boiler,
    "REHEATER": Reheater,

    "TURBINEEXS": TurbineExs,

    "CONDENSER": Condenser,

    "PUMP": Pump,

    "FWH-OPEN-DW0": OpenedheaterDw0,
    "FWH-OPEN-DW1": OpenedheaterDw1,
    "FWH-CLOSE-DW0": ClosedHeaterDw0,
    "FWH-CLOSE-DW1": ClosedHeaterDw1,
    "FWH-CLOSE-DW1-SG-CWP-WELL": CombinedHeater,
 
    "PIPEMLOSS": PipeMloss,
    "PIPEPTLOSS": PipePtloss,
    "PIPEPLOSS": PipePloss,
    "PIPEILEVEL": PipeIlevel,

    "SPLIT_ONE2TWO": Split_One2Two
    
}
