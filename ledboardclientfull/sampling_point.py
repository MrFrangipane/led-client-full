from dataclasses import dataclass

from ledboardclientfull.color_format import ColorFormat


@dataclass
class SamplingPoint:
    index: int
    x: int
    y: int
    universe_number: int
    universe_channel: int
    color_format: ColorFormat
    led_indices: list[int]
