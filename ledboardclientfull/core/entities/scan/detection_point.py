from dataclasses import dataclass


@dataclass
class DetectionPoint:
    led_number: int
    lightness: int
    x: int
    y: int
