from dataclasses import dataclass

from pythonarduinoserial.types import *


@dataclass
class ControlParametersStruct:
    speed: IntegerType() = 3
    scale_x: IntegerType() = 200
    scale_y: IntegerType() = 200
    min: IntegerType() = 150
    max: IntegerType() = 1024 - 200
    r: IntegerType() = 0
    g: IntegerType() = 200
    b: IntegerType() = 200
