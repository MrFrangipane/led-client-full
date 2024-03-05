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
    universe_a: UniverseStructure = field(default_factory=UniverseStructure)
    universe_b: UniverseStructure = field(default_factory=UniverseStructure)
    universe_c: UniverseStructure = field(default_factory=UniverseStructure)
