from unittest import TestCase

from ledboardclientfull.core.entities.mapping_tree.structures import MappingTreeStructure, UniverseStructure, PixelStructure


# FIXME : why not simply testing SummableDict ?
class TestMappingTreeSum(TestCase):

    def setUp(self):
        #
        # A
        self.structure_a = self._make_structure(4, 2)

        self.structure_a.universes[0].pixels[0].led_count = 1
        self.structure_a.universes[0].pixels[1].led_count = 3

        self.structure_a.universes[1].pixels[0].led_count = 5
        self.structure_a.universes[1].pixels[1].led_count = 7

        self.structure_a.universes[2].pixels[0].led_count = 9
        self.structure_a.universes[2].pixels[1].led_count = 11

        self.structure_a.universes[3].pixels[0].led_count = 13
        self.structure_a.universes[3].pixels[1].led_count = 15

        #
        # B
        self.structure_b = self._make_structure(4, 3)

        self.structure_b.universes.pop(0)
        self.structure_b.universes.pop(3)

        self.structure_b.universes[1].pixels[0].led_count = 2
        self.structure_b.universes[1].pixels[1].led_count = 4
        self.structure_b.universes[1].pixels[2].led_count = 6

        self.structure_b.universes[2].pixels[0].led_count = 8
        self.structure_b.universes[2].pixels[1].led_count = 10
        self.structure_b.universes[2].pixels[2].led_count = 12

        #
        # SUM
        self.structure_sum = self._make_structure(4, 3)

        self.structure_sum.universes[0].pixels[0].led_count = 1
        self.structure_sum.universes[0].pixels[1].led_count = 3
        self.structure_sum.universes[0].pixels.pop(2)

        self.structure_sum.universes[1].pixels[0].led_count = 7
        self.structure_sum.universes[1].pixels[1].led_count = 11
        self.structure_sum.universes[1].pixels[2].led_count = 6

        self.structure_sum.universes[2].pixels[0].led_count = 17
        self.structure_sum.universes[2].pixels[1].led_count = 21
        self.structure_sum.universes[2].pixels[2].led_count = 12

        self.structure_sum.universes[3].pixels[0].led_count = 13
        self.structure_sum.universes[3].pixels[1].led_count = 15
        self.structure_sum.universes[3].pixels.pop(2)

    def test_sum(self):
        self.assertEqual(
            self.structure_a + self.structure_b,
            self.structure_sum
        )

    def test_sum_symmetry(self):
        self.assertEqual(
            self.structure_a + self.structure_b,
            self.structure_b + self.structure_a,
        )

    def test_sum_with_empty(self):
        self.assertEqual(
            self.structure_a + MappingTreeStructure(),
            self.structure_a
        )

    def _make_structure(self, universe_count, pixel_count):
        new_structure = MappingTreeStructure()

        for u in range(universe_count):
            new_structure.universes[u] = self._make_universe(u, pixel_count)

        return new_structure

    def _make_universe(self, i, pixel_count):
        new_universe = UniverseStructure()
        new_universe.index = i
        for p in range(pixel_count):
            new_universe.pixels[p] = self._make_pixel(p)
        return new_universe

    @staticmethod
    def _make_pixel(i) -> PixelStructure:
        new_pixel = PixelStructure()
        new_pixel.index = i
        return new_pixel
