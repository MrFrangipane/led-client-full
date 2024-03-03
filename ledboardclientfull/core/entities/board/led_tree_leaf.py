from dataclasses import dataclass


@dataclass
class LEDTreeLeaf:
    led_number: int = 0
    universe_number: int = -1
    pixel_number: int = 0
    do_clear_tree: bool = False  # FIXME: make one dedicated struct ?
