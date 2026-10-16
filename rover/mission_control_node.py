"""Mission control ROS node for development state transitions. IMPLEMENTED.

Subscribe /dev/cmd (std_msgs/String), publish /rover/state (std_msgs/String).
These mock events are not judged astronaut commands and NEVER control motors.
"""
from rover.mission import Mission


def main():
    import rclpy
    from rclpy.node import Node
    from std_msgs.msg import String

    class MissionControlNode(Node):
        def __init__(self):
            super().__init__('mission_control')
            self.mission = Mission()
            self.state_pub = self.create_publisher(String, '/rover/state', 10)
            self.create_subscription(String, '/dev/cmd', self.on_command, 10)
            self.create_timer(1.0, self.publish_state)
            self.get_logger().warn('DEV-ONLY. No motor publisher; /dev/cmd mock only.')
            self.publish_state()

        def on_command(self, msg):
            accepted = self.mission.event(msg.data, source='mock_c2')
            self.get_logger().info(f'event={msg.data!r} accepted={accepted}')
            self.publish_state()

        def publish_state(self):
            msg = String()
            msg.data = self.mission.state.value
            self.state_pub.publish(msg)

    rclpy.init()
    node = MissionControlNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
