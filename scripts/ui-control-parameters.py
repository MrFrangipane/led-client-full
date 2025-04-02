import logging
import os

import sys

from pythonhelpers.tk_inter import Button, Frame, Main, IntegerSlider

from ledboardclientfull.board_api import BoardApi
from ledboardclientfull.serial_communication.c_structs.control_parameters import ControlParametersStruct


class UiControlParameters:
    SpeedRange = 200
    ScaleRange = 500
    MinMaxRange = 1024
    MaskRange = 255
    Padding = 5
    SliderWidth = 200

    def __init__(self, serial_port: str):
        self.board = BoardApi(serial_port)

    def send_to_board(self, value):
        self.board.set_control_parameters(ControlParametersStruct(
            speed_x=self.speed_x.get(),
            speed_y=self.speed_y.get(),
            speed_z=self.speed_z.get(),
            scale_x=self.scale_x.get(),
            scale_y=self.scale_y.get(),
            min=self.min.get(),
            max=self.max.get(),
            r=self.r.get(),
            g=self.g.get(),
            b=self.b.get(),
            mask_x1=self.mask_x1.get(),
            mask_x2=self.mask_x2.get(),
            mask_y1=self.mask_y1.get(),
            mask_y2=self.mask_y2.get(),
            noise_octaves=self.noise_octaves.get(),
            noise_scale=self.noise_scale.get()
        ))

    def get_from_board(self):
        parameters = self.board.get_control_parameters()
        if parameters is None:
            print("No parameters received !")
            return

        self.speed_x.set(parameters.speed_x)
        self.speed_y.set(parameters.speed_y)
        self.speed_z.set(parameters.speed_z)
        self.scale_x.set(parameters.scale_x)
        self.scale_y.set(parameters.scale_y)
        self.min.set(parameters.min)
        self.max.set(parameters.max)
        self.r.set(parameters.r)
        self.g.set(parameters.g)
        self.b.set(parameters.b)
        self.mask_x1.set(parameters.mask_x1)
        self.mask_x2.set(parameters.mask_x2)
        self.mask_y1.set(parameters.mask_y1)
        self.mask_y2.set(parameters.mask_y2)
        self.noise_octaves.set(parameters.noise_octaves)
        self.noise_scale.set(parameters.noise_scale)

    def save(self):
        self.board.save_control_parameters()
        hardware_configuration = self.board.get_configuration()

        if hardware_configuration is None:
            raise ValueError("Could not retrieve hardware configuration")
        self.board.set_configuration(hardware_configuration)
        print("Saved")

    def reboot_to_bootloader(self):
        self.board.reboot_in_bootloader_mode()

    def make_ui(self):
        self.main = Main("LED Board Serial utility")

        #
        # Frames
        frame_x = Frame(
            caption="X",
            parent=self.main,
            grid_row=0, grid_column=0
        )
        frame_y = Frame(
            caption="Y",
            parent=self.main,
            grid_row=0, grid_column=1
        )
        frame_z = Frame(
            caption="Z",
            parent=self.main,
            grid_row=0, grid_column=2
        )
        frame_noise = Frame(
            caption="Noise Params",
            parent=self.main,
            grid_row=1, grid_column=0
        )
        frame_rgb = Frame(
            caption="RGB",
            parent=self.main,
            grid_row=1, grid_column=1
        )
        frame_masks = Frame(
            caption="Masks",
            parent=self.main,
            grid_row=1, grid_column=2
        )
        frame_buttons = Frame(
            caption="Buttons",
            parent=self.main,
            grid_row=2, grid_column=1
        )

        #
        # X
        self.speed_x = IntegerSlider(
            "Speed",
            parent=frame_x,
            command=self.send_to_board,
            range_=UiControlParameters.SpeedRange,
            is_range_symmetric=True
        )
        self.scale_x = IntegerSlider(
            "Scale",
            parent=frame_x,
            command=self.send_to_board,
            range_=UiControlParameters.ScaleRange,
            is_range_symmetric=False
        )

        #
        # Y
        self.speed_y = IntegerSlider(
            "Speed",
            parent=frame_y,
            command=self.send_to_board,
            range_=UiControlParameters.SpeedRange,
            is_range_symmetric=True
        )
        self.scale_y = IntegerSlider(
            "Scale",
            parent=frame_y,
            command=self.send_to_board,
            range_=UiControlParameters.ScaleRange,
            is_range_symmetric=False
        )

        #
        # Z
        self.speed_z = IntegerSlider(
            "Speed",
            parent=frame_z,
            command=self.send_to_board,
            range_=UiControlParameters.SpeedRange,
            is_range_symmetric=True
        )

        #
        # Noise Params
        self.noise_scale = IntegerSlider(
            "Scale",
            parent=frame_noise,
            command=self.send_to_board,
            min_=1, max_=16
        )
        self.noise_octaves = IntegerSlider(
            "Octaves",
            parent=frame_noise,
            command=self.send_to_board,
            min_=1, max_=6
        )
        self.min = IntegerSlider(
            "Min",
            parent=frame_noise,
            command=self.send_to_board,
            range_=UiControlParameters.MinMaxRange,
            is_range_symmetric=False
        )
        self.max = IntegerSlider(
            "Max",
            parent=frame_noise,
            command=self.send_to_board,
            range_=UiControlParameters.MinMaxRange,
            is_range_symmetric=False
        )

        #
        # RGB
        self.r = IntegerSlider(
            "R",
            parent=frame_rgb,
            command=self.send_to_board,
            range_=UiControlParameters.MaskRange,
            is_range_symmetric=False
        )
        self.g = IntegerSlider(
            "G",
            parent=frame_rgb,
            command=self.send_to_board,
            range_=UiControlParameters.MaskRange,
            is_range_symmetric=False
        )
        self.b = IntegerSlider(
            "B",
            parent=frame_rgb,
            command=self.send_to_board,
            range_=UiControlParameters.MaskRange,
            is_range_symmetric=False
        )

        #
        # Masks
        self.mask_x1 = IntegerSlider(
            "X +",
            parent=frame_masks,
            command=self.send_to_board,
            range_=UiControlParameters.MaskRange,
            is_range_symmetric=True
        )
        self.mask_x2 = IntegerSlider(
            "X -",
            parent=frame_masks,
            command=self.send_to_board,
            range_=UiControlParameters.MaskRange,
            is_range_symmetric=True
        )
        self.mask_y1 = IntegerSlider(
            "Y +",
            parent=frame_masks,
            command=self.send_to_board,
            range_=UiControlParameters.MaskRange,
            is_range_symmetric=True
        )
        self.mask_y2 = IntegerSlider(
            "Y -",
            parent=frame_masks,
            command=self.send_to_board,
            range_=UiControlParameters.MaskRange,
            is_range_symmetric=True
        )

        #
        # Buttons
        self.button_send = Button(
            'From Board',
            parent=frame_buttons,
            command=self.get_from_board
        )
        self.button_save = Button(
            'Save',
            parent=frame_buttons,
            command=self.save
        )
        self.button_in_bootloader_mode = Button(
            'Reboot to bootloader',
            parent=frame_buttons,
            command=self.reboot_to_bootloader
        )


if __name__ == "__main__":
    import shutil
    import time

    com = "COM4"

    logging.basicConfig(level=logging.INFO)

    if "bootloader" in sys.argv:
        print("Rebooting in bootloader mode")
        board = BoardApi(serial_port=com)
        board.reboot_in_bootloader_mode()
        exit(0)

    if "upload" in sys.argv:
        filepath = sys.argv[-1]
        if not os.path.exists(filepath):
            raise ValueError(f"File {filepath} does not exist !")

        if not os.path.exists("F:/"):
            print("Rebooting in bootloader mode")
            board = BoardApi(serial_port=com)
            board.reboot_in_bootloader_mode()

        time.sleep(2)

        print(f"Uploading {filepath} to board")
        shutil.copy(filepath, "F:/")

        time.sleep(2)

    print("Starting UI")
    ui = UiControlParameters(serial_port=com)
    ui.make_ui()
    ui.get_from_board()
    Main.run()
