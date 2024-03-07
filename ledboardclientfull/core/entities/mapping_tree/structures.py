from dataclasses import dataclass, field

from ledboardclientfull.python_extensions.summable_dict import SummableDict


@dataclass
class PixelStructure:
    index: int = -1
    led_count: int = 0

    def __add__(self, other):
        if self.index != other.index:
            raise ValueError(
                f'Cannot add two {self.__class__.__name__} with different index '
                f'(self.index={self.index}, other.index={other.index})'
            )
        return PixelStructure(
            index=self.index,
            led_count=self.led_count + other.led_count
        )


@dataclass
class UniverseStructure:
    index: int = -1
    pixels: SummableDict[int, PixelStructure] = field(default_factory=SummableDict)

    def __add__(self, other):
        return UniverseStructure(
            index=self.index,
            pixels=self.pixels + other.pixels
        )


@dataclass
class MappingTreeStructure:
    universes: SummableDict[int, UniverseStructure] = field(default_factory=SummableDict)

    def __add__(self, other):
        return MappingTreeStructure(
            universes=self.universes + other.universes
        )
