import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Wrench
from sensor_msgs.msg import Imu
from std_msgs.msg import Float32,String

class pid_control_node(Node):
    def __init__(self):
        super().__init__('pid_control_node')

        self.current_mode = 'PID'
        self.current_depth = 0.0
        self.target_depth = 0.0
        self.current_imu = Imu()
        # subscriptions
        self.target_wrench_sub = self.create_subscription(
            Wrench,
            '/rov/target_wrench',
            self.target_wrench_callback,
            10
        )
        self.current_depth_sub = self.create_subscription(
            Float32,
            'rov/Depth',
            self.current_depth_callback,
            10
        )
        self.current_imu_sub = self.create_subscription(
            Imu,
            'rov/imu',
            self.current_imu_callback,
            10
        )
        self.current_mode_sub = self.create_subscription(
            String,
            'rov/current_mode',
            self.current_mode_callback,
            10
        )
        # publishing
        self.allocated_wrench_pub = self.create_publisher(
            Wrench,
            'rov/allocated_wrench',
            10
        )

        self.get_logger().info('PID controller initialized updated with depth and imu and current mode modifying the wrench')

    def target_wrench_callback(self,msg:Wrench):
        allocated_wrench = Wrench()
        if self.current_mode == "MANUAL":
            allocated_wrench = msg # wrench is passed as it is
        elif self.current_mode == "DEPTH_HOLD":
            current_depth = self.current_depth
            target_depth = self.target_depth
            allocated_wrench.force.x = msg.force.x
            allocated_wrench.force.y = msg.force.y
            allocated_wrench.torque.x = msg.torque.x
            allocated_wrench.torque.y = msg.torque.y
            allocated_wrench.torque.z = msg.torque.z
            # Pid controler for only the depth would be here
            allocated_wrench.force.z = 0.0 # its value will depend on the current and target depth
        elif self.current_mode == "IMU":
            current_depth = self.current_depth
            target_depth = self.target_depth
            current_imu = self.current_imu
            # Pid controler code would be here
            allocated_wrench.force.x = msg.force.x
            allocated_wrench.force.y = msg.force.y
            allocated_wrench.force.z = msg.force.z
            allocated_wrench.torque.x = msg.torque.x
            allocated_wrench.torque.y = msg.torque.y
            allocated_wrench.torque.z = msg.torque.z
        self.allocated_wrench_pub.publish(allocated_wrench)
    def current_depth_callback(self,msg:Float32):
        self.current_depth = msg.data
    def current_imu_callback(self,msg:Imu):
        self.current_imu = Imu()
        self.current_imu = msg
    def current_mode_callback(self, msg:String):
        self.current_mode = msg.data.upper()
def main(args=None):
    rclpy.init(args=args)
    node = pid_control_node()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
if __name__ == "__main__":
    main()
