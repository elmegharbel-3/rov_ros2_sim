import rclpy
import math
from rclpy import Node
from sensor_msgs.msg import Imu
from std_msgs.msg import Float32,Float32MultiArray
from geometry_msgs.msg import Quaternion


class MockSerial(Node):
    super.__init__("mock_serial_node")
    def __init__(self):
        self.current_depth = Float32()
        self.current_imu = Imu()
        self.motors_cmd_sub = self.create_subscription(
            Float32MultiArray,
            'rov/motors_cmd',
            self.motors_cmd_callback,
            10
        )

        self.current_imu_pub = self.create_publisher(
            Imu,
            'rov/imu',
            10
        )
        self.current_depth_pub = self.create_publisher(
            Float32,
            'rov/Depth',
            10
        )

    def motors_cmd_callback(self,msg:Float32MultiArray):
        self.motors_cmd = msg
        # microcontroller serial communication code here -->
    
    def telemetry_publisher(self):
        current_time = self.get_clock().now()
        depth_simulation = 1.5 + 0.05 * math.sin(current_time.nanoseconds / 1e9)
        self.current_depth.data = depth_simulation
        self.current_depth_pub.publish(self.current_depth)

        self.current_imu.stamp = current_time.to_msg()
        self.current_imu.frame_id = 'base_link'

        # Orientation Quaternion representing level attitude (Roll=0, Pitch=0, Yaw=0)
        self.current_imu.orientation.x = 0.0
        self.current_imu.orientation.y = 0.0
        self.current_imu.orientation.z = 0.0
        self.current_imu.orientation.w = 1.0

        # Angular Velocity (rad/s)
        self.current_imu.angular_velocity.x = 0.0
        self.current_imu.angular_velocity.y = 0.0
        self.current_imu.angular_velocity.z = 0.0

        # Linear Acceleration (m/s^2) - Gravity on Z axis
        self.current_imu.linear_acceleration.x = 0.0
        self.current_imu.linear_acceleration.y = 0.0
        self.current_imu.linear_acceleration.z = 9.81

        # Publish to /rov/imu
        self.imu_pub.publish(self.current_imu)
def main(args=None):
    rclpy.init(args=args)
    node = MockSerial()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown
if __name__ == '--main__':
    main()




    