from __future__ import print_function
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative, Command, MAVConnection
import pdb


# Set up option parsing to get connection string
import argparse
parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect',
                    help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
sitl = None


# Start SITL if no connection string specified
if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()

# 'udp:127.0.0.1:14551'
# Connect to the Vehicle
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True, heartbeat_timeout=60)


# pdb.set_trace()
#Callback method for new messages
def attack_message_handler(self, name, msg):
    pass
def attack_message_handler_status(self, int, msg):
    pass
# Try to send message to QGC
# vehicle = connect('udp:127.0.0.1:14551', wait_ready=True) # wait_ready=True, heartbeat_timeout=60


# vehicle = connect('udp:127.0.0.1:14551', wait_ready=True, heartbeat_timeout=30) # wait_ready=True, heartbeat_timeout=60

# pdb.set_trace()
udp_conn = MAVConnection('udpin:0.0.0.0:15667', source_system=1)


vehicle._handler.pipe(udp_conn)
udp_conn.master.mav.srcComponent = 1 # needed to make QGroundControl work!
udp_conn.start()

vehicle.add_message_listener('NAMED_VALUE_INT', attack_message_handler) # listen on msg
msg1 = vehicle.message_factory.named_value_int_encode(1000,'attack_type',3) # prepare a NAMED_VALUE_INT message 
vehicle.send_mavlink(msg1) # send the custom msg to QGC

vehicle.add_message_listener('STATUSTEXT', attack_message_handler_status) # listen on msg
msg2 = vehicle.message_factory.statustext_encode(6,"Hello") # prepare a NAMED_VALUE_INT message 
vehicle.send_mavlink(msg2)

# Option 2
# def my_new_fix_targets(message):
#     pass

# udp_conn.fix_targets = my_new_fix_targets
# msg1 = vehicle.message_factory.statustext_encode(3,'Hello')
# udp_conn.master.mav.send(msg1)


# pdb.set_trace()

# vehicle.close()
# Shut down simulator if it was started.
# if sitl:
#     sitl.stop()


def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            vehicle.mode = VehicleMode("LAND")
            break
        time.sleep(1)


def readmission(aFileName):
    """
    Load a mission from a file into a list. The mission definition is in the Waypoint file
    format (http://qgroundcontrol.org/mavlink/waypoint_protocol#waypoint_file_format).

    This function is used by upload_mission().
    """
    print ("\nReading mission from file: %s" % aFileName)
    cmds = vehicle.commands
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



def check_mission(aFileName):
    """
    Upload a mission from a file. 
    """
    #Read mission from file
    missionlist = readmission(aFileName)
    
    print ("\nCompare cuurrent mission with pre-planned file: %s" % import_mission_filename)

    missions_match = True
    # cmds = vehicle.commands

    # Get the set of commands from the vehicle
    cmd_list = vehicle.commands
    cmd_list.download()
    cmd_list.wait_ready()
    # cmds.clear()
    #Add new mission to vehicle
    for i in range(0, max(len(missionlist), len(cmd_list))):
        if round(missionlist[i].x, 4) != round(cmd_list[i].x, 4) or \
        round(missionlist[i].y, 4) != round(cmd_list[i].y, 4) or \
        round(missionlist[i].z, 4) != round(cmd_list[i].z, 4) :
            # pdb.set_trace()
            missions_match = False
            return missions_match



    return True
    # print ' Upload mission'
    # vehicle.commands.upload()



def download_mission():
    """
    Downloads the current mission and returns it in a list.
    It is used in save_mission() to get the file information to save.
    """
    # print " Download mission from vehicle"
    missionlist=[]
    cmd_list = vehicle.commands
    cmd_list.download()
    cmd_list.wait_ready()
    for cmd in cmd_list:
        missionlist.append(cmd)
    return missionlist

def save_mission(aFileName):
    """
    Save a mission in the Waypoint file format 
    (http://qgroundcontrol.org/mavlink/waypoint_protocol#waypoint_file_format).
    """
    # print "\nSave mission from Vehicle to file: %s" % export_mission_filename    
    #Download mission from vehicle
    missionlist = download_mission()
    #Add file-format information
    output='QGC WPL 110\n'
    #Add home location as 0th waypoint
    home = vehicle.home_location
    output+="%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (0,1,0,16,0,0,0,0,home.lat,home.lon,home.alt,1)
    #Add commands
    for cmd in missionlist:
        commandline="%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (cmd.seq,cmd.current,cmd.frame,cmd.command,cmd.param1,cmd.param2,cmd.param3,cmd.param4,cmd.x,cmd.y,cmd.z,cmd.autocontinue)
        output+=commandline
    with open(aFileName, 'w') as file_:
        # print " Write mission to file"
        file_.write(output)
        
        
def printfile(aFileName):
    """
    Print a mission file to demonstrate "round trip"
    """
    # print "\nMission file: %s" % aFileName
    with open(aFileName) as f:
        for line in f:
            print ("hii")
            # print ' %s' % line.strip()        

def upload_mission(aFileName):
    """
    Upload a mission from a file. 
    """
    #Read mission from file
    missionlist = readmission(aFileName)
    
    # print "\nUpload mission from a file: %s" % import_mission_filename
    #Clear existing mission from vehicle
    # print ' Clear mission'
    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready()
    cmds.clear()
    #Add new mission to vehicle
    for command in missionlist:
        cmds.add(command)
    # print ' Upload mission'
    vehicle.commands.upload()

    return missionlist



######      Main function       ######
import_mission_filename = 'scripts/imported_mission.txt'
export_mission_filename = 'scripts/exported_mission.txt'


starttime=time.time()
counter = 0

arm_and_takeoff(2)
vehicle.add_message_listener('STATUSTEXT', attack_message_handler_status) # listen on msg
msg2 = vehicle.message_factory.statustext_encode(6,"Hello") # prepare a NAMED_VALUE_INT message 
vehicle.send_mavlink(msg2)

# print("Close vehicle object")
# vehicle.close()

# Shut down simulator if it was started.
# if sitl:
#     sitl.stop()




# Upload initial missionlist
missionlist = upload_mission(import_mission_filename)

cmds = vehicle.commands
cmds.download()
cmds.wait_ready()
cmds.clear()
#Add new mission to vehicle
for command in missionlist:
    cmds.add(command)
# print ' Upload mission'
vehicle.commands.upload()
print("Close vehicle object")
vehicle.close()

# Shut down simulator if it was started.
if sitl:
    sitl.stop()
# break
# while True:
#     #Upload mission from file
#     # upload_mission(import_mission_filename)

#     #Download mission we just uploaded and save to a file
#     # save_mission(export_mission_filename)

#     missions_match = check_mission(import_mission_filename)
#     if missions_match:
#         print ("Commands match!")
#     else:
#         print ("Commands do not match")
#         break


#     # cmds = vehicle.commands
#     # cmds.download()
#     # cmds.wait_ready()
#     # print " Home Location: %s" % vehicle.home_location
#     time.sleep(60.0 - ((time.time() - starttime) % 60.0))
#     counter += 1

#     if counter > 2:
#     # Close vehicle object before exiting script
#         print("Close vehicle object")
#         vehicle.close()

#         # Shut down simulator if it was started.
#         if sitl:
#             sitl.stop()
#         break
