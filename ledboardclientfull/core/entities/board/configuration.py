from dataclasses import dataclass
from ipaddress import IPv4Address

from ledboardclientfull.core.entities.board.execution_mode import BoardExecutionMode
from ledboardclientfull.core.entities.board.pixel_type import PixelType
from ledboardclientfull.core.components import Components


@dataclass
class BoardConfiguration:
    name: str = ""

    execution_mode: BoardExecutionMode = BoardExecutionMode.Illumination

    serial_port_name: str = ""
    firmware_revision: int = 1
    hardware_id: str = ""
    hardware_revision: int = 1

    ip_address: IPv4Address = IPv4Address('0.0.0.0')
    universe_a: int = -1
    universe_b: int = -1
    universe_c: int = -1

    pixel_per_transmitter: int = 64  # value for Blitz (half totem)
    pixel_per_universe: int = Components().configuration.pixel_per_universe
    pixel_type: PixelType = PixelType.GRBW

    do_save_and_reboot: bool = False
    do_reboot_bootloader: bool = False
