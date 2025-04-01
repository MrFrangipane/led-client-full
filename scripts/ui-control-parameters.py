from tkinter import *

from ledboardclientfull.board_api import BoardApi
from ledboardclientfull.serial_communication.c_structs.control_parameters import ControlParametersStruct


class UiControlParameters:
    def __init__(self):
        self.board = BoardApi(serial_port='COM9')

    def send_to_board(self, value):
        self.board.set_control_parameters(ControlParametersStruct(
            speed=self.speed.get(),
            scale_x=self.scale_x.get(),
            scale_y=self.scale_y.get()
        ))

    def get_from_board(self):
        parameters = self.board.get_control_parameters()
        if parameters is None:
            print("No parameters received !")
            return

        self.speed.set(parameters.speed)
        self.scale_x.set(parameters.scale_x)
        self.scale_y.set(parameters.scale_y)

    def save(self):
        self.board.save_control_parameters()

    def reboot_to_bootloader(self):
        self.board.reboot_in_bootloader_mode()

    def _make_ui(self):
        self.master = Tk()

        self.speed = Scale(
            self.master,
            from_=0,
            to=50,
            orient=HORIZONTAL,
            length=200,
            command=self.send_to_board
        )
        self.speed.pack()

        self.scale_x = Scale(
            self.master,
            from_=1,
            to=500,
            orient=HORIZONTAL,
            length=200,
            command=self.send_to_board
        )
        self.scale_x.pack()

        self.scale_y = Scale(
            self.master,
            from_=1,
            to=500,
            orient=HORIZONTAL,
            length=200,
            command=self.send_to_board
        )
        self.scale_y.pack()

        self.button_from_board = Button(
            self.master,
            text='From Board',
            command=self.get_from_board
        )
        self.button_from_board.pack()

        self.button_save = Button(
            self.master,
            text='Save',
            command=self.save
        )
        self.button_save.pack()

        self.button_in_bootloader_mode = Button(
            self.master,
            text='Reboot to bootloader',
            command=self.reboot_to_bootloader
        )
        self.button_in_bootloader_mode.pack()

ui = UiControlParameters()
ui._make_ui()
mainloop()
