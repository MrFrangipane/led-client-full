from ledboardclientfull.core.entities.mapping_tree.mapping_tree import MappingTree
from ledboardclientfull.core.entities.scan.detection_point import DetectionPoint
from ledboardclientfull.core.entities.scan.scan_result import ScanResult
from ledboardclientfull.components.mapping_tree.segment_mapper import SegmentMapper


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

        # FIXME: dont imply 3 universes
        pixel_starts: dict[int, int] = {
            0: 0,
            1: 0,
            2: 0
        }
        tree = MappingTree()
        for segment, detected_points in self._segments.items():
            universe = segment_to_universe_map[segment]
            tree += SegmentMapper().make_tree(universe, detected_points, pixel_per_segment, pixel_starts[universe])
            pixel_starts[universe] += pixel_per_segment

        return tree

    def _make_segments(self):
        self._segments = dict()
        for detected_point in self._scan_result.detected_points.values():
            if detected_point.assigned_segment_number not in self._segments:
                self._segments[detected_point.assigned_segment_number] = [detected_point]
            else:
                self._segments[detected_point.assigned_segment_number].append(detected_point)


if __name__ == "__main__":
    import logging
    import os.path

    from ledboardclientfull import init_ledboard_client, BoardExecutionMode, board_api, project_api, scan_api

    logging.basicConfig(level=logging.INFO)

    init_ledboard_client()
    project_api.load(os.path.expanduser("~/ledboard-working-project.json"))
    configuration = board_api.get_configuration()

    segment_to_universe_mapping = {
        -1: None,
        0: 0,
        1: 0,
        2: 1,
        3: 1,
        4: 2
    }
    project_tree = scan_api.map_to_tree(
        scan_result=scan_api.get_scan_result(),
        pixel_per_segment=int(configuration.pixel_per_universe / 2),  # two half-totem per universe
        segment_to_universe_map=segment_to_universe_mapping
    )
    from pprint import pprint
    pprint(project_tree)

    # configuration.universe_a = 0
    # configuration.universe_b = 1
    # configuration.universe_c = 2
    # configuration.execution_mode = BoardExecutionMode.ArtNet
    # configuration.do_save_and_reboot = True
    # board_api.set_configuration(configuration)
