import zenoh
import time
import json
import argparse
from zenoh_ros_type.autoware_auto_msgs import AckermannControlCommand, LongitudinalCommand, AckermannLateralCommand
# from autoware_auto_control_msgs.msg import AckermannControlCommand
from Adafruit_PCA9685 import PCA9685

GET_CONTROL_KEY_EXPR = 'external/selected/control_cmd'

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


# Initialize the PCA9685 using the default address (0x40).
pwm = PCA9685(address=0x40, busnum=7)

# Set the PWM frequency to control the servo and ESC.
pwm.set_pwm_freq(60)

class VehicleController():
    def __init__(self, session, scope, use_bridge_ros2dds=True):
        self.session = session

        # This section sets the default values for the ESC
        self.fwdmax = 580
        self.revmax = 180
        self.stop = 380  # No throttle value accepted by the ESC

        # This section sets the default values for the steering servo
        self.steering_value = 380
        self.steering_init = 380
        self.steering_max_left = 260
        self.steering_max_right = 500
        self.reverse = 0
        
        self.topic_prefix = scope
        self.service_prefix = scope
        
        def callback_control_cmd(sample):
            
            data = AckermannControlCommand.deserialize(sample.payload)
            
            c_time = int(time.time() * 1000) % 100000
            recv_time = data.stamp.sec
            latency = c_time - recv_time
            
            steering_value = int(-data.lateral.steering_tire_angle * 380) + self.steering_init
            
            speed = int(data.longitudinal.speed) + self.stop
            if speed < self.stop:
                if self.reverse == 0:
                    self.reverse = 1
                    pwm.set_pwm(0, 0, 340) # set pwm flag
                    pwm.set_pwm(0, 0, 380)
                speed *= 0.9
                speed = int(speed)
            elif speed > self.stop:
                self.reverse = 0


            # Set the PCA9685 servo controller (dc motor and steering servo)
            if self.revmax < speed < self.fwdmax:
                pwm.set_pwm(0, 0, speed)

            if self.steering_max_left < self.steering_value < self.steering_max_right:
                pwm.set_pwm(1, 0, steering_value)

            print(f'reverse" {self.reverse}, latency: {latency} ms, steering: {steering_value:.2f}, speed: {speed:.2f}')
        
        ## Subscriber
        self.subscriber_control_cmd = self.session.declare_subscriber(GET_CONTROL_KEY_EXPR, callback_control_cmd)
        

def main():
    
    session = zenoh.open(conf)
    vehicleController = VehicleController(session, 'v1')
    
    while True:
        time.sleep(0.05)

