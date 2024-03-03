from ledboardclientfull.core.apis import APIs
from ledboardclientfull.core.entities.mapping_tree.leaf import MappingTreeLeaf
from ledboardclientfull.core.entities.mapping_tree.structure import MappingTreeStructure, PixelStructure
from ledboardclientfull.core.entities.scan.scan_result import ScanResult


class SegmentExporter:
    def __init__(self):
        self._scan_result: ScanResult = None

        self._min_x: int = None
        self._max_x: int = None

        self._pixels: dict[int, list[int]] = dict()
        self._pixel_count: int = 0

    def export(self, filename, pixel_count):
        self._pixel_count = pixel_count
        self._scan_result: ScanResult = APIs().scan.get_scan_result()

        self._find_min_max()
        self._group_by_pixels()

        # print(self._make_c_vectors_definitions())
        tree_structure = self._make_tree_structure()
        APIs().board.set_led_tree_structure(tree_structure)

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

    def _make_c_vectors_definitions(self) -> str:
        content = ["const std::vector<std::vector<int>> ledTree {"]
        for pixel in range(128):
            leds = self._pixels.get(pixel, None)
            if leds is not None:
                line = "    {" + ', '.join([str(led) for led in leds]) + "}"
            else:
                line = "    {}"

            if pixel < 127:
                line += ","

            content.append(line)
        content.append("};")

        return "\n".join(content)


if __name__ == "__main__":
    import os.path
    from ledboardclientfull import init_ledboard_client, project_api, scan_api

    init_ledboard_client()
    project_api.load(os.path.expanduser("~/ledboard-scan-ok.json"))
    scan_api.export_indexed_led_segment(
        filename="exported-segments.json",
        division_count=64
    )
