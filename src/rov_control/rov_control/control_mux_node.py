import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Wrench
from std_msgs.msg import String
from std_msgs.msg import Int32MultiArray

class ControlMuxNode(Node):
    def __init__(self):
        super().__init__('control_mux_node')
        self.current_mode = "MANUAL"
	self.wrench_sub = self.create_subscription(
 	    Wrench,
	    '/rov/cmd_wrench',
	    self.manual_callback,
	    10
	)

        self.button_sub = self.create_subscription(
            Int32MultiArray,
	    '/rov/cmd_buttons',
            self.buttons_callback,
            10
        )
        self.prev_button_state = 0 # initially it's not clicked
	self.toggle_depth_index = 0 # index of the depth control button

	self.target_pub = self.create_publisher(
	    Wrench,
	    '/rov/target_wrench',
	    10
	)
       self.mode_pub = self.create_publisher(
	String,
	'/rov/current_mode',
	10
	)
	self.get_logger().info('Control Mux Node initialized in Manual mode')

    def buttons_callback(self, msg: Int32MultiArray):
	if len(msg.data) > self.toggle_depth_index:
            current_btn = msg.data[self.toggle_depth_index]
	    if self.prev_button_state == 0 and current_btn == 1:
		if self.current_mode == "MANUAL":
		    self.current_mode = "DEPTH_HOLD"
		else: self.current_mode = "MANUAL"
		self.get_logger().info(f"Button Pressed!! Mode switched to {self.current_mode}")
                mode_msg = String()
		mode.msg.data = self.current_mode
		self.mode_pub.publish(mode_msg)
	    self.prev_button_state = current_btn
    def manual_callback(self, msg: Wrench):
	output_wrench = wrench()
	if self.current_mode == "MANUAL":
	    output_wrench = msg
	elif self.current_mode == "DEPTH_HOLD":
	    output_wrench.force.x = msg.force.x
            output_wrench.force.y = msg.force.y
	    # output_wrench.force.z is left at 0.0 so PID Latter can control it
            output_wrench.torque.x = msg.torque.x
            output_wrench.torque.y = msg.torque.y
            output_wrench.torque.z = msg.torque.z
	self.target_pub.publish(output_wrench)
def main(args=None):
    rclpy.init(args=args)
    node = ControlMuxNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown
if __name__ == '--main__':
    main()

