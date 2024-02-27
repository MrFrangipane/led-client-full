from dataclasses import dataclass

from pythonarduinoserial.types import *

from ledboardclientfull.core.board_configuration import BoardConfiguration


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
    def from_board_configuration(board_configuration: BoardConfiguration):
        new = BoardConfigurationStruct()
        new.name = board_configuration.name
        # TODO finish here
        return new

    def to_board_configuration(self) -> BoardConfiguration:
        new = BoardConfiguration()
        new.name = self.name
        # TODO finish here
        return new


@dataclass
class IlluminationStruct:
    led_start: IntegerType() = 0
    led_end: IntegerType() = 0
    r: IntegerType() = 0
    g: IntegerType() = 0
    b: IntegerType() = 0
    w: IntegerType() = 0


all_structs = [
    BoardConfigurationStruct,
    IlluminationStruct
]


if __name__ == "__main__":
    import argparse
    import logging
    import sys

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    parser = argparse.ArgumentParser(description="RP2040 LED Board - C Header exporter")
    parser.add_argument("--export-header", "-e", required=True, help="Export C Header to given filepath")
    args = parser.parse_args()

    from pythonarduinoserial.c_header_exporter import CHeaderExporter

    c_header_exporter = CHeaderExporter(
        struct_types=all_structs,
        namespace="Frangitron",
        include_guard_name="PLATFORMIO_SERIALPROTOCOL_H"
    )
    with open(args.export_header, "w+") as c_header_file:
        c_header_file.write(c_header_exporter.export())
