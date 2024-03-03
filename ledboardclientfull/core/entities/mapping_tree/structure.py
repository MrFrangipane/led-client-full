from dataclasses import dataclass, field


@dataclass
class PixelStructure:
    index: int = 0
    led_count: int = 0


@dataclass
class UniverseStructure:
    pixels: list[PixelStructure] = field(default_factory=list)


@dataclass
class MappingTreeStructure:
    universe_a: UniverseStructure = UniverseStructure()
    universe_b: UniverseStructure = UniverseStructure()
    universe_c: UniverseStructure = UniverseStructure()
