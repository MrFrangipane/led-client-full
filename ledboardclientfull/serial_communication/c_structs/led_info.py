from dataclasses import dataclass

from pythonarduinoserial.types import *


@dataclass
class LedInfoStruct:
    sampling_point_index: IntegerType() = 0
    led_index: IntegerType() = 0
