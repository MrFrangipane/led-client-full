from ledboardclientfull.core.apis import APIs
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

        universe_numbers = sorted({u: 0 for u in set(segment_to_universe_map.values()) if u is not None})
        pixel_starts = {u: 0 for u in universe_numbers}
        tree = MappingTree()
        for segment, detected_points in self._segments.items():
            universe = segment_to_universe_map[segment]
            if universe is None:
                raise ValueError(f"Following points are not assigned a segment: {detected_points}")
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


if __name__ == "__main__":
    import logging
    import os.path
    import json
    from ipaddress import IPv4Address

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
        pixel_per_segment=4, #int(configuration.pixel_per_universe / 2),  # two half-totem per universe
        segment_to_universe_map=segment_to_universe_mapping
    )

    with open('project_tree.json', 'w+') as project_tree_file:
        json.dump(project_tree.to_dict(), project_tree_file, indent=2)

    configuration.universe_a = 0
    configuration.universe_b = 1
    configuration.universe_c = 2
    configuration.ip_address = IPv4Address('192.168.20.201')
    configuration.execution_mode = BoardExecutionMode.ArtNet
    configuration.do_save_and_reboot = False
    board_api.set_configuration(configuration)

    scan_api.send_to_board(project_tree)

    configuration.do_save_and_reboot = True
    board_api.set_configuration(configuration)
