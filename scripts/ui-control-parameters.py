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
        self.board = BoardApi(serial_port=serial_port)

    def send_to_board(self, _=None):
        params = ControlParametersStruct(
            noise_speed_x=self.speed_x.get(),
            noise_speed_y=self.speed_y.get(),
            noise_speed_z=self.speed_z.get(),
            noise_scale_x=self.scale_x.get(),
            noise_scale_y=self.scale_y.get(),
            noise_min=self.min.get(),
            noise_max=self.max.get(),
            noise_r=self.r.get(),
            noise_g=self.g.get(),
            noise_b=self.b.get(),
            mask_x1=self.mask_x1.get(),
            mask_x2=self.mask_x2.get(),
            mask_y1=self.mask_y1.get(),
            mask_y2=self.mask_y2.get(),
            noise_octaves=self.noise_octaves.get(),
            noise_scale=self.noise_scale.get()
        )
        self.board.set_control_parameters(params)

    def get_from_board(self, _=None):
        parameters = self.board.get_control_parameters()
        if parameters is None:
            print("No parameters received !")
            return

        self.speed_x.set(parameters.noise_speed_x)
        self.speed_y.set(parameters.noise_speed_y)
        self.speed_z.set(parameters.noise_speed_z)
        self.scale_x.set(parameters.noise_scale_x)
        self.scale_y.set(parameters.noise_scale_y)
        self.min.set(parameters.noise_min)
        self.max.set(parameters.noise_max)
        self.r.set(parameters.noise_r)
        self.g.set(parameters.noise_g)
        self.b.set(parameters.noise_b)
        self.mask_x1.set(parameters.mask_x1)
        self.mask_x2.set(parameters.mask_x2)
        self.mask_y1.set(parameters.mask_y1)
        self.mask_y2.set(parameters.mask_y2)
        self.noise_octaves.set(parameters.noise_octaves)
        self.noise_scale.set(parameters.noise_scale)

    def save(self, _=None):
        self.board.save_control_parameters()
        hardware_configuration = self.board.get_configuration()

        if hardware_configuration is None:
            raise ValueError("Could not retrieve hardware configuration")
        self.board.set_configuration(hardware_configuration)
        print("Saved")

    def reboot_to_bootloader(self, _=None):
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
            on_change=self.send_to_board,
            range_=UiControlParameters.SpeedRange,
            is_range_symmetric=True
        )
        self.scale_x = IntegerSlider(
            "Scale",
            parent=frame_x,
            on_change=self.send_to_board,
            range_=UiControlParameters.ScaleRange,
            is_range_symmetric=False
        )

        #
        # Y
        self.speed_y = IntegerSlider(
            "Speed",
            parent=frame_y,
            on_change=self.send_to_board,
            range_=UiControlParameters.SpeedRange,
            is_range_symmetric=True
        )
        self.scale_y = IntegerSlider(
            "Scale",
            parent=frame_y,
            on_change=self.send_to_board,
            range_=UiControlParameters.ScaleRange,
            is_range_symmetric=False
        )

        #
        # Z
        self.speed_z = IntegerSlider(
            "Speed",
            parent=frame_z,
            on_change=self.send_to_board,
            range_=UiControlParameters.SpeedRange,
            is_range_symmetric=True
        )

        #
        # Noise Params
        self.noise_scale = IntegerSlider(
            "Scale",
            parent=frame_noise,
            on_change=self.send_to_board,
            min_=1, max_=16
        )
        self.noise_octaves = IntegerSlider(
            "Octaves",
            parent=frame_noise,
            on_change=self.send_to_board,
            min_=1, max_=6
        )
        self.min = IntegerSlider(
            "Min",
            parent=frame_noise,
            on_change=self.send_to_board,
            range_=UiControlParameters.MinMaxRange,
            is_range_symmetric=False
        )
        self.max = IntegerSlider(
            "Max",
            parent=frame_noise,
            on_change=self.send_to_board,
            range_=UiControlParameters.MinMaxRange,
            is_range_symmetric=False
        )

        #
        # RGB
        self.r = IntegerSlider(
            "R",
            parent=frame_rgb,
            on_change=self.send_to_board,
            range_=UiControlParameters.MaskRange,
            is_range_symmetric=False
        )
        self.g = IntegerSlider(
            "G",
            parent=frame_rgb,
            on_change=self.send_to_board,
            range_=UiControlParameters.MaskRange,
            is_range_symmetric=False
        )
        self.b = IntegerSlider(
            "B",
            parent=frame_rgb,
            on_change=self.send_to_board,
            range_=UiControlParameters.MaskRange,
            is_range_symmetric=False
        )

        #
        # Masks
        self.mask_x1 = IntegerSlider(
            "X +",
            parent=frame_masks,
            on_change=self.send_to_board,
            range_=UiControlParameters.MaskRange,
            is_range_symmetric=True
        )
        self.mask_x2 = IntegerSlider(
            "X -",
            parent=frame_masks,
            on_change=self.send_to_board,
            range_=UiControlParameters.MaskRange,
            is_range_symmetric=True
        )
        self.mask_y1 = IntegerSlider(
            "Y +",
            parent=frame_masks,
            on_change=self.send_to_board,
            range_=UiControlParameters.MaskRange,
            is_range_symmetric=True
        )
        self.mask_y2 = IntegerSlider(
            "Y -",
            parent=frame_masks,
            on_change=self.send_to_board,
            range_=UiControlParameters.MaskRange,
            is_range_symmetric=True
        )

        #
        # Buttons
        self.button_send = Button(
            'From Board',
            parent=frame_buttons,
            on_press=self.get_from_board
        )
        self.button_save = Button(
            'Save',
            parent=frame_buttons,
            on_press=self.save
        )
        self.button_in_bootloader_mode = Button(
            'Reboot to bootloader',
            parent=frame_buttons,
            on_press=self.reboot_to_bootloader
        )


if __name__ == "__main__":
    import shutil
    import time

    com = None
    firmware_filepath = None
    for arg in sys.argv:
        if arg.startswith("COM"):
            com = arg

        if arg.endswith(".uf2"):
            firmware_filepath = arg

    logging.basicConfig(level=logging.INFO)

    if "bootloader" in sys.argv:
        print("Rebooting in bootloader mode")
        board = BoardApi(serial_port=com)
        board.reboot_in_bootloader_mode()
        exit(0)

    if "upload" in sys.argv:
        if not os.path.exists(firmware_filepath):
            raise ValueError(f"File {firmware_filepath} does not exist !")

        if not os.path.exists("F:/"):
            print("Rebooting in bootloader mode")
            board = BoardApi(serial_port=com)
            board.reboot_in_bootloader_mode()

        time.sleep(2)

        print(f"Uploading {firmware_filepath} to board")
        shutil.copy(firmware_filepath, "F:/")

        time.sleep(2)

    print(f"Starting UI for {com}")
    ui = UiControlParameters(serial_port=com)
    ui.make_ui()
    ui.get_from_board()
    Main.run()
