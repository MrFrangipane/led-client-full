from ledboardclientfull.core.entities.scan.detection_point import DetectionPoint
from ledboardclientfull.core.entities.mapping_tree.mapping_tree import MappingTree
from ledboardclientfull.core.entities.mapping_tree.leaf import MappingTreeLeaf
from ledboardclientfull.core.entities.mapping_tree.structures import MappingTreeStructure, PixelStructure, UniverseStructure
from ledboardclientfull.core.entities.mapping_tree.leaves import Leaves, LeavesUniverse


# FIXME: this has to be more explicit (we need a Segment object)
class SegmentMapper:
    """
    Maps detected points to a MappingTree, given a universe and pixel per segment count and a pixel start offset

    Merge different MappingTrees by adding them together to get all mapped pixels
    """

    def __init__(self):
        self._universe: int = -1
        self._detected_points: list[DetectionPoint] = None
        self._pixel_count: int = None

        self._min_x: int = None
        self._max_x: int = None

        self._pixels: dict[int, list[int]] = dict()  # { pixel_number : [led_id] }
        self._pixel_count: int = 0
        self._pixel_start: int = 0

    def make_tree(self, universe, detected_points, pixel_per_segment, pixel_start) -> MappingTree:
        self._universe = universe
        self._detected_points = detected_points
        self._pixel_count = pixel_per_segment
        self._pixel_start = pixel_start

        self._find_min_max()
        self._group_by_pixels()

        tree = MappingTree()

        tree.structure = self._make_structure()
        tree.leaves = self._make_leaves()

        return tree

    def _find_min_max(self) -> None:
        self._min_x = None
        self._max_x = None

        for point in self._detected_points:
            if self._min_x is None:
                self._min_x = point.x
            else:
                self._min_x = min(self._min_x, point.x)

            if self._max_x is None:
                self._max_x = point.x
            else:
                self._max_x = max(self._max_x, point.x)

    def _group_by_pixels(self) -> None:
        size = self._max_x - self._min_x
        step = int(size / self._pixel_count)

        self._pixels = dict()

        for point in self._detected_points:
            pos = point.x - self._min_x
            pixel_number = self._pixel_start + min(int(pos / step), self._pixel_count - 1)

            if pixel_number not in self._pixels:
                self._pixels[pixel_number] = [point.led_number]
            else:
                self._pixels[pixel_number].append(point.led_number)

    def _make_structure(self) -> MappingTreeStructure:
        tree_structure = MappingTreeStructure()

        # FIXME: make this part of MappingTreeStructure ?
        if self._universe not in tree_structure.universes:
            tree_structure.universes[self._universe] = UniverseStructure()
            tree_structure.universes[self._universe].index = self._universe

        for pixel_number, leds in sorted(self._pixels.items()):
            tree_structure.universes[self._universe].pixels[pixel_number] = PixelStructure(
                index=pixel_number,
                led_count=len(leds)
            )

        return tree_structure

    def _make_leaves(self) -> Leaves:
        leaves = Leaves()

        # FIXME: make this part of MappingTreeStructure ?
        if self._universe not in leaves.universes:
            leaves.universes[self._universe] = LeavesUniverse()
            leaves.universes[self._universe].index = self._universe

        for pixel_number, leds in sorted(self._pixels.items()):
            leaves.universes[self._universe].leaves[pixel_number] = list()
            for mapping_id, led_id in enumerate(leds):
                leaves.universes[self._universe].leaves[pixel_number].append(
                    MappingTreeLeaf(led_id, mapping_id, pixel_number, self._universe)
                )

        return leaves
