from dataclasses import dataclass

from pythonarduinoserial.types import *


@dataclass
class ControlParametersStruct:
    speed_x: IntegerType() = 0
    speed_y: IntegerType() = 0
    speed_z: IntegerType() = 0

    scale_x: IntegerType() = 200
    scale_y: IntegerType() = 200

    min: IntegerType() = 150
    max: IntegerType() = 1024 - 200

    r: IntegerType() = 0
    g: IntegerType() = 200
    b: IntegerType() = 200

    # > 0: additive, < 0: multiply
    mask_x1: IntegerType() = 0
    mask_x2: IntegerType() = 0
    mask_y1: IntegerType() = 0
    mask_y2: IntegerType() = 0

    noise_scale: IntegerType() = 3
    noise_octaves: IntegerType() = 2
