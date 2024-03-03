from ledboardclientfull.core.apis import APIs
from ledboardclientfull.core.entities.mapping_tree.leaf import MappingTreeLeaf
from ledboardclientfull.core.entities.mapping_tree.structure import MappingTreeStructure, PixelStructure
from ledboardclientfull.core.entities.scan.scan_result import ScanResult
from ledboardclientfull.core.components import Components  # FIXME should we use an API to access internal settings ?


class ScanToTreeMapper:
    def __init__(self):
        self._scan_result: ScanResult = None

        self._min_x: int = None
        self._max_x: int = None

        self._pixels: dict[int, list[int]] = dict()
        self._pixel_count: int = 0

    def map_to_tree_and_send_to_board(self, pixel_count):  # FIXME split and rename
        self._pixel_count = pixel_count
        self._scan_result: ScanResult = APIs().scan.get_scan_result()

        self._find_min_max()
        self._group_by_pixels()

        tree_structure = self._make_tree_structure()
        APIs().board.set_mapping_tree_structure(tree_structure)

        for pixel_number, leds in sorted(self._pixels.items()):
            for mapping_id, led_id in enumerate(leds):
                APIs().board.send_mapping_tree_leaf(
                    MappingTreeLeaf(led_id, mapping_id, pixel_number, universe_number=0)
                )

    def _find_min_max(self):
        self._min_x = None
        self._max_x = None

        for point in self._scan_result.detected_points.values():
            if self._min_x is None:
                self._min_x = point.x
            else:
                self._min_x = min(self._min_x, point.x)

            if self._max_x is None:
                self._max_x = point.x
            else:
                self._max_x = max(self._max_x, point.x)

    def _group_by_pixels(self):
        size = self._max_x - self._min_x
        step = int(size / self._pixel_count)

        self._pixels = dict()

        for point in self._scan_result.detected_points.values():
            pos = point.x - self._min_x
            pixel_id = min(int(pos / step), self._pixel_count - 1)

            if pixel_id not in self._pixels:
                self._pixels[pixel_id] = [point.led_number]
            else:
                self._pixels[pixel_id].append(point.led_number)

    def _make_tree_structure(self) -> MappingTreeStructure:
        tree_structure = MappingTreeStructure()
        for pixel_number, leds in sorted(self._pixels.items()):
            tree_structure.universe_a.pixels.append(
                PixelStructure(index=pixel_number, led_count=len(leds))
            )

        return tree_structure


if __name__ == "__main__":
    import logging
    import os.path

    from ledboardclientfull import init_ledboard_client, BoardExecutionMode, board_api, project_api, scan_api

    logging.basicConfig(level=logging.INFO)

    init_ledboard_client()
    project_api.load(os.path.expanduser("~/ledboard-scan-ok.json"))

    configuration = board_api.get_configuration()
    configuration.execution_mode = BoardExecutionMode.ArtNet
    configuration.do_save_and_reboot = False  # FIXME weird, no ?
    board_api.set_configuration(configuration)

    scan_api.map_to_tree_and_send_to_board(
        division_count=64
    )
