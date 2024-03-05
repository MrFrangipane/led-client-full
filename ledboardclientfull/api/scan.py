from typing import Tuple

from PySide6.QtGui import QPixmap

from ledboardclientfull.core.components import Components
from ledboardclientfull.core.entities.scan.scan_result import ScanResult
from ledboardclientfull.core.entities.scan.settings import ScanSettings
from ledboardclientfull.core.entities.scan.mask import ScanMask
from ledboardclientfull.core.entities.mapping_tree.mapping_tree import MappingTree

# FIXME: separate detecting devices from getting names list


def get_capture_devices_names() -> list[str]:
    return Components().image_processor.get_capture_devices_names()


def set_capture_device(device_index: int) -> None:
    Components().image_processor.set_capture_device(device_index)


def set_capture_device_name(name: str) -> None:
    Components().image_processor.set_capture_device_name(name)


def capture_device_name() -> str:
    return Components().image_processor.capture_device_name()


def video_capture_index() -> int:
    return Components().image_processor.video_capture_index()


def get_settings() -> ScanSettings:
    return Components().image_processor.settings


def set_settings(settings: ScanSettings) -> None:
    Components().image_processor.settings = settings


def viewport_pixmap() -> QPixmap:
    return Components().image_processor.viewport_pixmap()


def set_mask(mask: ScanMask) -> None:
    Components().image_processor.set_mask(mask)


def get_mask():
    return Components().image_processor.mask


def reset_mask() -> None:
    Components().image_processor.reset_mask()


def start_scan() -> None:
    Components().scanner.start_scan()


def step_scan() -> None:
    Components().scanner.step_scan()


def stop_scan() -> None:
    Components().scanner.stop_scan()


def is_scanning() -> bool:
    return Components().scanner.is_scanning()


def get_detection_coordinates() -> Tuple[int, int, int]:  # FIXME make a DataClass
    return Components().image_processor.detection_coordinates


def get_scan_result() -> ScanResult:
    return Components().scanner.scan_result


def set_scan_result(result: ScanResult) -> None:
    Components().scanner.scan_result = result


def do_detection():
    Components().image_processor.viewport_pixmap()  # FIXME hacky


def map_to_tree(scan_result: ScanResult, pixel_per_segment: int, segment_to_universe_map: dict[int, int]) -> MappingTree:
    return Components().scan_to_tree_mapper.map_to_tree(scan_result, pixel_per_segment, segment_to_universe_map)
