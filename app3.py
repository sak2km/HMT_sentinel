from Tkinter import *
from tkinter import ttk
from msg_window2 import msg_window2
from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, Command
import time, math, pdb, argparse
from pymavlink import mavutil




# root.destroy()
class app3():
    def __init__(self):
        # self.vehicle = vehicle
        print("hi")

    def run(self):
        root = Tk()
        root.title("Sentinel Panel")
        app = msg_window2(master=root)
        # app.button_handler2()
        app.configure(bg='gray90')
        app.entry_update()

        app.mainloop()