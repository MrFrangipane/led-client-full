import time

from ledboardclientfull.board_api import BoardApi
from ledboardclientfull.sampling_point import SamplingPoint
from ledboardclientfull.color_format import ColorFormat


def make_wave_share_points():
    index = 0
    sampling_points = list()

    for y in range(10):
        for x in range(16):
            new = SamplingPoint(
                index=index,
                x=x,
                y=y,
                universe_number=0,
                universe_channel=index * 3,
                color_format=ColorFormat.RGB,
                led_indices=[index]
            )
            sampling_points.append(new)
            index += 1
    return sampling_points


def waveshare_10x16(port: str):
    board = BoardApi(serial_port=port)
    configuration = board.get_configuration()
    board.set_sampling_points(make_wave_share_points())


def strip_5m(port: str):
    board = BoardApi(serial_port=port)
    configuration = board.get_configuration()
    configuration.led_count = 300
    board.set_configuration(configuration)

    print(configuration)

    sampling_points = list()
    for s in range(150):
        new = SamplingPoint(
            index=s,
            x=int((150 - s) * 1.2),
            y=0,
            universe_number=0,
            universe_channel=s * 3,
            color_format=ColorFormat.RGB,
            led_indices=[s]
        )
        sampling_points.append(new)

    for s in range(150, 300):
        new = SamplingPoint(
            index=s,
            x=(s - 150),
            y=10,
            universe_number=0,
            universe_channel=s * 3,
            color_format=ColorFormat.RGB,
            led_indices=[s]
        )
        sampling_points.append(new)

    board.set_sampling_points(sampling_points)


def print_config(port: str):
    print("Current configuration:")
    board = BoardApi(serial_port=port)
    configuration = board.get_configuration()
    for key, value in vars(configuration).items():
        print(f"{key} = {value}")
    print('-' * 20)


def rect_256(port: str):
    board = BoardApi(serial_port=port)
    configuration = board.get_configuration()
    configuration.led_count = 256
    board.set_configuration(configuration)

    index = 0
    led_offset = 0
    sampling_points = list()  # make_wave_share_points()
    point_offset = len(sampling_points)

    for y in range(16):
        x_ = (lambda X: X) if y % 2 else (lambda X: 15 - X)
        for x in range(16):
            new = SamplingPoint(
                index=point_offset + index,
                x=x_(x),
                y=y,
                universe_number=0,
                universe_channel=index * 3,
                color_format=ColorFormat.RGB,
                led_indices=[led_offset + index]
            )
            sampling_points.append(new)
            index += 1

    print(f"Sampling points: {len(sampling_points)}")
    board.set_sampling_points(sampling_points)


def set_speed_z(port: str, speed: int):
    board = BoardApi(serial_port=port)
    parameters = board.get_control_parameters()
    if parameters is None:
        print("No parameters received !")
        return
    parameters.noise_speed_z = speed
    board.save_control_parameters()



if __name__ == '__main__':
    com = "COM11"
    # print_config(com)
    # waveshare_10x16(com)
    # strip_5m(com)
    rect_256(com)
    # set_speed_z(com, 1)
    print("Done.")
