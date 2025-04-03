from ledboardclientfull.board_api import BoardApi
from ledboardclientfull.sampling_point import SamplingPoint
from ledboardclientfull.color_format import ColorFormat


def waveshare_10x16(port: str):
    board = BoardApi(serial_port=port)
    configuration = board.get_configuration()

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

    board.set_sampling_points(sampling_points)


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
            x=s - 150,
            y=10,
            universe_number=0,
            universe_channel=s * 3,
            color_format=ColorFormat.RGB,
            led_indices=[s]
        )
        sampling_points.append(new)

    board.set_sampling_points(sampling_points)


if __name__ == '__main__':
    # waveshare_10x16('COM9')
    strip_5m('COM4')
