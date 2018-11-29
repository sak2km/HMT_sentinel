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

print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True, heartbeat_timeout=60)


#Callback method for new messages
def attack_message_handler(self, name, msg):
    pass
def attack_message_handler_status(self, int, msg):
    pass
# Try to send message to QGC
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

pdb.set_trace()


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



starttime=time.time()
counter = 0

arm_and_takeoff(2)
vehicle.add_message_listener('STATUSTEXT', attack_message_handler_status) # listen on msg
msg2 = vehicle.message_factory.statustext_encode(6,"Hello") # prepare a NAMED_VALUE_INT message 
vehicle.send_mavlink(msg2)

print("Close vehicle object")
vehicle.close()

# Shut down simulator if it was started.
if sitl:
    sitl.stop()