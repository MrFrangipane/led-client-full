from dataclasses import dataclass

from pythonarduinoserial.types import *

from ledboardclientfull.sampling_point import SamplingPoint


@dataclass
class SamplePointStruct:
    index: IntegerType() = 0
    x: IntegerType() = 0
    y: IntegerType() = 0
    universe_number: IntegerType() = 0
    universe_channel: IntegerType() = 0
    color_format: IntegerType() = 0

    @staticmethod
    def from_sampling_point(sampling_point: SamplingPoint) -> "SamplePointStruct":
        new = SamplePointStruct()
        new.index = sampling_point.index
        new.x = sampling_point.x
        new.y = sampling_point.y
        new.universe_number = sampling_point.universe_number
        new.universe_channel = sampling_point.universe_channel
        new.color_format = sampling_point.color_format
        return new
