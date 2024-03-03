from dataclasses import dataclass


@dataclass
class MappingTreeLeaf:
    led_id: int = 0  # LED Strip
    mapping_id: int = 0  # Tree Mapping
    pixel_number: int = 0  # Artnet
    universe_number: int = 0  # Artnet
