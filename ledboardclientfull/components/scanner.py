import logging
import time
from copy import copy

from ledboardclientfull.core.apis import APIs

from ledboardclientfull.core.entities.board.illumination import BoardIllumination
from ledboardclientfull.core.entities.board.illumination_type import BoardIlluminationType

from ledboardclientfull.core.entities.scan.detection_point import DetectionPoint
from ledboardclientfull.core.entities.scan.scan_result import ScanResult
from ledboardclientfull.core.entities.scan.settings import ScanSettings

_logger = logging.getLogger(__name__)


class Scanner:

    def __init__(self):
        self.scan_result: ScanResult = None

        self._backup_illumination: BoardIllumination = None
        self._current_led = 0
        self._is_scanning = False
        self._settings: ScanSettings = None

    def start_scan(self):
        self._backup_illumination = APIs().illumination.get_illumination()
        self._settings = APIs().scan.get_settings()

        self.scan_result = ScanResult(
            board_configuration=APIs().board.get_configuration(),
            scan_settings=self._settings
        )

        self._current_led = self._settings.led_first
        self._is_scanning = True

        _logger.info(f"Starting scan {self._settings}")

    def step_scan(self):
        if self._current_led > self._settings.led_last:
            self.stop_scan()
            return

        illumination = copy(self._backup_illumination)
        illumination.type = BoardIlluminationType.Single
        illumination.led_single = self._current_led
        APIs().illumination.illuminate(illumination)

        time.sleep(self._settings.detection_time_interval_ms / 1000.0)
        APIs().scan.do_detection()

        x, y, value = APIs().scan.get_detection_coordinates()
        if value > self._settings.detection_value_threshold:
            new = DetectionPoint(
                led_number=self._current_led,
                x=x, y=y
            )
            self.scan_result.detected_points[self._current_led] = new
            _logger.info(f"Detected LED {new} (v={value})")
        else:
            _logger.info(f"Skipped LED {self._current_led} (v={value})")

        self._current_led += 1

    def stop_scan(self):
        self._current_led = 0
        self._is_scanning = False
        APIs().illumination.illuminate(self._backup_illumination)

    def is_scanning(self) -> bool:
        return self._is_scanning
