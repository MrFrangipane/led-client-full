from dataclasses import dataclass

from pythonarduinoserial.types import *


@dataclass
class ControlParametersStruct:
    noise_octaves: IntegerType() = 2
    noise_scale: IntegerType() = 3

    noise_scale_x: IntegerType() = 200
    noise_scale_y: IntegerType() = 200

    noise_speed_x: IntegerType() = 0
    noise_speed_y: IntegerType() = 0
    noise_speed_z: IntegerType() = 0

    noise_min: IntegerType() = 150
    noise_max: IntegerType() = 1024 - 200

    noise_r: IntegerType() = 0
    noise_g: IntegerType() = 200
    noise_b: IntegerType() = 200

    runner_r: IntegerType() = 255
    runner_g: IntegerType() = 0
    runner_b: IntegerType() = 0

    runner_trigger: IntegerType() = 0

    # > 0: additive, < 0: multiply
    mask_x1: IntegerType() = 0
    mask_x2: IntegerType() = 0
    mask_y1: IntegerType() = 0
    mask_y2: IntegerType() = 0

    bat_low: IntegerType() = 0
    bat_1_bar: IntegerType() = 0
