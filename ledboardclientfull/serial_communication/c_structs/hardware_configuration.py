from dataclasses import dataclass

from pythonarduinoserial.types import *


@dataclass
class HardwareConfigurationStruct:
    name: StringType(8) = "Board"  # includes null terminator, length 8 to avoid manual bytes padding

    hardware_id: BytesType(8) = BytesDefault(8)
    hardware_revision: IntegerType() = 0
    gpio_admin_mode: IntegerType() = 1  # absent in Jan 2024 LedBoard
    gpio_dmx_input: IntegerType() = 5  # absent in Jan 2024 LedBoard
    gpio_led_first: IntegerType() = 6  # default for Jan 2024 LedBoard

    firmware_revision: IntegerType() = 0

    wifi_password: StringType(16) = "0123456789ABCDE"  # includes null terminator, length 16 to avoid manual bytes padding
    wifi_ip_address: BytesType(4) = bytes([192, 168, 0, 201])
    wifi_gateway: BytesType(4) = bytes([192, 168, 0, 1])
    wifi_subnet: BytesType(4) = bytes([255, 255, 0, 0])

    led_count: IntegerType() = 160  # value for 16x10 Led matrix
    led_color_format: IntegerType() = 1  # GRB

    osc_receive_port: IntegerType() = 54321
