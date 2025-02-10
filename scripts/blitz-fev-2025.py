import json
from dataclasses import dataclass

from pythonarduinoserial.types import *


@dataclass
class BeginSamplePointsReceptionCommand:
    count: IntegerType() = 0


@dataclass
class EndSamplePointsReceptionCommand:
    unused: IntegerType() = 0


@dataclass
class BeginLedInfoReceptionCommand:
    count: IntegerType() = 0


@dataclass
class SaveSamplingPointsCommand:
    unused: IntegerType() = 0  # FIXME


@dataclass
class SamplePointStruct:
    index: IntegerType() = 0
    x: FloatType() = 0.0
    y: FloatType() = 0.0
    universe_number: IntegerType() = 0
    universe_channel: IntegerType() = 0
    color_format: IntegerType() = 0


@dataclass
class LedInfoStruct:
    sampling_point_index: IntegerType() = 0
    led_index: IntegerType() = 0


@dataclass
class HardwareConfigurationStruct:
    name: StringType(8) = "Board"  # includes null terminator, length 8 to avoid manual bytes padding

    hardware_id: BytesType(8) = BytesDefault(8)
    hardware_revision: IntegerType() = 0
    pin_admin_mode: IntegerType() = 1
    pin_dmx_input: IntegerType() = 11
    pin_led_first: IntegerType() = 6  # GPIO number
    slider_logarithmic_scale: FloatType() = 1.5

    firmware_revision: IntegerType() = 0

    wifi_password: StringType(16) = "0123456789ABCDE"  # includes null terminator, length 16 to avoid manual bytes padding
    wifi_ip_address: BytesType(4) = bytes([192, 168, 0, 201])
    wifi_gateway: BytesType(4) = bytes([192, 168, 0, 1])
    wifi_subnet: BytesType(4) = bytes([255, 255, 0, 0])

    led_count: IntegerType() = 144
    led_color_format: IntegerType() = 1  # GRB

    osc_receive_port: IntegerType() = 54321


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
    for universe in universes:
        sampling_points: dict[int, SamplePointStruct] = dict()
        led_infos: list[LedInfoStruct] = list()
        for leaves in tree["leaves"]['universes'][universe]["leaves"].values():
            for leaf in leaves:
                sampling_point_index = leaf["pixel_number"]
                scan_point = scan["scan_result"]["detected_points"][str(leaf["led_id"])]
                sampling_points[sampling_point_index] = SamplePointStruct(
                    index=sampling_point_index,
                    x=float(scan_point["x"]) / 10.0,
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
    ports = ['COM4'] if 'COM4' in ports else ports
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

        data_universe_0 = read_scan_data()['0']

        serial_communicator = SerialCommunicator(structs=all_structs)
        serial_communicator.set_port_name(ports[0])
        serial_communicator.connect()

        hardware_configuration_struct = serial_communicator.receive(HardwareConfigurationStruct)
        hardware_configuration_struct.name = "Blitz"
        hardware_configuration_struct.pin_led_first = 6
        hardware_configuration_struct.led_count = 250

        serial_communicator.send(hardware_configuration_struct)

        count = 450 # RP2040 can only handle that much ? (not tested with multiple leds per point)
        serial_communicator.send(BeginSamplePointsReceptionCommand(count))

        for sampling_point in data_universe_0["sampling_points"].values():
            serial_communicator.send(sampling_point)
            for led_info in data_universe_0["led_infos"]:
                if led_info.sampling_point_index == sampling_point.index:
                    serial_communicator.send(led_info)

            time.sleep(0.01)

        serial_communicator.send(EndSamplePointsReceptionCommand())
        serial_communicator.send(SaveSamplingPointsCommand())
        time.sleep(0.01)

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

        led_indexes = sorted([led.led_index for led in data['0']['led_infos']])
        pprint.pprint(led_indexes)
