from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from ledboardclientfull import ScanResult
from ledboardclientfull.core.entities.board.configuration import BoardConfiguration
from ledboardclientfull.core.entities.board.illumination import BoardIllumination
from ledboardclientfull.core.entities.scan.mask import ScanMask
from ledboardclientfull.core.entities.scan.settings import ScanSettings


@dataclass_json
@dataclass
class Project:
    name: str = "New LED Board project"

    board_configuration: BoardConfiguration = field(default_factory=BoardConfiguration)
    board_illumination: BoardIllumination = field(default_factory=BoardIllumination)

    scan_capture_device_name: str = ""
    scan_mask: ScanMask = field(default_factory=ScanMask)
    scan_result: ScanResult = None
    scan_settings: ScanSettings = field(default_factory=ScanSettings)

    serialization_version: int = 1  # Read only /!\
