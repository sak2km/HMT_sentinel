from Tkinter import *
from msg_window2 import msg_window2
from msg_window1 import msg_window1
from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, Command
import time, math, pdb, argparse
from pymavlink import mavutil


#Set up option parsing to get connection string
# parser = argparse.ArgumentParser(description='Demonstrates basic mission operations.')
# parser.add_argument('--connect', 
#                    help="vehicle connection target string. If not specified, SITL automatically started and used.")
# args = parser.parse_args()

# connection_string = args.connect
# vehicle = connect(connection_string, wait_ready=True)



# root = Tk()
# app = msg_window2(master=root)
# # app.button_handler2()
# app.entry_update(vehicle)

# app.mainloop()
# # root.destroy()



# from app3 import app3
# app3_obj = app3()
# app3_obj.run()
# print("hii")

root2 = Tk()
root2.title("Sentinel Panel")
app2 = msg_window2(master=root2)
# app.button_handler2()
app2.configure(bg='#00274d')
app2.entry_update()

app2.mainloop()