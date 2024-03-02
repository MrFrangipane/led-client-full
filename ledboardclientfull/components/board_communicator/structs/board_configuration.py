from dataclasses import dataclass
from binascii import hexlify
from ipaddress import IPv4Address

from pythonarduinoserial.types import *

from ledboardclientfull.core.entities.board.configuration import BoardConfiguration
from ledboardclientfull.core.entities.board.pixel_type import PixelType


@dataclass
class BoardConfigurationStruct:
    name: StringType(8) = StringDefault(8)  # includes null terminator, length 8 to avoid manual bytes padding
    hardware_revision: IntegerType() = 1
    firmware_revision: IntegerType() = 1
    hardware_id: BytesType(8) = BytesDefault(8)
    ip_address: BytesType(4) = BytesDefault(4)
    universe: IntegerType() = -1
    pixel_per_transmitter: IntegerType() = 150
    pixel_type: IntegerType() = 0  # 4 bytes int instead of bool to avoid manual bytes padding
    do_save_and_reboot: IntegerType() = 0  # 4 bytes int instead of bool to avoid manual bytes padding
    do_reboot_bootloader: IntegerType() = 0

    @staticmethod
    def from_entity(source: BoardConfiguration):
        new = BoardConfigurationStruct()

        new.name = source.name[:7]  # TODO check if necessary ?
        new.hardware_revision = source.hardware_revision
        new.firmware_revision = source.firmware_revision
        new.hardware_id = source.hardware_id.replace(" ", "").encode("ascii")
        new.ip_address = bytes([int(i) for i in str(source.ip_address).split('.')])
        new.universe = source.universe
        new.pixel_per_transmitter = source.pixel_per_transmitter
        new.pixel_type = source.pixel_type.value
        new.do_save_and_reboot = int(source.do_save_and_reboot)
        new.do_reboot_bootloader = int(source.do_reboot_bootloader)

        return new

    def to_entity(self) -> BoardConfiguration:
        new = BoardConfiguration()

        new.name = self.name.strip(" \x00")
        new.hardware_revision = self.hardware_revision
        new.firmware_revision = self.firmware_revision
        new.hardware_id = hexlify(self.hardware_id, sep=" ").decode()  # FIXME construct a proper string
        new.ip_address = IPv4Address(".".join(str(int(b)) for b in self.ip_address))
        new.universe = self.universe
        new.pixel_per_transmitter = self.pixel_per_transmitter
        new.pixel_type = PixelType(self.pixel_type)
        new.do_save_and_reboot = bool(self.do_save_and_reboot)
        new.do_reboot_bootloader = bool(self.do_reboot_bootloader)

        return new
