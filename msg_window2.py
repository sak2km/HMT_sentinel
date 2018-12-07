from Tkinter import *
import tkinter as tk
from tkinter import ttk
import tkMessageBox
import datetime
import time
import pdb

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
    # def popupmsg(self, msg):
    #     # popup = tk.Tk()
    #     # popup.wm_title("!")
    #     # label = ttk.Label(popup, text=msg, font='Helvetica 16 bold')
    #     # label.pack(side="top", fill="x", pady=10)
    #     # B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    #     # B1.pack()
    #     # popup.mainloop()
    #     t = tk.Toplevel(self)
    #     t.wm_title("Warning!")
    #     l = tk.Label(t, text=msg)
    #     l.pack(side="top", fill="both", expand=True, padx=100, pady=100)

    def update_reconfig_msg(self):
        self.txt_3.configure(text="Control system reconfigured. Trajectories updated automatically.")
        # make it disappear after 3 sec
        self.after(5000, self.hide_reconfig_msg)
        
    def hide_reconfig_msg(self):
        self.txt_3.configure(text='',fg="red", font='Helvetica 14')


    def update_response_option(self):
      # Popup warning message an attack has occured
      if tkMessageBox.showinfo("Message", 'Some of available responses options will be provided.\n\nVerify these options if necessary.'):
        print('Some of available responses options will be provided.\n\nVerify these options if necessary.')
        time_second_popup = str(self.flight_time[0:10])
        # notify Sentinel that the popup window has opened.
        with open("scripts/popup_log.txt", 'w+') as file_:
          output = "counter\tpopup_opened\ttime_clicked1\ttime_clicked2\n"
          output += "%s\t%s\t%s\t%s\n" % (self.counter, 1, self.time_first_popup, time_second_popup)
          file_.write(output)




      if self.recovery_options == 'NA':
        # self.label_statistics.lower(self.frame2)
        self.label_statistics.configure(text='Response options:')
        self.txt_2.configure(text='Not available.',fg="#414141", font='Helvetica 14')
      else:
        self.label_statistics.configure(text='Response options:')
        # print(self.recovery_options)
        self.txt_2.configure(text=self.recovery_options, fg="#414141", font='Helvetica 14')

    def read_attack_popup(self):
      # if popup_opened == 1, attack window have opened
      popup_opened = 0
      with open("scripts/popup_log.txt") as f:
        for i, line in enumerate(f):
          if i==0:
            if not line.startswith('counter\tpopup_opened\ttime_clicked1\ttime_clicked2'):
              raise Exception('File is not supported WP version')
          else:
            linearray=line.split('\t')
            counter_log=int(linearray[0]) # button counter from log file
            popup_opened=int(linearray[1])
      if popup_opened == 1:
        return True
      else:
        return False

    def entry_update(self, vehicle=None):
        # print("hi")
        # entry_altitude.delete(1.0, END)
        # self.alt = vehicle.location.global_relative_frame.alt
        self.read_parameters()
        # Whther attack popup have been opened
        popup_opened = self.read_attack_popup()


        # self.txt_function.configure(text=self.function)
        self.txt_mission.configure(text=self.mission)
        if float(self.battery) > 70:
          self.txt_battery = Label(self.frame_time_battery, fg='#00ff00',bg='#001a33', width=15, height=5)
          self.txt_battery.grid(row=0, column=1, pady=0)
        elif float(self.battery) <= 70:
          self.txt_battery = Label(self.frame_time_battery, fg='#ffff00',bg='#001a33', width=15, height=5)
          self.txt_battery.grid(row=0, column=1, pady=0)
        elif float(self.battery) <= 50:
          self.txt_battery = Label(self.frame_time_battery, fg='#ffa500',bg='#001a33', width=15, height=5)
          self.txt_battery.grid(row=0, column=1, pady=0)
        elif float(self.battery) <= 20:
          self.txt_battery = Label(self.frame_time_battery, fg='#ff0000',bg='#001a33', width=15, height=5)
          self.txt_battery.grid(row=0, column=1, pady=0)


        self.txt_battery.configure(text=self.battery, font='Helvetica 16 bold')
        self.txt_1.configure(text=self.damage_info)
        self.flight_time = str(datetime.timedelta(seconds=self.flight_time_sec))
        self.txt_time.configure(text=self.flight_time[0:10], fg='#ffffff',)

        # print("self.attacked_popup_flag: %s, self.attacked: %s,  self.attacked_popup: %s"%(self.attacked_popup_flag, self.attacked, self.attacked_popup))

        if not self.attacked:
            self.time_first_popup = '0'
            self.time_second_popup = '0'


        if self.attacked and self.attacked_popup and not popup_opened:
          # self.attacked_popup_flag and
          if self.damage_type == 'nav':
            self.label_forceland.configure(text="Damage on: Navigation module (Drone A).", font='Helvetica 16 bold')
          elif self.damage_type == 'guidance':
            self.label_forceland.configure(text="Damage on: Guidance module (Drone A).", font='Helvetica 16 bold')
          elif self.damage_type == 'other':
            self.label_forceland.configure(text="Damage on: Other modules (Drone A).", font='Helvetica 16 bold')
          elif self.damage_type == 'glabal':
            self.label_forceland.configure(text="Damage on: Navigation, Guidance, and other modules (Drone A).", font='Helvetica 16 bold')
          elif self.damage_type == 'local':
            self.label_forceland.configure(text="Damage on: Navigation module (Drone A).", font='Helvetica 16 bold')

          if self.history_stat == 'NA':
            # self.label_statistics.lower(self.frame2)
            self.label_statistics.configure(text='')
            self.txt_2.configure(text='')
          else:
            history_stat_str = self.history_stat.replace(".", ".\n")
            self.label_statistics.configure(text='Previous Statistics:')
            self.txt_2.configure(text=history_stat_str,fg="#414141", font='Helvetica 14')

          # Popup warning message an attack has occured
          if tkMessageBox.showinfo("Message", "A Cyber attack detected!!!"):
            print('Attack message delivered.')
            print('popup open recorded.')

            self.time_first_popup = str(self.flight_time[0:10])
            # notify Sentinel that the popup window has opened.
            with open("scripts/popup_log.txt", 'w+') as file_:
              output = "counter\tpopup_opened\ttime_clicked1\ttime_clicked2\n"
              output += "%s\t%s\t%s\t%s\n" % (self.counter, 1, self.time_first_popup, self.time_second_popup)
              file_.write(output)
            self.attacked_popup = False

          # self.popupmsg("A Cyber attack detected!!!")



          # top = Toplevel()
          # top.title('Welcome')
          # Message(top, text='hiiii', padx=20, pady=20).pack()
          # top.after('20', top.destroy)




          # tkMessageBox.showinfo("Message", "A Cyber attack detected!!!")

          self.after(5000, self.update_reconfig_msg)

          self.after(10000, self.update_response_option)

          

        elif not self.attacked and not self.attacked_popup:
          # No attack
          self.label_forceland.configure(text="Damage on: ", font='Helvetica 16 bold')
          self.label_statistics.configure(text='Previous Statistics:')
          self.txt_2.configure(text="Not available",fg="#414141", font='Helvetica 14')



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
        self.attacked_popup = False
        self.attacked_popup_flag = True
        self.time_first_popup = '0'
        self.time_second_popup = '0'

        # create all of the main containers
        self.frame1 = Frame(self, bg='#001a33', highlightbackground="#001a33", highlightthickness=5, width=55, height=50, pady=5)
        self.frame2 = Frame(self, bg='#001a33', highlightbackground="#001a33", highlightthickness=5, width=55, height=150, pady=5)
        self.frame3 = Frame(self, bg='#00274d', highlightbackground="#00274d", highlightthickness=5, width=55, height=50, pady=5)
        # self.frame3 = Frame(self, bg='gray', highlightbackground="gray90", highlightthickness=5, width=300, height=150, pady=5)
        # self.frame4 = Frame(self, bg='gray', highlightbackground="gray90", highlightthickness=5, width=300, height=150, pady=5)
        # self.frame5 = Frame(self, bg='gray', highlightbackground="gray90", highlightthickness=5, width=300, height=150, pady=5)
        # self.frame6 = Frame(self, bg='gray90', highlightbackground="gray90", highlightthickness=5,  width=300, height=150, pady=5)
        self.frame_time_battery = Frame(self, bg='#001a33', width=55, height=10)
        self.frame_mission = Frame(self, bg='#001a33', width=55, height=10 )
        # self.frame_battery = Frame(self, bg='white', width=300, height=10, pady=3)
        # self.frame_time = Frame(self, bg='white', width=300, height=10, pady=3)

        # # layout all of the main containers
        # self.grid_rowconfigure(1, weight=1)
        # self.grid_columnconfigure(0, weight=1)

        self.frame1.grid(row=0, column=0, columnspan=2,rowspan=1)
        self.frame2.grid(row=1, column=0, columnspan=2, rowspan=2)
        self.frame3.grid(row=3, column=0, columnspan=2, rowspan=1)
        # self.frame3.grid(row=1, column=0)
        # self.frame4.grid(row=1, column=1)
        # self.frame5.grid(row=2, column=0)
        # self.frame6.grid(row=2, column=1)
        self.frame_time_battery.grid(row=4, column=0)
        self.frame_mission.grid(row=4, column=1)
        # self.frame_battery.grid(row=4, column=0)
        # self.frame_time.grid(row=4, column=1)


        self.label_forceland = Label(self.frame1,anchor=W,justify="left", fg='#ffffff',bg='#001a33',width=40,text="Damage on: ", font='Helvetica 16 bold')
        self.label_forceland.grid(row=0, column=0)
        self.label_statistics = Label(self.frame2, anchor=W, width=40, justify="left", fg='#ffffff',bg='#001a33',text="Previously Reported Cyber-attacks:", font='Helvetica 21')
        self.label_statistics.grid(row=0, column=0)
        # self.label_original = Label(self.frame3, bg='gray',text="Original Plan", font='Helvetica 14 bold').grid(row=0, column=0)
        # self.label_alternative = Label(self.frame4, bg='gray',text="Alternative Plan", font='Helvetica 14 bold').grid(row=0, column=0)
        # self.label_home = Label(self.frame5, bg='gray',text="Return to Base", font='Helvetica 14 bold').grid(row=0, column=0)
        # self.label_function = Label(self.frame_time_battery, bg='gray', text="Function", font='Helvetica 14 bold').grid(row=0, column=0)
        self.label_mission = Label(self.frame_mission, bg='#001a33', text="Mission Completion", fg='#ffffff',font='Helvetica 14 bold').grid(row=0, column=0)
        self.label_battery = Label(self.frame_time_battery, bg='#001a33', text="Battery", fg='#ffffff', font='Helvetica 14 bold').grid(row=0, column=0)
        self.label_time = Label(self.frame_time_battery, bg='#001a33', text="Flight Time", fg='#ffffff',font='Helvetica 14 bold').grid(row=1, column=0)

        # ttk.Style().configure("RB.TButton", foreground='red', background='red')
        # self.button_1 = ttk.Button(self.frame1, text="Applyyy", style="RB.TButton", command= lambda: self.button_handler(0))
        # self.button_1.grid(row=0, column=1)
        # self.button_1 = Button(self.frame1, text="Apply", command= lambda: self.button_handler(0)).grid(row=0, column=1)
        # self.button_2 = Button(self.frame2, text="Apply", command= lambda: self.button_handler(1)).grid(row=0, column=1)
        # self.button_3 = Button(self.frame3, text="Apply", command= lambda: self.button_handler(2)).grid(row=0, column=1)
        # self.button_4 = Button(self.frame4, text="Apply", command= lambda: self.button_handler(3)).grid(row=0, column=1)
        # self.button_5 = Button(self.frame5, text="Apply", command= lambda: self.button_handler(4)).grid(row=0, column=1)


        # v = StringVar()

        self.txt_1 = Label(self.frame1, anchor=W, justify="left", borderwidth=0,bg='#001a33',fg='#ffffff',font='Helvetica 14 bold', bd=0, width=45, height=2)
        self.txt_2 = Label(self.frame2, anchor=W, justify="left", borderwidth=0,bg='#001a33', bd=0, width=45, height=7,fg="#ffffff", font='Helvetica 14')
        self.txt_3 = Label(self.frame3, anchor=W, justify="left", borderwidth=0,bg='#00274d', bd=0, width=55,fg="red", font='Helvetica 14')
        # self.txt_3 = Label(self.frame3, borderwidth=0,bg='gray', bd=0, width=40, height=5)
        # self.txt_4 = Label(self.frame4, borderwidth=0, bg='gray', bd=0, width=40, height=5)
        # self.txt_5 = Label(self.frame5, borderwidth=0,bg='gray', bd=0, width=45, height=5)
        # self.txt_function = Label(self.frame_function_battery, bg='gray', bd=0, width=15, height=5)
        self.txt_mission = Label(self.frame_mission, bg='#001a33', fg='#ffffff',bd=0, width=15, height=5)
        self.txt_battery = Label(self.frame_time_battery, bg='#001a33',bd=0, width=15, height=5)
        self.txt_time = Label(self.frame_time_battery, bg='#001a33', fg='#ffffff',bd=0, width=15, height=5)

        self.txt_1.grid(row=1, columnspan=2, pady=0)
        self.txt_2.grid(row=1, columnspan=2, pady=0)
        self.txt_3.grid(row=0, columnspan=2, pady=0)
        # self.txt_3.grid(row=1, columnspan=2, pady=0)
        # self.txt_4.grid(row=1, columnspan=2, pady=0)
        # self.txt_5.grid(row=1, columnspan=2, pady=0,  sticky="S")
        # self.txt_function.grid(row=0, column=1, pady=0)
        self.txt_mission.grid(row=0, column=1, pady=0)
        self.txt_battery.grid(row=0, column=1, pady=0)
        self.txt_time.grid(row=1, column=1, pady=0)


        msg1 = "Damage on navigation module (Drone A)."
        msg2 = "Monitoring the System..."
        # msg3 = "Check that position and function of the new UAV"
        # msg4 = "Verify that the alternate flight plan is uncorrupted"
        # msg5 = "Check that UAV components are uncorrupted"
        # msg_function = "87%"
        msg_mission = "24%"
        msg_battery = "100%"
        msg_time = "0:00"

        # self.txt_1.insert(INSERT,msg1)
        # self.txt_2.insert(INSERT,msg2)
        # self.txt_3.insert(INSERT,msg3)
        # v.set(msg4)
        self.txt_1.configure(text=msg1)
        self.txt_2.configure(text=msg2, fg='#ffffff',)
        # self.txt_3.configure(text="Control system reconfigured. Trajectories updated automatically.")
        # self.txt_3.configure(text=msg3)
        # self.txt_4.configure(text=msg4)
        # self.txt_5.configure(text=msg5)

        # self.txt_function.configure(text=msg_function)
        self.txt_mission.configure(text=msg_mission)
        self.txt_battery.configure(text=msg_battery)
        self.txt_time.configure(text=msg_time)



        # notify Sentinel that the popup window has not been opend. 
        # Default setting
        # with open("scripts/popup_log.txt", 'w+') as file_:
        #   output = "counter popup_opened\n"
        #   output += "%s\t%s\n" % (self.counter, 0)
        #   file_.write(output)

        # output='function battery mission flight_time attacked_popup attacked damage_type history_stat \n'
        # output+="%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % ( "83%", 100, 100 ,0, False, False, 'global', 'NA')
        # with open("scripts/parameters.txt", 'w') as file_:
        #     # print " Write mission to file"
        #     file_.write(output)


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
        # missionlist=[]
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
                    attacked_pop_str = str(linearray[4])
                    attacked_str = str(linearray[5])
                    self.damage_type = str(linearray[6])
                    self.history_stat=str(linearray[7])
                    self.damage_info = ''

                    if attacked_pop_str == 'True':
                      self.attacked_popup = True
                    elif attacked_str == 'False':
                      self.attacked_popup = False

                    if attacked_str == 'True':
                      self.attacked = True
                    elif attacked_str == 'False':
                      self.attacked = False

        with open("scripts/response_option.txt") as f:
            for i, line in enumerate(f):
                if i==0:
                    if not line.startswith('response_option'):
                        raise Exception('File is not supported WP version')
                else:
                    self.recovery_options=line.replace("\t", "\n")

                      # self.label.lower(self.frame)
                    # print(self.attacked)
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