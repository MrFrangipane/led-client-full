from dataclasses import dataclass


@dataclass
class ScanSettings:
    viewport_blur: bool = False
    viewport_brightest_pixel: bool = False
    blur_radius: int = 0
    led_first: int = 0
    led_last: int = 0
    detection_value_threshold: int = 230
    detection_time_interval_ms: int = 200
