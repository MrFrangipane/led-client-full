import cv2
import numpy as np
from numpy.typing import ArrayLike
from PySide6.QtGui import QPixmap, QImage

from ledboardclientfull.components.image_processor.video_capture import VideoCapture
from ledboardclientfull.core.entities.scan.settings import ScanSettings


class ScanImageProcessor:
    def __init__(self):
        self._video_capture = VideoCapture()
        self._device_index = -1
        self._device_names: list[str] = list()
        self.settings = ScanSettings()
        self._frame: ArrayLike = None
        self._mask: ArrayLike = None

    def get_capture_devices_names(self) -> list[str]:
        self._device_names = self._video_capture.get_devices_names()
        return self._device_names

    def set_capture_device(self, device_index: int):
        self._video_capture.open(device_index)
        self._device_index = device_index

    def set_capture_device_name(self, name: str) -> None:
        if not name:
            return

        if not self._device_names:
            self.get_capture_devices_names()  # FIXME: separate detecting devices from getting names list

        self.set_capture_device(self._device_names.index(name))

    def video_capture_index(self) -> int:
        return self._device_index

    def capture_device_name(self) -> str:
        if self._device_index == -1:
            return ""
        return self._device_names[self._device_index]

    def set_scan_settings(self, settings: ScanSettings):
        self.settings = settings

    def reset_mask(self):
        if self._mask is not None:
            self._mask.fill(255)

    def set_mask(self, mask_geometry: ArrayLike):  # fixme use a dataclass
        self._mask = np.zeros(self._frame.shape[:2], dtype="uint8")
        if mask_geometry.size:
            cv2.fillPoly(self._mask, pts=[mask_geometry], color=(255, 255, 255))

    def viewport_pixmap(self):
        if not self._video_capture.is_open:
            return QPixmap()

        self._frame = self._video_capture.read()

        if self.settings.viewport_blur and self.settings.blur_radius > 0:
            blur = self.settings.blur_radius * 2 + 1
            self._frame = cv2.GaussianBlur(self._frame, (blur, blur), 0)

        self._frame = cv2.bitwise_and(self._frame, self._frame, mask=self._mask)

        if self.settings.viewport_brightest_pixel:
            gray = cv2.cvtColor(self._frame, cv2.COLOR_RGB2GRAY)  # is it BGR ?
            _, maximum_value, _, maximum_location = cv2.minMaxLoc(gray)
            cv2.circle(self._frame, maximum_location, 5, (255, 0, 0), -1)

        height, width, channel = self._frame.shape
        bytes_per_line = 3 * width
        qt_image = QImage(self._frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(qt_image)
