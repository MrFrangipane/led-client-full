import time

from pythonarduinoserial.communicator import SerialCommunicator

from ledboardclientfull.sampling_point import SamplingPoint
from ledboardclientfull.serial_communication import c_commands, c_structs, all_structs


class BoardApi:

    def __init__(self, serial_port):
        self.serial_port = serial_port

        self.serial_communicator = SerialCommunicator(structs=all_structs.get())
        self.serial_communicator.set_port_name(self.serial_port)

    def __del__(self):
        self.serial_communicator.disconnect()

    def configure(self, configuration: c_structs.HardwareConfigurationStruct):
        self.serial_communicator.send(configuration)

    def get_configuration(self) -> c_structs.HardwareConfigurationStruct:
        return self.serial_communicator.receive(c_structs.HardwareConfigurationStruct)

    def set_sampling_points(self, sampling_points: list[SamplingPoint]):
        if not sampling_points:
            return

        self.serial_communicator.send(c_commands.BeginSamplePointsReceptionCommand(len(sampling_points)))
        for sampling_point in sampling_points:
            self.serial_communicator.send(c_structs.SamplePointStruct.from_sampling_point(sampling_point))
            for led_index in sampling_point.led_indices:
                self.serial_communicator.send(c_structs.LedInfoStruct(sampling_point.index, led_index))

        time.sleep(0.6)
        self.serial_communicator.send(c_commands.SaveSamplingPointsCommand())
        time.sleep(0.6)
        self.serial_communicator.send(c_commands.EndSamplePointsReceptionCommand())

    def get_control_parameters(self) -> c_structs.ControlParametersStruct:
        return self.serial_communicator.receive(c_structs.ControlParametersStruct)

    def set_control_parameters(self, parameters: c_structs.ControlParametersStruct):
        self.serial_communicator.send(parameters)

    def save_control_parameters(self):
        self.serial_communicator.send(c_commands.SaveControlParametersCommand())

    def reboot_in_bootloader_mode(self):
        self.serial_communicator.send(c_commands.RebootInBootloaderModeCommand())
