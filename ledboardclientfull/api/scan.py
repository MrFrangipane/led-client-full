from PySide6.QtGui import QPixmap

from ledboardclientfull.core.components import Components
from ledboardclientfull.core.entities.scan.settings import ScanSettings

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


def set_mask(mask_geometry) -> None:  # FIXME use entity
    Components().image_processor.set_mask(mask_geometry)


def reset_mask() -> None:
    Components().image_processor.reset_mask()
