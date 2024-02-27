from dataclasses import dataclass


@dataclass
class Illumination:
    led_start: int = 0
    led_end: int = 0
    r: int = 0
    g: int = 0
    b: int = 0
    w: int = 0
