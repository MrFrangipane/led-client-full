from dataclasses import dataclass


@dataclass
class DetectionPoint:
    led_number: int
    x: int
    y: int
