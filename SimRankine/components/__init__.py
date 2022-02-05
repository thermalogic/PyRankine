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
    Boiler.devtype: Boiler,
    Reheater.devtype: Reheater,

    TurbineExs.devtype: TurbineExs,

    Condenser.devtype: Condenser,

    Pump.devtype: Pump,

    OpenedheaterDw0.devtype: OpenedheaterDw0,
    OpenedheaterDw1.devtype: OpenedheaterDw1,
    ClosedHeaterDw0.devtype: ClosedHeaterDw0,
    ClosedHeaterDw1.devtype: ClosedHeaterDw1,
    CombinedHeater.devtype: CombinedHeater,
 
    PipeMloss.devtype: PipeMloss,
    PipePtloss.devtype: PipePtloss,
    PipePloss.devtype: PipePloss,
    PipeIlevel.devtype: PipeIlevel,

    Split_One2Two.devtype: Split_One2Two
    
}
