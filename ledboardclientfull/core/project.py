from dataclasses import dataclass

from dataclasses_json import dataclass_json

from ledboardclientfull.core.board.configuration import BoardConfiguration
from ledboardclientfull.core.board.illumination import BoardIllumination
from ledboardclientfull.core.scan.mask import ScanMask
from ledboardclientfull.core.scan.settings import ScanSettings


@dataclass_json
@dataclass
class Project:
    name: str = "New LED Board project"
    board_configuration: BoardConfiguration = BoardConfiguration()
    board_illumination: BoardIllumination = BoardIllumination()
    scan_capture_device_name: str = ""
    scan_mask: ScanMask = ScanMask()
    scan_settings: ScanSettings = ScanSettings()
