from ledboardclientfull.board_api import BoardApi
from ledboardclientfull.sampling_point import SamplingPoint
from ledboardclientfull.color_format import ColorFormat


board = BoardApi(serial_port='COM9')
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
