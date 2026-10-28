import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Wrench
from std_msgs.msg import Int32MultiArray


class TeleopNode(Node):
    def __init__(self):
        # 1. initialize the node with it's official ros2 name
        super().__init__('teleop_node')

        # 2. subscribing => raw joystick inputs from topside laptop rosbridge
        self.joy_sub = self.create_subscription(
            Joy,  # message type
            '/joy',  # topic we listening to
            self.joy_callback,  # call non stop every time data arrives
            10  # QoS holds 10 messages in a queue if cpu gets busy
        )

        # 3. publishing desired 6 dof direction(Surge,Sway,Heave,Roll,Pitch,Yaw)
        self.wrench_pub = self.create_publisher(
            Wrench,
            '/rov/cmd_wrench',
            10
        )
        self.buttons_pub = self.create_publisher(
            Int32MultiArray,
            '/rov/cmd_buttons',
            10
        )
# instead of print in ros2 use this, message appears on start [--init--(x)]
        self.get_logger().info('Teleop Node initialized and waiting for /joy command...')

    def joy_callback(self, msg: Joy):  # we called this func when subscribing
        """
        Runs automatically every time a new joystick message arrives on /joy
        """
        # Note: Surge = Forward/Backward (Fx), Sway = Left/Right (Fy), Heave = Up/Down (Fz)
        # double check axis index according to the joy input customised
        if len(msg.axes) >= 4:
            cmd_wrench = Wrench()  # here we're following the ros2 format btw
            cmd_wrench.force.x = float(msg.axes[1])   # Sway
            cmd_wrench.force.y = float(msg.axes[0])   # Surge
            cmd_wrench.force.z = float(msg.axes[3])   # Heave
            cmd_wrench.torque.z = float(msg.axes[2])  # Yaw

            # Add Pitch and Roll if 6 axes exist
            if len(msg.axes) >= 6:
                cmd_wrench.torque.x = float(msg.axes[4])  # Pitch
                cmd_wrench.torque.y = float(msg.axes[5])  # Roll

            self.wrench_pub.publish(cmd_wrench)

        if len(msg.buttons) > 0:
            map_buttons = Int32MultiArray()
            map_buttons.data = [int(b) for b in msg.buttons]
            self.buttons_pub.publish(map_buttons)


def main(args=None):
    rclpy.init(args=args)
    node = TeleopNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
