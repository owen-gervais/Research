import serial
from time import sleep

import rclpy
from rclpy.node import Node

from tutorial_interfaces.msg import Imu


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('acceleration_publisher')
        self.publisher_ = self.create_publisher(Imu, 'acceleration', 10)
        timer_period = 0.2  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.serialPort = serial.Serial(port = '/dev/ttyS0',
         baudrate = 115200,
         timeout = 1)
        self.waitTime = .2


    def timer_callback(self):
        msg = Imu()

        data = self.serialPort.readline().decode('utf-8')
        data = list(map(int,data[1:-4].split(',')))
        msg.x = data[0]
        msg.y = data[1]
        msg.z = data[2]
        self.publisher_.publish(msg)
        sleep(self.waitTime)

def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
