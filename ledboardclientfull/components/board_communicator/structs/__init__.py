from ledboardclientfull.components.board_communicator.structs.board_configuration import BoardConfigurationStruct
from ledboardclientfull.components.board_communicator.structs.illumination import IlluminationStruct
from ledboardclientfull.components.board_communicator.structs.led_tree_leaf import MappingTreeLeafStruct


all_structs = [
    BoardConfigurationStruct,
    IlluminationStruct,
    MappingTreeLeafStruct
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
