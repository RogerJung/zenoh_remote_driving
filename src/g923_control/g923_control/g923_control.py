import pygame
import rclpy
from rclpy.node import Node
from configparser import ConfigParser
import math
import zenoh
import json
import time
from zenoh_ros_type.autoware_auto_msgs import AckermannControlCommand, LongitudinalCommand, AckermannLateralCommand
import argparse
from zenoh_ros_type.rcl_interfaces import Time

SET_CONTROL_KEY_EXPR = 'external/selected/control_cmd'

parser = argparse.ArgumentParser(prog='remote_control')
parser.add_argument('--connect', '-e', dest='connect',
                    metavar='ENDPOINT',
                    action='append',
                    type=str,
                    help='Endpoints to connect to.')
parser.add_argument('--listen', '-l', dest='listen',
                    metavar='ENDPOINT',
                    action='append',
                    type=str,
                    help='Endpoints to listen on.')
args = parser.parse_args()


conf = zenoh.Config()

if args.connect is not None:
    conf.insert_json5(zenoh.config.CONNECT_KEY, json.dumps(args.connect))
if args.listen is not None:
    conf.insert_json5(zenoh.config.LISTEN_KEY, json.dumps(args.listen))

"""
[G923 Racing Wheel]
steering_wheel = 0
clutch = 1
throttle = 2
brake = 3
gear_up = 4
gear_down = 5
gear_1 = 12
gear_2 = 13
gear_3 = 14
gear_4 = 15
gear_5 = 16
reverse = 17
"""

class g923_controller(Node):
    def __init__(self, session):
        super().__init__("g923_controller")
        pygame.init()
        self.session = session
        self._joystick = pygame.joystick.Joystick(0)
        self._joystick.init()

        self._steer_idx = 0
        self._throttle_idx = 2
        self._brake_idx = 3
        self._reverse_idx = 17
        self._gearup_idx = 4
        self._geardown_idx = 5
        self._gear_1 = 12
        self._gear_2 = 13
        self._gear_3 = 14
        self._gear_4 = 15
        self._gear_5 = 16
        self._reverse = 17
        
        self.control_publisher = self.session.declare_publisher(SET_CONTROL_KEY_EXPR)
        
        ### Control command
        self.control_command = AckermannControlCommand(
            stamp=Time(
                sec=0,
                nanosec=0
            ),
            lateral=AckermannLateralCommand(
                stamp=Time(
                    sec=0,
                    nanosec=0
                ),
                steering_tire_angle=0,
                steering_tire_rotation_rate=0
            ),
            longitudinal=LongitudinalCommand(
                stamp=Time(
                    sec=0,
                    nanosec=0
                ),
                speed=0,
                acceleration=0,
                jerk=0
            )
        )
    
    def pub_control(self, steering, throttle):
        ### Steering angle
        self.control_command.lateral.steering_tire_angle = steering
        
        ### Timestamp
        self.control_command.stamp.sec = int(time.time() * 1000) % 100000
        self.control_command.stamp.nanosec = 0

        ### Pub control
        self.control_command.longitudinal.speed = throttle
        self.control_publisher.put(self.control_command.serialize())

    def run(self):
        joysticks = {}
        done = False
        reverse = False
        while not done:
            # Event processing step.
            # Possible joystick events: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
            # JOYBUTTONUP, JOYHATMOTION, JOYDEVICEADDED, JOYDEVICEREMOVED
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True  # Flag that we are done so we exit this loop.

                if event.type == pygame.JOYBUTTONDOWN:
                    print("Joystick button pressed.")
                    if event.button == 0:
                        joystick = joysticks[event.instance_id]
                        if joystick.rumble(0, 0.7, 500):
                            print(f"Rumble effect played on joystick {event.instance_id}")
                    elif event.button == self._reverse_idx:
                        reverse = True

                if event.type == pygame.JOYBUTTONUP:
                    print("Joystick button released.")
                    if event.button == self._reverse_idx:
                        reverse = False

                # Handle hotplugging
                if event.type == pygame.JOYDEVICEADDED:
                    # This event will be generated when the program starts for every
                    # joystick, filling up the list without needing to create them manually.
                    joy = pygame.joystick.Joystick(event.device_index)
                    joysticks[joy.get_instance_id()] = joy
                    print(f"Joystick {joy.get_instance_id()} connencted")

                if event.type == pygame.JOYDEVICEREMOVED:
                    del joysticks[event.instance_id]
                    print(f"Joystick {event.instance_id} disconnected")

            # For each joystick:
            for joystick in joysticks.values():

                # Usually axis run in pairs, up/down for one, and left/right for
                # the other. Triggers count as axes.
                axes = joystick.get_numaxes()
                jsInputs = [float(self._joystick.get_axis(i)) for i in range(axes)]
                # Custom function to map range of inputs [1, -1] to outputs [0, 1] i.e 1 from inputs means nothing is pressed
                # For the steering, it seems fine as it is
                K1 = -0.25  # 0.55
                steerCmd = K1 * math.tan(1.1 * jsInputs[self._steer_idx])

                K2 = 1.6  # 1.6
                throttleCmd = K2 + (2.05 * math.log10(
                    -0.7 * jsInputs[self._throttle_idx] + 1.4) - 1.2) / 0.92
                if throttleCmd <= 0:
                    throttleCmd = 0
                elif throttleCmd > 1:
                    throttleCmd = 1
                
                if reverse:
                    throttleCmd = throttleCmd * -1

                brakeCmd = 1.6 + (2.05 * math.log10(
                    -0.7 * jsInputs[self._brake_idx] + 1.4) - 1.2) / 0.92
                if brakeCmd <= 0:
                    brakeCmd = 0
                elif brakeCmd > 1:
                    brakeCmd = 1
                
            print(f"{steerCmd:.3f}, {throttleCmd:.3f}, {brakeCmd:.3f}")
            self.pub_control(steerCmd, throttleCmd * 15)

            time.sleep(0.1)


def main(args=None):
    session = zenoh.open(conf)
    rclpy.init(args=args)

    controller = g923_controller(session)
    controller.run()

    controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()