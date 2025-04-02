import logging
import sys

logging.basicConfig(level=logging.DEBUG)

from tkinter import *

from ledboardclientfull.board_api import BoardApi
from ledboardclientfull.serial_communication.c_structs.control_parameters import ControlParametersStruct


class UiControlParameters:

    SpeedRange = 200
    ScaleRange = 500
    MinMaxRange = 1024

    def __init__(self):
        self.board = BoardApi(serial_port='COM9')

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

    def save(self):
        self.board.save_control_parameters()

    def reboot_to_bootloader(self):
        self.board.reboot_in_bootloader_mode()

    def _make_ui(self):
        self.master = Tk()

        #
        # Frames
        frame_x = Frame(self.master, padx=5, pady=5, relief=RAISED, borderwidth=2)
        frame_y = Frame(self.master, padx=5, pady=5, relief=RAISED, borderwidth=2)
        frame_z = Frame(self.master, padx=5, pady=5, relief=RAISED, borderwidth=2)
        frame_min_max = Frame(self.master, padx=5, pady=5, relief=RAISED, borderwidth=2)
        frame_rgb = Frame(self.master, padx=5, pady=5, relief=RAISED, borderwidth=2)
        frame_buttons = Frame(self.master, padx=5, pady=5, relief=RAISED, borderwidth=2)
        frame_masks = Frame(self.master, padx=5, pady=5, relief=RAISED, borderwidth=2)

        frame_x.grid(row=0, column=0, padx=5, pady=5)
        frame_y.grid(row=0, column=1, padx=5, pady=5)
        frame_z.grid(row=0, column=2, padx=5, pady=5)
        frame_min_max.grid(row=1, column=0, padx=5, pady=5)
        frame_rgb.grid(row=1, column=1, padx=5, pady=5)
        frame_masks.grid(row=1, column=2, padx=5, pady=5)
        frame_buttons.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

        #
        # X
        Label(frame_x, text="X").pack(pady=5)
        self.speed_x = Scale(
            frame_x,
            from_=-UiControlParameters.SpeedRange,
            to=UiControlParameters.SpeedRange,
            orient=HORIZONTAL,
            length=200,
            command=self.send_to_board,
        )
        self.speed_x.pack(pady=5)

        self.scale_x = Scale(
            frame_x,
            from_=1,
            to=UiControlParameters.ScaleRange,
            orient=HORIZONTAL,
            length=200,
            command=self.send_to_board,
        )
        self.scale_x.pack(pady=5)

        #
        # Y
        Label(frame_y, text="Y").pack(pady=5)
        self.speed_y = Scale(
            frame_y,
            from_=-UiControlParameters.SpeedRange,
            to=UiControlParameters.SpeedRange,
            orient=HORIZONTAL,
            length=200,
            command=self.send_to_board,
        )
        self.speed_y.pack(pady=5)

        self.scale_y = Scale(
            frame_y,
            from_=1,
            to=UiControlParameters.ScaleRange,
            orient=HORIZONTAL,
            length=200,
            command=self.send_to_board,
        )
        self.scale_y.pack(pady=5)

        #
        # Z
        Label(frame_z, text="Z").pack(pady=5)
        self.speed_z = Scale(
            frame_z,
            from_=-UiControlParameters.SpeedRange,
            to=UiControlParameters.SpeedRange,
            orient=HORIZONTAL,
            length=200,
            command=self.send_to_board,
        )
        self.speed_z.pack(pady=5)

        #
        # Min / Max
        Label(frame_min_max, text="min max").pack(pady=5)
        self.min = Scale(
            frame_min_max,
            from_= 0,
            to=UiControlParameters.MinMaxRange,
            orient=HORIZONTAL,
            length=200,
            command=self.send_to_board,
        )
        self.min.pack(pady=5)

        self.max = Scale(
            frame_min_max,
            from_= 0,
            to=UiControlParameters.MinMaxRange,
            orient=HORIZONTAL,
            length=200,
            command=self.send_to_board,
        )
        self.max.pack(pady=5)

        #
        # RGB
        Label(frame_rgb, text="RGB").pack(pady=5)
        self.r = Scale(
            frame_rgb,
            from_=0,
            to=255,
            orient=HORIZONTAL,
            length=200,
            command=self.send_to_board,
        )
        self.r.pack(pady=5)
        self.g = Scale(
            frame_rgb,
            from_=0,
            to=255,
            orient=HORIZONTAL,
            length=200,
            command=self.send_to_board,
        )
        self.g.pack(pady=5)
        self.b = Scale(
            frame_rgb,
            from_=0,
            to=255,
            orient=HORIZONTAL,
            length=200,
            command=self.send_to_board,
        )
        self.b.pack(pady=5)

        #
        # Masks
        Label(frame_masks, text="Masks X").pack(pady=5)
        self.mask_x1 = Scale(
            frame_masks,
            from_=-255,
            to=255,
            orient=HORIZONTAL,
            length=200,
            command=self.send_to_board,
        )
        self.mask_x1.pack(pady=5)
        self.mask_x2 = Scale(
            frame_masks,
            from_=-255,
            to=255,
            orient=HORIZONTAL,
            length=200,
            command=self.send_to_board,
        )
        self.mask_x2.pack(pady=5)

        Label(frame_masks, text="Masks Y").pack(pady=5)
        self.mask_y1 = Scale(
            frame_masks,
            from_=-255,
            to=255,
            orient=HORIZONTAL,
            length=200,
            command=self.send_to_board,
        )
        self.mask_y1.pack(pady=5)
        self.mask_y2 = Scale(
            frame_masks,
            from_=-255,
            to=255,
            orient=HORIZONTAL,
            length=200,
            command=self.send_to_board,
        )
        self.mask_y2.pack(pady=5)

        #
        # Buttons
        self.button_from_board = Button(
            frame_buttons,
            text='From Board',
            command=self.get_from_board
        )
        self.button_from_board.pack(pady=5)

        self.button_save = Button(
            frame_buttons,
            text='Save',
            command=self.save
        )
        self.button_save.pack(pady=5)

        self.button_in_bootloader_mode = Button(
            frame_buttons,
            text='Reboot to bootloader',
            command=self.reboot_to_bootloader
        )
        self.button_in_bootloader_mode.pack(pady=5)


if __name__ == "__main__":
    if "bootloader" in sys.argv:
        print("Rebooting in bootloader mode")
        board = BoardApi(serial_port='COM9')
        board.reboot_in_bootloader_mode()
        exit(0)

    ui = UiControlParameters()
    ui._make_ui()
    mainloop()
