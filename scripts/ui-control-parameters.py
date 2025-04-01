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

    def save(self):
        self.board.save_control_parameters()

    def reboot_to_bootloader(self):
        self.board.reboot_in_bootloader_mode()

    def _make_ui(self):
        self.master = Tk()

        #
        # X
        frame_x = Frame(self.master, padx=5, pady=5, relief=RAISED, borderwidth=2)
        frame_x.pack(fill=BOTH, expand=True, padx=5, pady=5)
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
        frame_y = Frame(self.master, padx=5, pady=5, relief=RAISED, borderwidth=2)
        frame_y.pack(fill=BOTH, expand=True, padx=5, pady=5)
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
        frame_z = Frame(self.master, padx=5, pady=5, relief=RAISED, borderwidth=2)
        frame_z.pack(fill=BOTH, expand=True, padx=5, pady=5)
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
        frame_min_max = Frame(self.master, padx=5, pady=5, relief=RAISED, borderwidth=2)
        frame_min_max.pack(fill=BOTH, expand=True, padx=5, pady=5)
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
        # Buttons
        self.button_from_board = Button(
            self.master,
            text='From Board',
            command=self.get_from_board
        )
        self.button_from_board.pack(pady=5)

        self.button_save = Button(
            self.master,
            text='Save',
            command=self.save
        )
        self.button_save.pack(pady=5)

        self.button_in_bootloader_mode = Button(
            self.master,
            text='Reboot to bootloader',
            command=self.reboot_to_bootloader
        )
        self.button_in_bootloader_mode.pack(pady=5)

ui = UiControlParameters()
ui._make_ui()
mainloop()
