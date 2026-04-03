#!/usr/bin/env python3
"""Drive a turtle in a square pattern using direct velocity commands.

This script creates a ROS2 node that publishes Twist messages to
/turtle1/cmd_vel, making the turtle drive in a square. The turtle
leaves a visible trail so you can see the shape it draws.

Run with:  python3 ~/drive_pattern.py
(Make sure turtlesim_node is already running in another terminal.)
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class DrivePattern(Node):
    """Publish velocity commands to drive the turtle in a pattern."""

    def __init__(self):
        super().__init__('drive_pattern')
        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        # Timer fires every 0.1 seconds (10 Hz)
        self.timer = self.create_timer(0.1, self.timer_callback)

        # State machine: alternate between 'forward' and 'turn'
        self.state = 'forward'
        self.ticks = 0

        # ============================================================
        # TODO: Adjust these values to change the pattern!
        # ============================================================
        self.forward_ticks = 20     # Drive forward for 20 ticks (2.0 s)
        self.turn_ticks = 16        # Turn for 16 ticks (1.6 s)
        self.linear_speed = 1.0     # Forward speed (units/s)
        self.angular_speed = 1.0    # Turn speed (rad/s)

        self.sides_completed = 0
        self.total_sides = 4        # TODO: Change for triangle (3), pentagon (5), etc.
        # ============================================================

        self.get_logger().info(
            f'Drawing a {self.total_sides}-sided shape. '
            f'Watch the TurtleSim window!'
        )

    def timer_callback(self):
        """Called every 0.1 s — decide whether to drive or turn."""
        msg = Twist()

        if self.sides_completed >= self.total_sides:
            # Done — publish zeros to stop the turtle
            self.publisher.publish(msg)
            self.get_logger().info(
                f'Pattern complete! Drew {self.sides_completed} sides.'
            )
            self.timer.cancel()
            return

        if self.state == 'forward':
            msg.linear.x = self.linear_speed
            msg.angular.z = 0.0
            self.ticks += 1
            if self.ticks >= self.forward_ticks:
                self.ticks = 0
                self.state = 'turn'

        elif self.state == 'turn':
            msg.linear.x = 0.0
            msg.angular.z = self.angular_speed
            self.ticks += 1
            if self.ticks >= self.turn_ticks:
                self.ticks = 0
                self.state = 'forward'
                self.sides_completed += 1
                self.get_logger().info(
                    f'Side {self.sides_completed}/{self.total_sides} complete'
                )

        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = DrivePattern()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
