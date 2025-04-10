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
    configuration.led_count = 150
    configuration.gpio_led_first = 12
    board.set_configuration(configuration)

    print(configuration)

    sampling_points = list()
    for i in range(6):
        for s in range(150):
            index = (i * 150) + s
            new = SamplingPoint(
                index=index,
                x=int(s * (1 + (i * .1))),
                y=i * 10,
                universe_number=0,
                universe_channel=s * 3,
                color_format=ColorFormat.RGB,
                led_indices=[index]
            )
            sampling_points.append(new)

    board.set_sampling_points(sampling_points)


if __name__ == '__main__':
    # waveshare_10x16('COM9')
    strip_5m('COM11')
