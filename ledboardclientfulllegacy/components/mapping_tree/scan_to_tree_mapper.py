import logging

from ledboardclientfull.core.apis import APIs
from ledboardclientfull.core.entities.mapping_tree.mapping_tree import MappingTree
from ledboardclientfull.core.entities.scan.detection_point import DetectionPoint
from ledboardclientfull.core.entities.scan.scan_result import ScanResult
from ledboardclientfull.components.mapping_tree.segment_mapper import SegmentMapper


_logger = logging.getLogger(__name__)


class ScanToTreeMapper:
    """
    Maps a ScanResult to a MappingTree
    """

    def __init__(self):
        self._scan_result: ScanResult = None
        self._segments: dict[int: list[DetectionPoint]] = dict()  # { segment_number: [detection_point] }

    def map_to_tree(self, scan_result, pixel_per_segment, segment_to_universe_map) -> MappingTree:
        self._scan_result = scan_result

        self._make_segments()

        universe_numbers = sorted({u: 0 for u in set(segment_to_universe_map.values()) if u is not None})
        pixel_starts = {u: 0 for u in universe_numbers}
        tree = MappingTree()
        for segment, detected_points in self._segments.items():
            universe = segment_to_universe_map[segment]
            if universe is None:
                _logger.warning(f"{len(detected_points)} detected points are not assigned a segment")
                continue
            tree += SegmentMapper().make_tree(universe, detected_points, pixel_per_segment, pixel_starts[universe])
            pixel_starts[universe] += pixel_per_segment

        return tree

    @staticmethod
    def send_to_board(mapping_tree: MappingTree):
        APIs().board.set_mapping_tree_structure(mapping_tree.structure)
        all_leaves = mapping_tree.leaves.all()
        for leaf in all_leaves:
            APIs().board.send_mapping_tree_leaf(leaf)

    def _make_segments(self):
        self._segments = dict()
        for detected_point in self._scan_result.detected_points.values():
            if detected_point.assigned_segment_number not in self._segments:
                self._segments[detected_point.assigned_segment_number] = [detected_point]
            else:
                self._segments[detected_point.assigned_segment_number].append(detected_point)
