from Tkinter import *
from tkinter import ttk
import datetime

class msg_window2(Frame):

    def button_handler(self,button_num):
        print("At counter %s, button %s clicked!!" %(self.counter, button_num))

        fileName = "scripts/button_log.txt"
        output='counter button_clicked\n'
        # Keep track of what button has been clicked at what iteration

        output+="%s\t%s\n" % (self.counter,button_num)

        self.counter += 1

        with open(fileName, 'w') as file_:
            # print " Write mission to file"
            file_.write(output)

    def entry_update(self, vehicle=None):
        # print("hi")
        # entry_altitude.delete(1.0, END)
        # self.alt = vehicle.location.global_relative_frame.alt
        self.read_parameters()


        self.txt_function.configure(text=self.function)
        self.txt_mission.configure(text=self.mission)
        self.txt_battery.configure(text=self.battery)
        self.flight_time = str(datetime.timedelta(seconds=self.flight_time_sec))
        self.txt_time.configure(text=self.flight_time[0:10])

        # self.entry_altitude.delete(0, END)
        # self.entry_altitude.insert(0, self.alt)
        # self.entry_speed.delete(0, END)
        # self.entry_speed.insert(0, self.speed)
        # self.entry_battery.delete(0, END)
        # self.entry_battery.insert(0, self.battery)
        # self.entry_waypoint.delete(0, END)
        # self.entry_waypoint.insert(0, self.waypoint)

        # self.sentinel_txt.configure(state='normal')
        # self.sentinel_txt.delete(1.0, END)
        # self.sentinel_txt.insert(INSERT,self.sentinel_msg)
        # self.sentinel_txt.configure(state='disabled')

        # f = open("selectionRatio.txt", 'w+')

                    # self.f.write(c2)
                    # self.f.write('\n')
        # print(alt)
        self.after(500,self.entry_update)

    def createWidgets(self):
        self.counter = 0

        # create all of the main containers
        self.frame1 = Frame(self, bg='gray', highlightbackground="gray90", highlightthickness=5, width=300, height=150, pady=5)
        self.frame2 = Frame(self, bg='gray', highlightbackground="gray90", highlightthickness=5, width=300, height=150, pady=5)
        self.frame3 = Frame(self, bg='gray', highlightbackground="gray90", highlightthickness=5, width=300, height=150, pady=5)
        self.frame4 = Frame(self, bg='gray', highlightbackground="gray90", highlightthickness=5, width=300, height=150, pady=5)
        self.frame5 = Frame(self, bg='gray', highlightbackground="gray90", highlightthickness=5, width=300, height=150, pady=5)
        self.frame6 = Frame(self, bg='gray90', highlightbackground="gray90", highlightthickness=5,  width=300, height=150, pady=5)
        self.frame_function_battery = Frame(self, bg='gray', width=300, height=10, pady=3)
        self.frame_mission_time = Frame(self, bg='gray', width=300, height=10, pady=3)
        # self.frame_battery = Frame(self, bg='white', width=300, height=10, pady=3)
        # self.frame_time = Frame(self, bg='white', width=300, height=10, pady=3)

        # # layout all of the main containers
        # self.grid_rowconfigure(1, weight=1)
        # self.grid_columnconfigure(0, weight=1)

        self.frame1.grid(row=0, column=0)
        self.frame2.grid(row=0, column=1)
        self.frame3.grid(row=1, column=0)
        self.frame4.grid(row=1, column=1)
        self.frame5.grid(row=2, column=0)
        self.frame6.grid(row=2, column=1)
        self.frame_function_battery.grid(row=3, column=0)
        self.frame_mission_time.grid(row=3, column=1)
        # self.frame_battery.grid(row=4, column=0)
        # self.frame_time.grid(row=4, column=1)


        self.label_forceland = Label(self.frame1, bg='gray',text="Force Land", font='Helvetica 14 bold').grid(row=0, column=0)
        self.label_guided = Label(self.frame2, bg='gray',text="Guided Mode", font='Helvetica 14 bold').grid(row=0, column=0)
        self.label_original = Label(self.frame3, bg='gray',text="Original Plan", font='Helvetica 14 bold').grid(row=0, column=0)
        self.label_alternative = Label(self.frame4, bg='gray',text="Alternative Plan", font='Helvetica 14 bold').grid(row=0, column=0)
        self.label_home = Label(self.frame5, bg='gray',text="Return to Base", font='Helvetica 14 bold').grid(row=0, column=0)
        self.label_function = Label(self.frame_function_battery, bg='gray', text="Function", font='Helvetica 14 bold').grid(row=0, column=0)
        self.label_mission = Label(self.frame_mission_time, bg='gray', text="Mission", font='Helvetica 14 bold').grid(row=0, column=0)
        self.label_battery = Label(self.frame_function_battery, bg='gray', text="Battery", font='Helvetica 14 bold').grid(row=1, column=0)
        self.label_time = Label(self.frame_mission_time, bg='gray', text="Flight Time", font='Helvetica 14 bold').grid(row=1, column=0)

        # ttk.Style().configure("RB.TButton", foreground='red', background='red')
        # self.button_1 = ttk.Button(self.frame1, text="Applyyy", style="RB.TButton", command= lambda: self.button_handler(0))
        # self.button_1.grid(row=0, column=1)
        self.button_1 = Button(self.frame1, text="Apply", command= lambda: self.button_handler(0)).grid(row=0, column=1)
        self.button_2 = Button(self.frame2, text="Apply", command= lambda: self.button_handler(1)).grid(row=0, column=1)
        self.button_3 = Button(self.frame3, text="Apply", command= lambda: self.button_handler(2)).grid(row=0, column=1)
        self.button_4 = Button(self.frame4, text="Apply", command= lambda: self.button_handler(3)).grid(row=0, column=1)
        self.button_5 = Button(self.frame5, text="Apply", command= lambda: self.button_handler(4)).grid(row=0, column=1)


        # v = StringVar()

        self.txt_1 = Label(self.frame1, borderwidth=0,bg='gray', bd=0, width=40, height=5)
        self.txt_2 = Label(self.frame2, borderwidth=0,bg='gray', bd=0, width=40, height=5)
        self.txt_3 = Label(self.frame3, borderwidth=0,bg='gray', bd=0, width=40, height=5)
        self.txt_4 = Label(self.frame4, borderwidth=0, bg='gray', bd=0, width=40, height=5)
        self.txt_5 = Label(self.frame5, borderwidth=0,bg='gray', bd=0, width=45, height=5)
        self.txt_function = Label(self.frame_function_battery, bg='gray', bd=0, width=15, height=5)
        self.txt_mission = Label(self.frame_mission_time, bg='gray', bd=0, width=15, height=5)
        self.txt_battery = Label(self.frame_function_battery, bg='gray', bd=0, width=15, height=5)
        self.txt_time = Label(self.frame_mission_time, bg='gray', bd=0, width=15, height=5)

        self.txt_1.grid(row=1, columnspan=2, pady=0)
        self.txt_2.grid(row=1, columnspan=2, pady=0)
        self.txt_3.grid(row=1, columnspan=2, pady=0)
        self.txt_4.grid(row=1, columnspan=2, pady=0)
        self.txt_5.grid(row=1, columnspan=2, pady=0,  sticky="S")
        self.txt_function.grid(row=0, column=1, pady=0)
        self.txt_mission.grid(row=0, column=1, pady=0)
        self.txt_battery.grid(row=1, column=1, pady=0)
        self.txt_time.grid(row=1, column=1, pady=0)


        msg1 = "Verify that there are no attacks on UAV control signal"
        msg2 = "Verify that the original flight plan is uncorrupted"
        msg3 = "Check that position and function of the new UAV"
        msg4 = "Verify that the alternate flight plan is uncorrupted"
        msg5 = "Check that UAV components are uncorrupted"
        msg_function = "87%"
        msg_mission = "24%"
        msg_battery = "100%"
        msg_time = "0:00"

        # self.txt_1.insert(INSERT,msg1)
        # self.txt_2.insert(INSERT,msg2)
        # self.txt_3.insert(INSERT,msg3)
        # v.set(msg4)
        self.txt_1.configure(text=msg1)
        self.txt_2.configure(text=msg2)
        self.txt_3.configure(text=msg3)
        self.txt_4.configure(text=msg4)
        self.txt_5.configure(text=msg5)

        self.txt_function.configure(text=msg_function)
        self.txt_mission.configure(text=msg_mission)
        self.txt_battery.configure(text=msg_battery)
        self.txt_time.configure(text=msg_time)


        # self.txt_function.insert(INSERT,msg_function)
        # self.txt_mission.insert(INSERT,msg_mission)
        # self.txt_battery.insert(INSERT,msg_battery)
        # self.txt_time.insert(INSERT,msg_time)

        # self.txt_1.configure(state='disabled')
        # self.txt_2.configure(state='disabled')
        # self.txt_3.configure(state='disabled')
        # self.txt_5.configure(state='disabled')
        # # self.txt_4.configure(state='disabled')
        # self.txt_function.configure(state='disabled')
        # self.txt_mission.configure(state='disabled')
        # self.txt_battery.configure(state='disabled')
        # self.txt_time.configure(state='disabled')


  
       # # self.label_status = Label(self, text="UAV Status").grid(row=0, column=0,columnspan=2,sticky=N, pady=10)
       #  self.label_altitude = Label(self, text="Altitude:").grid(row=0, column=0, pady=5)
       #  self.label_speed = Label(self, text="Speed:").grid(row=1, column=0,pady=5)
       #  self.label_battery = Label(self, text="Battery:").grid(row=2, column=0, pady=5)
       #  self.label_waypoint = Label(self, text="Waypoint:").grid(row=3, column=0, pady=5)
       #  self.entry_altitude = Entry(self)
       #  self.entry_speed = Entry(self)
       #  self.entry_battery = Entry(self)
       #  self.entry_waypoint = Entry(self)
       #  self.entry_altitude.grid(row=0, column=1)
       #  self.entry_speed.grid(row=1, column=1)
       #  self.entry_battery.grid(row=2, column=1)
       #  self.entry_waypoint.grid(row=3, column=1)
         
       #  # self.label_sentinel_msg = Label(self, text="Sentinel Message").grid(row=0, column=2, columnspan=4, sticky=N, pady=10)

       #  self.entry_1_1 = Entry(self)
       #  self.entry_1_2 = Entry(self)
       #  self.entry_1_3 = Entry(self)
       #  self.entry_2_1 = Entry(self)
       #  self.entry_2_2 = Entry(self)
       #  self.entry_2_3 = Entry(self)
       #  self.entry_3_1 = Entry(self)
       #  self.entry_3_2 = Entry(self)
       #  self.entry_3_3 = Entry(self)
       #  self.entry_4_1 = Entry(self)
       #  self.entry_4_2 = Entry(self)
       #  self.entry_4_3 = Entry(self)
       
       #  # self.label_forceland = Label(self, text="Force Land").grid(row=0, column=2, pady=5)
       #  # self.button_1 = Button(self, text="Apply", command= lambda: self.button_handler(0)).grid(row=0, column=3)
       #  # # self.button_1_1 = Button(self, text="Refresh", command= lambda: self.button_handler(0)).grid(row=0, column=4)
       #  # # self.status_1_1 = Label(self, text="Time:").grid(row=1, column=2, pady=5)
       #  # # self.status_1_2 = Label(self, text="Control Signal:").grid(row=2, column=2, pady=5)
       #  # # self.status_1_3 = Label(self, text="other:").grid(row=3, column=2, pady=5)
       #  # # self.entry_1_1.grid(row=1, column=3)
       #  # # self.entry_1_2.grid(row=2, column=3)
       #  # # self.entry_1_3.grid(row=3, column=3)


       #  # self.label_guided = Label(self, text="Guided Mode").grid(row=0, column=5, pady=5)
       #  # self.button_2 = Button(self, text="Apply", command= lambda: self.button_handler(1)).grid(row=0, column=6)
       #  # # self.button_2_1 = Button(self, text="Refresh", command= lambda: self.button_handler(0)).grid(row=0, column=7)
       #  # # self.status_2_1 = Label(self, text="Time:").grid(row=1, column=5, pady=5)
       #  # # self.status_2_2 = Label(self, text="Control Signal:").grid(row=2, column=5, pady=5)
       #  # # self.status_2_3 = Label(self, text="other:").grid(row=3, column=5, pady=5)
       #  # # self.entry_2_1.grid(row=1, column=6)
       #  # # self.entry_2_2.grid(row=2, column=6)
       #  # # self.entry_2_3.grid(row=3, column=6)

       #  # self.label_original = Label(self, text="Original Plan").grid(row=4, column=2, pady=5)
       #  # self.button_3 = Button(self, text="Apply", command= lambda: self.button_handler(2)).grid(row=4, column=3)
       #  # # self.button_3_1 = Button(self, text="Refresh", command= lambda: self.button_handler(0)).grid(row=4, column=4)
       #  # # self.status_3_1 = Label(self, text="Time:").grid(row=5, column=2, pady=5)
       #  # # self.status_3_2 = Label(self, text="Control Signal:").grid(row=6, column=2, pady=5)
       #  # # self.status_3_3 = Label(self, text="other:").grid(row=7, column=2, pady=5)
       #  # # self.entry_3_1.grid(row=5, column=3)
       #  # # self.entry_3_2.grid(row=6, column=3)
       #  # # self.entry_3_3.grid(row=7, column=3)

       #  # self.label_alternative = Label(self, text="Alternative Plan").grid(row=4, column=5, pady=5)
       #  # self.button_4 = Button(self, text="Apply", command= lambda: self.button_handler(3)).grid(row=4, column=6)
       #  # # self.button_4_1 = Button(self, text="Refresh", command= lambda: self.button_handler(0)).grid(row=4, column=7)
       #  # # self.status_4_1 = Label(self, text="Time:").grid(row=5, column=5, pady=5)
       #  # # self.status_4_2 = Label(self, text="Control Signal:").grid(row=6, column=5, pady=5)
       #  # # self.status_4_3 = Label(self, text="other:").grid(row=7, column=5, pady=5)
       #  # # self.entry_4_1.grid(row=5, column=6)
       #  # # self.entry_4_2.grid(row=6, column=6)
       #  # # self.entry_4_3.grid(row=7, column=6)
         
       #  # # sentinel_canvas = Canvas(root, width=400, height=350, bg = '#afeeee')
        # self.sentinel_txt = Text(self)
        # self.sentinel_txt.grid(row=8, column=0, columnspan=4, rowspan=5, sticky=S, pady=3)



       #  # # sentinel_canvas.create_text(100,10,fill="darkblue",font="Times 20 italic bold",
       #  # #                         text="1")

    def read_parameters(self):
        missionlist=[]
        with open("scripts/parameters.txt") as f:
            for i, line in enumerate(f):
                if i==0:
                    if not line.startswith('function battery mission flight_time'):
                        raise Exception('File is not supported WP version')
                else:
                    linearray=line.split('\t')
                    self.function=str(linearray[0])
                    self.battery=str(linearray[1])
                    self.mission=str(linearray[2])
                    self.flight_time_sec=round(float(linearray[3]),2)
                    # ln_param2=float(linearray[5])
                    # ln_param3=float(linearray[6])
                    # ln_param4=float(linearray[7])
                    # ln_param5=float(linearray[8])
                    # ln_param6=float(linearray[9])
                    # ln_param7=float(linearray[10])
                    # ln_autocontinue=int(linearray[11].strip())
                    # pdb.set_trace()
        #             cmd = Command( 0, 0, 0, ln_frame, ln_command, ln_currentwp, ln_autocontinue, ln_param1, ln_param2, ln_param3, ln_param4, ln_param5, ln_param6, ln_param7)
        #             missionlist.append(cmd)
        # return missionlist

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()


# root = Tk()
# app = msg_window2(master=root)
# app.button_handler2()

# app.mainloop()
# root.destroy()