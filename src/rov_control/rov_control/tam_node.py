import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Wrench
from std_msgs.msg import Float32MultiArray

class TamNode(Node):
    def __init__(self):
        super().__init__("tam_node")
        self.allocated_wrench_sub = self.create_subscription(
            Wrench,
            'rov/allocated_wrench',
            self.allocated_wrench_callback,
            10
        )

        self.motors_cmd_pub = self.create_publisher (
            Float32MultiArray,
            "rov/motors_cmd",
            10
        )
    def allocated_wrench_callback(self,msg:Wrench):
        self.allocated_wrench = Wrench()
        self.wrench_list = Float32MultiArray()
        self.allocated_wrench = msg
        self.wrench_list.data = [
            self.allocated_wrench.force.x,
            self.allocated_wrench.force.y,
            self.allocated_wrench.force.z,
            self.allocated_wrench.torque.x, # pitch
            self.allocated_wrench.torque.y, # roll
            self.allocated_wrench.torque.z, # yaw
            ]
        # allocation matrix code here -->

        self.motors_cmd_pub.publish(self.wrench_list)

def main(args=None):
    rclpy.init(args=args)
    node = TamNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
if __name__ == "__main__":
    main()

