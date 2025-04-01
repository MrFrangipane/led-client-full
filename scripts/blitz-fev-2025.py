import json
from dataclasses import dataclass

from pythonarduinoserial.types import *


def make_simple_led_strip_data(count_x, count_y):
    data = dict()
    sampling_points: dict[int, SamplePointStruct] = dict()
    led_infos: list[LedInfoStruct] = list()
    pixels_done = list()

    sampling_point_index = 0
    for y in range(count_y):
        for x in range(count_x):
            sampling_points[sampling_point_index + 1] = SamplePointStruct(
                index=sampling_point_index,
                x=float(x),
                y=float(y),
                universe_number=1,
                universe_channel=sampling_point_index * 3,
                color_format=1
            )

            led_infos.append(
                LedInfoStruct(
                    sampling_point_index=sampling_point_index,
                    led_index=sampling_point_index
                )
            )
            sampling_point_index += 1

    data[1] = {
        "sampling_points": sampling_points,
        "led_infos": led_infos
    }

    return data


def read_scan_data():

    import json

    tree_filepath = "E:/PROJECTS_2025/ledboard-projects/backups/pylones-OK-2024-03-06.json"
    scan_filepath = "E:/PROJECTS_2025/ledboard-projects/scan-a-b-c-d-2024-03-06-v1.json"

    with open(tree_filepath, "r") as tree_file:
        tree = json.load(tree_file)

    with open(scan_filepath, "r") as scan_file:
        scan = json.load(scan_file)

    universes = sorted(tree["structure"]["universes"].keys())

    data = dict()
    sampling_point_index = 0
    for universe in universes:
        sampling_points: dict[int, SamplePointStruct] = dict()
        led_infos: list[LedInfoStruct] = list()
        pixels_done = list()

        for leaves in tree["leaves"]['universes'][universe]["leaves"].values():
            for leaf in leaves:
                if leaf["pixel_number"] not in pixels_done:
                    pixels_done.append(leaf["pixel_number"])
                    sampling_point_index += 1

                scan_point = scan["scan_result"]["detected_points"][str(leaf["led_id"])]
                sampling_points[sampling_point_index] = SamplePointStruct(
                    index=sampling_point_index - 1,
                    x=0.0, #float(scan_point["x"]) / 10.0,
                    y=float(scan_point["y"]) / 10.0,
                    universe_number=int(universe),
                    universe_channel=sampling_point_index * 3,
                    color_format=1
                )

                led_infos.append(
                    LedInfoStruct(
                        sampling_point_index=sampling_point_index,
                        led_index=leaf["led_id"]
                    )
                )
        data[universe] = {
            "sampling_points": sampling_points,
            "led_infos": led_infos
        }

    return data


if __name__ == "__main__":
    import sys
    import time

    PORT = 'COM9'

    from serial.tools.list_ports import comports as list_serial_ports
    from pythonarduinoserial.communicator import SerialCommunicator

    all_structs = [
        HardwareConfigurationStruct,
        BeginSamplePointsReceptionCommand,
        EndSamplePointsReceptionCommand,
        BeginLedInfoReceptionCommand,
        SaveSamplingPointsCommand,
        SamplePointStruct,
        LedInfoStruct
    ]

    ports = [port.name for port in list_serial_ports()]
    ports = [PORT] if PORT in ports else ports
    print(ports)

    def make_header():
        import argparse
        import logging
        import sys

        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
        parser = argparse.ArgumentParser(description="RP2040 LED Board - C Header exporter")
        parser.add_argument("--export-header", "-e", required=True, help="Export C Header to given filepath")
        args, _ = parser.parse_known_args()

        from pythonarduinoserial.c_header_exporter import CHeaderExporter

        c_header_exporter = CHeaderExporter(
            struct_types=all_structs,
            namespace="Frangitron",
            include_guard_name="PLATFORMIO_SERIALPROTOCOL_H"
        )
        with open(args.export_header, "w+") as c_header_file:
            c_header_file.write(c_header_exporter.export())

    def upload_blitz():
        if len(ports) != 1:
            print("No serial port found")
            return

        serial_communicator = SerialCommunicator(structs=all_structs)
        serial_communicator.set_port_name(ports[0])
        serial_communicator.connect()

        hardware_configuration_struct = serial_communicator.receive(HardwareConfigurationStruct)
        hardware_configuration_struct.name = "Blitz"
        hardware_configuration_struct.pin_led_first = 6
        hardware_configuration_struct.led_count = 160

        serial_communicator.send(hardware_configuration_struct)

        # scan_data = read_scan_data()
        scan_data = make_simple_led_strip_data(16, 10)
        count = sum([len(universe['sampling_points']) for universe in scan_data.values()])
        print(f"total SamplingPoint: {count}")

        serial_communicator.send(BeginSamplePointsReceptionCommand(count))
        for data_universe in scan_data.values():
            for sampling_point in data_universe["sampling_points"].values():
                serial_communicator.send(sampling_point)
                for led_info in data_universe["led_infos"]:
                    if led_info.sampling_point_index == sampling_point.index:
                        serial_communicator.send(led_info)

                print(sampling_point.index)

        time.sleep(0.6)
        serial_communicator.send(SaveSamplingPointsCommand())
        time.sleep(0.6)
        serial_communicator.send(EndSamplePointsReceptionCommand())

        serial_communicator.disconnect()

    def  get_info():
        if len(ports) == 1:
            serial_communicator = SerialCommunicator(structs=all_structs)
            serial_communicator.set_port_name(ports[0])
            serial_communicator.connect()

            hardware_configuration_struct = serial_communicator.receive(HardwareConfigurationStruct)
            serial_communicator.disconnect()

            print(hardware_configuration_struct)


    if "makecheader" in sys.argv:
        make_header()

    elif "upload-blitz" in sys.argv:
        upload_blitz()

    else:
        import pprint
        get_info()
        data = read_scan_data()
        pprint.pprint(data)
