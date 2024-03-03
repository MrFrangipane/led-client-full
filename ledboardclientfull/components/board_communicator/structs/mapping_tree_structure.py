import logging
from dataclasses import dataclass

from pythonarduinoserial.types import *

from ledboardclientfull.core.entities.mapping_tree.structure import MappingTreeStructure, UniverseStructure, PixelStructure
from ledboardclientfull.core.components import Components

_logger = logging.getLogger(__name__)

_ppu = Components().configuration.pixel_per_universe
_PixelsLEDCountType = ListType(type_=IntegerType(), length=_ppu)


@dataclass
class MappingTreeStructureStruct:
    universe_a_pixels_led_count: _PixelsLEDCountType = ListDefault(type_=IntegerType(), length=_ppu)
    universe_b_pixels_led_count: _PixelsLEDCountType = ListDefault(type_=IntegerType(), length=_ppu)
    universe_c_pixels_led_count: _PixelsLEDCountType = ListDefault(type_=IntegerType(), length=_ppu)

    @staticmethod
    def from_entity(source: MappingTreeStructure):
        univ_a = [0] * 128
        univ_b = [0] * 128
        univ_c = [0] * 128

        for pixel in source.universe_a.pixels:
            if pixel.index > _ppu - 1:
                _logger.warning(f"MappingTreeStructureStruct overflow for Universe A, pixel {pixel.index}")
                break
            univ_a[pixel.index] = pixel.led_count

        for pixel in source.universe_b.pixels:
            if pixel.index > _ppu - 1:
                _logger.warning(f"MappingTreeStructureStruct overflow for Universe B, pixel {pixel.index}")
                break
            univ_b[pixel.index] = pixel.led_count

        for pixel in source.universe_c.pixels:
            if pixel.index > _ppu - 1:
                _logger.warning(f"MappingTreeStructureStruct overflow for Universe B, pixel {pixel.index}")
                break
            univ_c[pixel.index] = pixel.led_count

        new = MappingTreeStructureStruct(
            universe_a_pixels_led_count=univ_a,
            universe_b_pixels_led_count=univ_b,
            universe_c_pixels_led_count=univ_c
        )

        return new

    def to_entity(self) -> MappingTreeStructure:
        new = MappingTreeStructure()

        for pixel_index, led_count in enumerate(self.universe_a_pixels_led_count):
            new.universe_a.pixels.append(PixelStructure(pixel_index, led_count))

        for pixel_index, led_count in enumerate(self.universe_b_pixels_led_count):
            new.universe_b.pixels.append(PixelStructure(pixel_index, led_count))

        for pixel_index, led_count in enumerate(self.universe_c_pixels_led_count):
            new.universe_c.pixels.append(PixelStructure(pixel_index, led_count))

        return new
