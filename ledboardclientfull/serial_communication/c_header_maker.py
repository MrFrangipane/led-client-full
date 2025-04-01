import argparse
import logging
import sys

from pythonarduinoserial.c_header_exporter import CHeaderExporter

from ledboardclientfull.serial_communication import all_structs


def make_c_header(filepath: str):
    c_header_exporter = CHeaderExporter(
        struct_types=all_structs.get(),
        namespace="Frangitron",
        include_guard_name="PLATFORMIO_SERIALPROTOCOL_H"
    )

    with open(filepath, "w+") as c_header_file:
        c_header_file.write(c_header_exporter.export())


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    parser = argparse.ArgumentParser(description="RP2040 LED Board - C Header exporter")
    parser.add_argument("--export-header", "-e", required=True, help="Export C Header to given filepath")
    args, _ = parser.parse_known_args()

    make_c_header(filepath=args.export_header)
