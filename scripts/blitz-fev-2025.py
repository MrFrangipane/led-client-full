import sys

from dataclasses import dataclass

from serial.tools.list_ports import comports as list_serial_ports

from pythonarduinoserial.types import *
from pythonarduinoserial.communicator import SerialCommunicator


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
    z: FloatType() = 0.0
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
    pin_led_first: IntegerType() = 12
    slider_logarithmic_scale: FloatType() = 1.5

    firmware_revision: IntegerType() = 0

    wifi_password: StringType(16) = "0123456789ABCDE"  # includes null terminator, length 16 to avoid manual bytes padding
    wifi_ip_address: BytesType(4) = bytes([192, 168, 0, 201])
    wifi_gateway: BytesType(4) = bytes([192, 168, 0, 1])
    wifi_subnet: BytesType(4) = bytes([255, 255, 0, 0])

    led_count: IntegerType() = 144
    led_color_format: IntegerType() = 1  # GRB

    osc_receive_port: IntegerType() = 54321


if __name__ == "__main__":
    all_structs = [
        HardwareConfigurationStruct,
        BeginSamplePointsReceptionCommand,
        EndSamplePointsReceptionCommand,
        BeginLedInfoReceptionCommand,
        SaveSamplingPointsCommand,
        SamplePointStruct,
        LedInfoStruct
    ]

    if "makecheader" in sys.argv:
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

    elif "setname" in sys.argv:
        ports = [port.name for port in list_serial_ports()]
        if len(ports) == 1:
            serial_communicator = SerialCommunicator(structs=all_structs)
            serial_communicator.set_port_name(ports[0])
            serial_communicator.connect()

            hardware_configuration_struct = serial_communicator.receive(HardwareConfigurationStruct)
            hardware_configuration_struct.name = "Valenti"

            serial_communicator.send(hardware_configuration_struct)

            count = 4
            serial_communicator.send(BeginSamplePointsReceptionCommand(count))
            for l in range(count):
                serial_communicator.send(SamplePointStruct(
                    index=l,
                    x=l * 0.1,
                    y=0.0,
                    z=0.0,
                    universe_number=0,
                    universe_channel=0,
                    color_format=1
                ))

            # serial_communicator.send(SaveSamplingPointsCommand())

            serial_communicator.disconnect()

    else:
        ports = [port.name for port in list_serial_ports()]
        if len(ports) == 1:
            serial_communicator = SerialCommunicator(structs=all_structs)
            serial_communicator.set_port_name(ports[0])
            serial_communicator.connect()

            hardware_configuration_struct = serial_communicator.receive(HardwareConfigurationStruct)
            serial_communicator.disconnect()

            print(hardware_configuration_struct)
