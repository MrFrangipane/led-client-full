from dataclasses import dataclass
from ipaddress import IPv4Address

from ledboardclientfull.core.entities.board.execution_mode import BoardExecutionMode
from ledboardclientfull.core.entities.board.pixel_type import PixelType


@dataclass
class BoardConfiguration:
    name: str = ""

    execution_mode: BoardExecutionMode = BoardExecutionMode.Illumination

    serial_port_name: str = ""
    hardware_revision: int = 1
    firmware_revision: int = 1
    hardware_id: str = ""

    ip_address: IPv4Address = IPv4Address('0.0.0.0')
    universe: int = -1

    pixel_per_transmitter: int = 150
    pixel_type: PixelType = PixelType.GRBW

    do_save_and_reboot: bool = False
    do_reboot_bootloader: bool = False
