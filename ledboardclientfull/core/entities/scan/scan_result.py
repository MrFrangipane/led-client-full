from dataclasses import dataclass, field
from dataclasses_json import dataclass_json


from ledboardclientfull.core.entities.board.configuration import BoardConfiguration
from ledboardclientfull.core.entities.scan.settings import ScanSettings
from ledboardclientfull.core.entities.scan.detection_point import DetectionPoint


@dataclass_json
@dataclass
class ScanResult:
    board_configuration: BoardConfiguration
    scan_settings: ScanSettings
    detected_points: dict[int, DetectionPoint] = field(default_factory=dict)
