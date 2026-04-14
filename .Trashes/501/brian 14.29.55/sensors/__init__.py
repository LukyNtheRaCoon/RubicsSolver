from .SensorPort import *
from .BrianBrianComm import *
from .Sensor import *
from . import sensor_port_probe
from . import NXT as NXT
from . import EV3 as EV3
from . import HiTec as HiTec


class SensorException(Exception):
    """Default sensor Exception"""


class SensorAlreadyClosedError(SensorException):
    """Thrown when trying to access closed Sensor"""


class SensorIsNotReadyError(SensorException):
    """Thrown when trying to read values from a sensor that is not ready"""


class SensorPortAlreadyInUse(SensorException):
    """Thrown when trying to register sensor or sensor probe with autodetect to already used port"""