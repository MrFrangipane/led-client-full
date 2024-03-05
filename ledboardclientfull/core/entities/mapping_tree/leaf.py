from dataclasses import dataclass


@dataclass
class MappingTreeLeaf:
    led_id: int = 0  # LED Strip
    mapping_id: int = 0  # Tree Mapping
    pixel_number: int = 0  # Artnet
    universe_number: int = 0  # Artnet

    def __add__(self, other):
        raise ValueError(
            f'Two {self.__class__.__name__} cannot be summed ! '
            f'(self.led_id={self.led_id}, other.led_id={other.led_id})'
        )
