from __future__ import print_function

from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, Command
import time, math, pdb, random
from pymavlink import mavutil
import threading
import os

#Set up option parsing to get connection string
import argparse 
import time


class Sentinel():
    def __init__(self):
        parser = argparse.ArgumentParser(description='Demonstrates basic mission operations.')
        parser.add_argument('--connect', 
                           help="vehicle connection target string. If not specified, SITL automatically started and used.")
        parser.add_argument('--attack_waypoint', 
                           help="the waypoint number cyber attack will be conducted",
                           default='1000')
        parser.add_argument('--attack_time', 
                           help="time (in seconds) cyber attack will be conducted",
                           default='100000')
        parser.add_argument('--attack_altitude', 
                           help="altitude cyber attack will be conducted",
                           default='100000')
        parser.add_argument('--attack_coordinate', 
                           help="coordinate cyber attack will be conducted",
                           default='100000,10000')
        args = parser.parse_args()

        self.connection_string = args.connect
        self.attack_waypoint = int(args.attack_waypoint)
        self.attack_time = int(args.attack_time)
        self.attack_altitude = int(args.attack_altitude)
        self.attack_coordinate = str(args.attack_coordinate).split(',')

        self.sitl = None

        self.original_mission_filename = 'scripts/original_mission.txt'
        self.original_mission_filename_save = 'scripts/original_mission.txt'
        self.alternate_mission_filename = 'scripts/alternate_mission.txt'


        #Start SITL if no connection string specified
        if not self.connection_string:
            import dronekit_sitl
            self.sitl = dronekit_sitl.start_default()
            self.connection_string = self.sitl.connection_string()


        # Connect to the Vehicle
        print('Connecting to vehicle on: %s' % self.connection_string)
        self.vehicle = connect(self.connection_string, wait_ready=True)
        self.button_counter = "0" # iteration in which last button clicked occured.
        self.flag_param_save = True
        self.sentinel_msg = "sentinel message 0"
        self.attacked = False

    def get_location_metres(self, original_location, dNorth, dEast):
        """
        Returns a LocationGlobal object containing the latitude/longitude `dNorth` and `dEast` metres from the 
        specified `original_location`. The returned Location has the same `alt` value
        as `original_location`.
        The function is useful when you want to move the vehicle around specifying locations relative to 
        the current vehicle position.
        The algorithm is relatively accurate over small distances (10m within 1km) except close to the poles.
        For more information see:
        http://gis.stackexchange.com/questions/2951/algorithm-for-offsetting-a-latitude-longitude-by-some-amount-of-meters
        """
        earth_radius=6378137.0 #Radius of "spherical" earth
        #Coordinate offsets in radians
        dLat = dNorth/earth_radius
        dLon = dEast/(earth_radius*math.cos(math.pi*original_location.lat/180))

        #New position in decimal degrees
        newlat = original_location.lat + (dLat * 180/math.pi)
        newlon = original_location.lon + (dLon * 180/math.pi)
        return LocationGlobal(newlat, newlon,original_location.alt)

    def get_distance_metres(self, aLocation1, aLocation2):
        """
        Returns the ground distance in metres between two LocationGlobal objects.
        This method is an approximation, and will not be accurate over large distances and close to the 
        earth's poles. It comes from the ArduPilot test code: 
        https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
        """
        dlat = aLocation2.lat - aLocation1.lat
        dlong = aLocation2.lon - aLocation1.lon
        return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5

    def distance_to_current_waypoint(self):
        """
        Gets distance in metres to the current waypoint. 
        It returns None for the first waypoint (Home location).
        """
        nextwaypoint = self.vehicle.commands.next
        if nextwaypoint==0 or nextwaypoint > len(self.vehicle.commands)-1:
            return None
        missionitem=self.vehicle.commands[nextwaypoint-1] # commands are zero indexed
        lat = missionitem.x
        lon = missionitem.y
        alt = missionitem.z
        targetWaypointLocation = LocationGlobalRelative(lat,lon,alt)
        distancetopoint = self.get_distance_metres(self.vehicle.location.global_frame, targetWaypointLocation)
        return distancetopoint

    def distance_to_home(self):
        """
        Gets distance in metres to the current waypoint. 
        It returns None for the first waypoint (Home location).
        """
        home = self.vehicle.commands[0]
        targetWaypointLocation = LocationGlobalRelative(home.x,home.y,home.z)
        distancetopoint = self.get_distance_metres(self.vehicle.location.global_frame, targetWaypointLocation)
        return distancetopoint

    def download_mission(self):
        """
        Download the current mission from the vehicle.
        """    
        missionlist=[]
        cmd_list = self.vehicle.commands
        cmd_list.download()
        cmd_list.wait_ready()
        for cmd in cmd_list:
            missionlist.append(cmd)
        return missionlist

    def adds_square_mission(self, aLocation, aSize):
        """
        Adds a takeoff command and four waypoint commands to the current mission. 
        The waypoints are positioned to form a square of side length 2*aSize around the specified LocationGlobal (aLocation).
        The function assumes vehicle.commands matches the vehicle mission state 
        (you must have called download at least once in the session and after clearing the mission)
        """ 
        cmds = self.vehicle.commands

        print(" Clear any existing commands")
        cmds.clear() 
        
        print(" Define/add new commands.")
        # Add new commands. The meaning/order of the parameters is documented in the Command class. 
         
        #Add MAV_CMD_NAV_TAKEOFF command. This is ignored if the vehicle is already in the air.
        cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 0, 10))

        #Define the four MAV_CMD_NAV_WAYPOINT locations and add the commands
        point1 = self.get_location_metres(aLocation, aSize, -aSize)
        point2 = self.get_location_metres(aLocation, aSize, aSize)
        point3 = self.get_location_metres(aLocation, -aSize, aSize)
        point4 = self.get_location_metres(aLocation, -aSize, -aSize)
        cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, point1.lat, point1.lon, 11))
        cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, point2.lat, point2.lon, 12))
        cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, point3.lat, point3.lon, 13))
        cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, point4.lat, point4.lon, 14))
        #add dummy waypoint "5" at point 4 (lets us know when have reached destination)
        cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, point4.lat, point4.lon, 14))    

        print(" Upload new commands to vehicle")
        cmds.upload()

    def adds_triangle_mission(self, aLocation, aSize):
        """
        Adds a takeoff command and four waypoint commands to the current mission. 
        The waypoints are positioned to form a square of side length 2*aSize around the specified LocationGlobal (aLocation).
        The function assumes vehicle.commands matches the vehicle mission state 
        (you must have called download at least once in the session and after clearing the mission)
        """ 
        cmds = self.vehicle.commands

        print(" Clear any existing commands")
        cmds.clear() 
        
        print(" Define/add new commands.")
        # Add new commands. The meaning/order of the parameters is documented in the Command class. 
         
        #Add MAV_CMD_NAV_TAKEOFF command. This is ignored if the vehicle is already in the air.
        cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 0, 10))

        #Define the four MAV_CMD_NAV_WAYPOINT locations and add the commands
        point1 = self.get_location_metres(aLocation, aSize, -aSize)
        point2 = self.get_location_metres(aLocation, aSize, aSize)
        point3 = self.get_location_metres(aLocation, -aSize, aSize)
        # point4 = get_location_metres(aLocation, -aSize, -aSize)
        cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, point1.lat, point1.lon, 11))
        cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, point2.lat, point2.lon, 12))
        cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, point3.lat, point3.lon, 13))
        # cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, point4.lat, point4.lon, 14))

        self.missions.append(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, point1.lat, point1.lon, 11))
        self.missions.append(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, point2.lat, point2.lon, 12))
        self.missions.append(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, point3.lat, point3.lon, 13))

        print(" Upload new commands to vehicle")
        cmds.upload()

    def arm_and_takeoff(self, aTargetAltitude):
        """
        Arms vehicle and fly to aTargetAltitude.
        """
        print("Basic pre-arm checks")
        # Don't let the user try to arm until autopilot is ready
        while not self.vehicle.is_armable:
            print(" Waiting for vehicle to initialise...")
            time.sleep(5)

            
        print("Arming motors")
        # Copter should arm in GUIDED mode
        self.vehicle.mode = VehicleMode("GUIDED")
        self.vehicle.armed = True

        while not self.vehicle.armed:      
            print(" Waiting for arming...")
            time.sleep(5)

        print("Taking off!")
        self.vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

        # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command 
        #  after Vehicle.simple_takeoff will execute immediately).
        # pdb.set_trace()
        self.first_save = True
        self.trigger_param_save()
        counter = 0
        while True:
            print(" Altitude: ", self.vehicle.location.global_relative_frame.alt)
            counter += 1      
            if self.vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95: #Trigger just below target alt.
                print("Reached target altitude")
                break
            if counter > 10:
                print("break due to counter")
                break
            time.sleep(5)

    def add_new_mission(self, current_wp, hacked_waypoint):
        # Get the set of commands from the vehicle        
        print('!!!!!!!!!!!CYBER ATTACK !!! New waypoint is Added')

        cmds = self.vehicle.commands
        cmds.download()
        cmds.wait_ready()

        # Save the vehicle commands to a list
        missionlist=[]
        for count, cmd in enumerate(self.missions):
            missionlist.append(cmd)

        # Modify the mission as needed. For example, here we change the
        # first waypoint into a MAV_CMD_NAV_TAKEOFF command.
        # missionlist[0].command = mavutil.mavlink.MAV_CMD_NAV_TAKEOFF

        # Clear the current mission (command is sent when we call upload())
        cmds.clear()
        # pdb.set_trace()

        #Write the modified mission and flush to the vehicle
        for count,cmd in enumerate(missionlist):
            # pdb.set_trace()
            cmds.add(cmd)
            if count == current_wp-1:
                cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, hacked_waypoint.lat, hacked_waypoint.lon, 14))
        
         
        cmds.upload()
        cmds.next = current_wp+1
        # mode guided to activate? new waypoints:
        # https://github.com/dronekit/dronekit-python/issues/201
        self.vehicle.mode = VehicleMode("GUIDED")
        self.vehicle.mode = VehicleMode("AUTO")
        self.vehicle.armed = True

    def save_mission(self, aFileName):
        """
        Save a mission in the Waypoint file format 
        (http://qgroundcontrol.org/mavlink/waypoint_protocol#waypoint_file_format).
        """
        # print "\nSave mission from Vehicle to file: %s" % export_mission_filename    
        #Download mission from vehicle
        missionlist = self.download_mission()

        # pdb.set_trace()
        #Add file-format information
        output='QGC WPL 110\n'
        #Add home location as 0th waypoint
        home = self.vehicle.home_location
        output+="%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (0,1,0,16,0,0,0,0,35.9835973,-95.8742309,0,1)

        #Add commands
        for cmd in missionlist:
            commandline="%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (cmd.seq,cmd.current,cmd.frame,cmd.command,cmd.param1,cmd.param2,cmd.param3,cmd.param4,cmd.x,cmd.y,cmd.z,cmd.autocontinue)
            output+=commandline
        with open(aFileName, 'w') as file_:
            # print " Write mission to file"
            file_.write(output)

    def readmission(self,aFileName):
        """
        Load a mission from a file into a list. The mission definition is in the Waypoint file
        format (http://qgroundcontrol.org/mavlink/waypoint_protocol#waypoint_file_format).

        This function is used by upload_mission().
        """
        print ("\nReading mission from file: %s" % aFileName)
        cmds =  self.vehicle.commands
        missionlist=[]
        with open(aFileName) as f:
            for i, line in enumerate(f):
                if i==0:
                    if not line.startswith('QGC WPL 110'):
                        raise Exception('File is not supported WP version')
                else:
                    linearray=line.split('\t')
                    ln_index=int(linearray[0])
                    ln_currentwp=int(linearray[1])
                    ln_frame=int(linearray[2])
                    ln_command=int(linearray[3])
                    ln_param1=float(linearray[4])
                    ln_param2=float(linearray[5])
                    ln_param3=float(linearray[6])
                    ln_param4=float(linearray[7])
                    ln_param5=float(linearray[8])
                    ln_param6=float(linearray[9])
                    ln_param7=float(linearray[10])
                    ln_autocontinue=int(linearray[11].strip())
                    # pdb.set_trace()
                    cmd = Command( 0, 0, 0, ln_frame, ln_command, ln_currentwp, ln_autocontinue, ln_param1, ln_param2, ln_param3, ln_param4, ln_param5, ln_param6, ln_param7)
                    missionlist.append(cmd)
        return missionlist


    def upload_mission(self,aFileName,onlyFirst=False):
        """
        Upload a mission from a file. 
        """
        #Read mission from file
        missionlist = self.readmission(aFileName)
        
        # print "\nUpload mission from a file: %s" % import_mission_filename
        #Clear existing mission from vehicle
        # print ' Clear mission'
        cmds =  self.vehicle.commands
        cmds.download()
        cmds.wait_ready()
        cmds.clear()
        #Add new mission to vehicle
        for i, command in enumerate(missionlist):
            if not onlyFirst or i == 0:
                cmds.add(command)
        # print ' Upload mission'
        self.vehicle.commands.upload()

        return missionlist

    def save_parameters(self,aFileName):

        output='function battery mission flight_time\n'
        #Add home location as 0th waypoint
        # home = vehicle.home_location
        time_elpased = round(time.time() - self.time_start,2)


        # self.txt_function.configure(text=self.function)
        # self.txt_mission.configure(text=self.mission)
        # self.txt_battery.configure(text=self.battery)
        # self.txt_time.configure(text=self.flight_time)

        function =  "83%"
        # speed =  self.vehicle.airspeed
        waypoint =  self.vehicle.commands.next
        num_waypoints = len(self.vehicle.commands)
        if num_waypoints > 0:
            mission = str(round(float(waypoint)/num_waypoints * 100,2)) + " %"
        else :
            mission = "Nan"
        # print(self.vehicle.battery.level)
        battery =  str(round(self.vehicle.battery.level)) + " %"

        output+="%s\t%s\t%s\t%s\n" % (function, battery, mission ,time_elpased)

        with open(aFileName, 'w') as file_:
            # print " Write mission to file"
            file_.write(output)



        header = 'time lon lat speed battery waypoint attack\n'

        lon = self.vehicle.location.global_relative_frame.lon
        lat = self.vehicle.location.global_relative_frame.lat
        speed =  self.vehicle.airspeed
        # battery =  self.vehicle.battery.level
        # waypoint =  self.vehicle.commands.next

        output = "%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (time_elpased,lon,lat,speed,battery,waypoint,self.attacked)

        # print(os.stat("trajectory_log.txt").st_size)

        # if os.stat("trajectory_log.txt").st_size == 0: 
        #     with open('trajectory_log.txt', 'w') as file_:
        #         file_.write(header)
        # else:
        #     with open('trajectory_log.txt', 'w+') as file_:
        #         for i, line in enumerate(file_):
        #             if i==0 and not line.startswith('time lon lat speed battery waypoint attack'):
        #                 pdb.set_trace()
        #                 file_.write(header)
        #             break
        # with open("scripts/trajectory_log.txt", "w+") as file_:
        #     file_.write(header)

        # with open('scripts/trajectory_log.txt', 'w+') as file_:
        #     for i, line in enumerate(file_):
        #         if i==0 and not line.startswith('time lon lat speed battery waypoint attack'):
        #             pdb.set_trace()
        #             file_.write(header)
        #             break
        #         break
        if self.first_save:
            with open('scripts/trajectory_log.txt', 'w+') as file_:
                file_.write(header)

        self.first_save = False


        with open("scripts/trajectory_log.txt", "a+") as file_:
            file_.write(output)


    def process_buttons(self,button_num):
        if button_num == 0:
            self.sentinel_msg = "Button 1: <Force-land> triggered at iteration %s!" %(self.button_counter)
            print(self.sentinel_msg)
            self.vehicle.mode = VehicleMode("LAND")

            # print("Close vehicle object")
            # # timer_vehicle_close = threading.Timer(3.0,  self.vehicle.close()) 
            # self.vehicle.close()
            # if self.sitl is not None:
            #     self.sitl.stop()
            return

        if button_num == 1:
            print("Button 2: <Guided Mode> triggered!")
            cmds = self.vehicle.commands
            cmds.download()
            cmds.wait_ready()
            cmds.clear()
            self.vehicle.commands.upload()
            self.vehicle.commands.next = 0
            self.vehicle.mode = VehicleMode("GUIDED")
            # self.vehicle.mode = VehicleMode("AUTO")
            self.vehicle.armed = True
            return

        if button_num == 2:
            # print("Button 1: <Original Plan> triggered!")

            self.sentinel_msg = "Button 3: <Original Plan> triggered at iteration %s!" %(self.button_counter)
            print(self.sentinel_msg)

            # Upload initial missionlist
            missionlist = self.upload_mission(self.original_mission_filename)
            cmds = self.vehicle.commands
            cmds.download()
            cmds.wait_ready()
            cmds.clear()

            #Add new mission to vehicle
            for command in missionlist:
                cmds.add(command)
            # print ' Upload mission'
            self.vehicle.commands.upload()
            self.vehicle.mode = VehicleMode("GUIDED")
            self.vehicle.mode = VehicleMode("AUTO")
            self.vehicle.armed = True
            # self.vehicle.commands.next = self.vehicle.commands.next-1
            return

        if button_num == 3:
            self.sentinel_msg = "Button 4: <Alternate Plan> triggered at iteration %s!" %(self.button_counter)
            print(self.sentinel_msg)

            missionlist = self.upload_mission(self.alternate_mission_filename)
            cmds = self.vehicle.commands
            cmds.download()
            cmds.wait_ready()
            cmds.clear()

            #Add new mission to vehicle
            for command in missionlist:
                cmds.add(command)
            # print ' Upload mission'
            self.vehicle.commands.upload()
            self.vehicle.mode = VehicleMode("GUIDED")
            self.vehicle.mode = VehicleMode("AUTO")
            self.vehicle.armed = True
            self.vehicle.commands.next = self.vehicle.commands.next-1
            return
        if button_num == 4:
            self.sentinel_msg = "Button 5: <Return Home> triggered at iteration %s!" %(self.button_counter)
            print(self.sentinel_msg)
            # cmds = self.vehicle.commands
            # cmds.download()
            # cmds.wait_ready()
            # cmds.clear()
            self.vehicle.mode = VehicleMode("RTL")
            self.toHome=True


            # missionlist = self.upload_mission(self.original_mission_filename, True)
            # cmds = self.vehicle.commands
            # cmds.download()
            # cmds.wait_ready()
            # cmds.clear()
            # self.vehicle.commands.next = 0
            # #Add new mission to vehicle
            # for command in missionlist:
            #     cmds.add(command)
            # print(len(missionlist))
            # # print ' Upload mission'
            # self.vehicle.commands.upload()
            # self.vehicle.mode = VehicleMode("GUIDED")
            # self.vehicle.mode = VehicleMode("AUTO")
            # self.vehicle.mode = VehicleMode("RTL")
            # self.vehicle.armed = True



            # #Add new mission to vehicle
            # # cmds.add(self.home_location)

            # # self.vehicle.mode = VehicleMode("RTL")
            # # self.vehicle.commands.next = 0

            # self.vehicle.close()
            # if self.sitl is not None:
            #     self.sitl.stop()


            # #Add new mission to vehicle
            # cmds.add(self.home_location)
            # # # print ' Upload mission'
            # self.vehicle.commands.upload()
            # self.vehicle.mode = VehicleMode("GUIDED")
            # self.vehicle.mode = VehicleMode("AUTO")
            # self.vehicle.armed = True
            # self.vehicle.commands.next = self.vehicle.commands.next-1
            return



    def read_button_log(self,aFileName):
        with open(aFileName) as f:
            for i, line in enumerate(f):
                if i==0:
                    if not line.startswith('counter button_clicked'):
                        raise Exception('File is not supported WP version')
                else:
                    linearray=line.split('\t')
                    counter_log=int(linearray[0]) # button counter from log file
                    button_num=int(linearray[1])
            if counter_log > self.button_counter: # counter from log file > counter from sentinel
                print("New button click %s detected"%(button_num))
                # Update sentinel's button counter
                self.button_counter = counter_log
                self.process_buttons(button_num)
            return counter_log


    def trigger_param_save(self):
        timer = threading.Timer(0.5, self.trigger_param_save)
        if self.flag_param_save:
            timer.start()
            # print(flag_param_save)
            # print("!!!!!timer started!!")
            self.save_parameters("scripts/parameters.txt")
            self.button_counter = self.read_button_log("scripts/button_log.txt")
        else:
            print("!!!!time to close param save!!")
            timer.cancel()


    def distance_to_coordinate(self, lon, lat):
        """
        Gets distance in metres to the current waypoint. 
        It returns None for the first waypoint (Home location).
        """
        nextwaypoint = self.vehicle.commands.next
        if nextwaypoint==0:
            return None
        missionitem=self.vehicle.commands[nextwaypoint-1] # commands are zero indexed
        lat = missionitem.x
        lon = missionitem.y
        alt = missionitem.z
        targetWaypointLocation = LocationGlobalRelative(lat,lon,alt)
        distancetopoint = self.get_distance_metres(self.vehicle.location.global_frame, targetWaypointLocation)
        return distancetopoint


    def check_attack_trigger(self):
        nextwaypoint = self.vehicle.commands.next
        time_elpased = time.time() - self.time_start 
        altitude = self.vehicle.location.global_relative_frame.alt

        targetLocation = LocationGlobalRelative(float(self.attack_coordinate[0]),float(self.attack_coordinate[1]),altitude)
        distancetopoint = self.get_distance_metres(self.vehicle.location.global_frame, targetLocation)
        # print(altitude)
        # print(self.attack_altitude)

        if nextwaypoint >= self.attack_waypoint :
            self.sentinel_msg = "Cyber attack triggered at waypoint: %s!" %(nextwaypoint)
            print(self.sentinel_msg)
            return True
        elif time_elpased >= self.attack_time :
            self.sentinel_msg = "Cyber attack triggered at time: %s seconds!" %(time_elpased)
            print(self.sentinel_msg)
            return True
        elif altitude >= self.attack_altitude :
            self.sentinel_msg = "Cyber attack triggered at altitude: %s!" %(altitude)
            print(self.sentinel_msg)
            return True
        elif distancetopoint <= 10 : 
            self.sentinel_msg = "Cyber attack triggered at distance to cooordinate (%s): %s!" %(targetLocation, distancetopoint)
            print(self.sentinel_msg)
            return True
        else:
            return False


    def run(self):
        self.time_start = time.time()

        print('Create a new mission (for current location)')
        self.missions = []
        self.adds_triangle_mission(self.vehicle.location.global_frame, 15)

        self.save_mission(self.original_mission_filename_save)

        self.home_location = self.vehicle.location.global_frame


        # From Copter 3.3 you will be able to take off using a mission item. Plane must take off using a mission item (currently).
        self.arm_and_takeoff(10)

        ### Trigger threaded parameter save function for sentinel panel display ###


        # sentinel_msg = "sentinel message 0"

        print("Starting mission")
        # Reset mission set to first (0) waypoint
        self.vehicle.commands.next=0

        # Set mode to AUTO to start mission
        self.vehicle.mode = VehicleMode("AUTO")


        # Monitor mission. 
        # Demonstrates getting and setting the command number 
        # Uses distance_to_current_waypoint(), a convenience function for finding the 
        #   distance to the next waypoint.
        counter = 0
        # self.attacked = False
        self.toHome = False

        # threading.Timer(1.0, trigger_param_save).start()

        while True:
            nextwaypoint = self.vehicle.commands.next
            # Update parameter status in a txt file for the tkinter panel

            if not self.toHome:
                # self.sentinel_msg = "sentinel message " + str(counter)

                print('Distance to waypoint (%s): %s' % (nextwaypoint, self.distance_to_current_waypoint()))
            if self.check_attack_trigger() and not self.attacked: # check whether attack trigger point reached.
                print('Cyper attack point is reached!!!!')
                hacked_waypoint = self.get_location_metres(self.home_location, -15, -15)
                self.add_new_mission(nextwaypoint, hacked_waypoint)
                self.attacked = True
                # pdb.set_trace()
            # if nextwaypoint==3: #Skip to next waypoint
            #     print('Skipping to Waypoint 5 when reach waypoint 3')
            #     vehicle.commands.next = 5
            # print('%s, %s, %s' %(nextwaypoint, len(self.vehicle.commands,self.distance_to_current_waypoint())))
            if nextwaypoint == len(self.vehicle.commands) and self.distance_to_current_waypoint() < 3:
                # pdb.set_trace()
                if not self.toHome:
                    print('Final waypoint reached. Return to home')
                    self.vehicle.mode = VehicleMode("RTL")
                    self.toHome = True

            if self.toHome :
                break;
            time.sleep(3)
            counter += 1
            if counter > 100:
                print("break due to counter")
                break


        # print('Now land')
        # self.vehicle.mode = VehicleMode("LAND")


        # vehicle.armed = False
        self.flag_param_save = False
        #Close vehicle object before exiting script
        print("Close vehicle object")
        timer_vehicle_close = threading.Timer(3.0,  self.vehicle.close()) 
        # vehicle.close()
        # param = [0,0,0,0,0]
        # param[0] = 0
        # param[1] = 0
        # param[2] = vehicle.battery.level
        # param[3] = vehicle.commands.next
        # param[4] = sentinel_msg
        # save_parameters("scripts/parameters.txt",sentinel_msg, param)
        # if timer is not None:
        #     print("!!!!###timer canceled!!")
        #     timer.cancel()
        # Shut down simulator if it was started.
        if self.sitl is not None:
            self.sitl.stop()


###########################   UI for sentinel   ###########################
# from Tkinter import *
# from msg_window2 import msg_window2

# root = Tk()
# app = msg_window2(master=root)
# # app.button_handler2()
# app.entry_update(vehicle)

# # app.mainloop()
# from app3 import app3
# app3_obj = app3(vehicle)
# app3_obj.run()

##############################################################################

flight_obj = Sentinel()
flight_obj.run()
