from ledboardclientfull.core.apis import APIs
from ledboardclientfull.core.entities.scan.scan_result import ScanResult


class SegmentExporter:
    def __init__(self):
        pass

    def export(self, filename, transmitter, division_count):
        scan_result: ScanResult = APIs().scan.get_scan_result()
        min_x = None
        max_x = None

        for point in scan_result.detected_points.values():
            if min_x is None:
                min_x = point.x
            else:
                min_x = min(min_x, point.x)

            if max_x is None:
                max_x = point.x
            else:
                max_x = max(max_x, point.x)

        size = max_x - min_x
        step = int(size / division_count)

        divisions = dict()

        for point in scan_result.detected_points.values():
            pos = point.x - min_x
            division = min(int(pos / step), division_count - 1)

            if division not in divisions:
                divisions[division] = [point.led_number]
            else:
                divisions[division].append(point.led_number)

        content = ["const std::vector<std::vector<int>> divisions {"]
        for pixel in range(128):
            leds = divisions.get(pixel, None)
            if leds is not None:
                line = "    {" + ', '.join([str(led) for led in leds]) + "}"
            else:
                line = "    {}"

            if pixel < 127:
                line += ","

            content.append(line)
        content.append("};")

        print("")
        print("\n".join(content))
        print("")
