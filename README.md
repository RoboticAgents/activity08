# Activity 8: Writing Your First ROS2 Node — Direct Velocity Control

This activity is a companion to the [Writing ROS2 Nodes slides](https://learnroboticagents.com/slides/ros2nodes.html). Before you write the `NavigateToPose` action client in Project 4 Part 3, it is helpful to first experience what it means to control a robot by **publishing velocity commands directly** — using the same `Twist` message type but without any navigation intelligence.

You'll use **TurtleSim** — a lightweight 2D robot simulator built into ROS2. The turtle responds to velocity commands just like a TurtleBot, but in a simple 2D window where it **draws a trail** as it moves. This lets you see exactly what your node is doing.

**Due:** Wednesday, April 8 at 11:00 AM

---

## Why TurtleSim?

| | TurtleSim (this activity) | TurtleBot3 in Gazebo (Project 4) |
|---|---|---|
| **Dimension** | 2D — top-down view | 3D — full physics simulation |
| **Velocity topic** | `/turtle1/cmd_vel` (`Twist`) | `/cmd_vel` (`TwistStamped`) |
| **Sensors** | Position only (`/turtle1/pose`) | Lidar, odometry, IMU |
| **Obstacle avoidance** | None — turtle hits the wall and stops | Nav2 plans around obstacles |
| **Visual feedback** | Draws a trail on screen | 3D robot moves in Gazebo |
| **ROS2 concepts** | Same: nodes, topics, publishers, messages, timers |

The **ROS2 patterns are identical** — you create a node, create a publisher, and publish messages on a timer. The only differences are the topic name and whether a navigation stack is helping you.

---

## Setup

1. Make sure Docker Desktop is running.

2. Start the TurtleSim environment:

   ```bash
   cd activity08
   docker compose up
   ```

   > **Slow machine?** Use low-lag mode: `docker compose -f docker-compose.yml -f compose.lowlag.yml up`

   > **Note:** If you have another Docker environment running on port 6080 (e.g., from Project 4), stop it first: `docker compose down` in that project's folder.

3. Open your browser and go to **http://localhost:6080**. You'll see a VNC desktop.

4. Right-click the desktop → **Terminal** to open a terminal.

---

## Part 1: Exploring the ROS2 Graph

In Activities 5 and 6, you used `ros2 node list`, `ros2 topic list`, and `ros2 topic echo` to inspect TurtleBot3 in Gazebo. Now you'll use the **same tools** with a completely different simulator — these tools work with *any* ROS2 system.

### Step 1: Launch TurtleSim

In the terminal inside the VNC desktop:

```bash
source /opt/ros/jazzy/setup.bash
ros2 run turtlesim turtlesim_node
```

A window with a turtle on a blue background will appear. This turtle is your robot.

### Step 2: Explore the ROS2 graph

Open a **second terminal** (right-click desktop → Terminal) and run these commands — the same ones you used in Activity 5 with TurtleBot3:

```bash
source /opt/ros/jazzy/setup.bash

# What nodes are running?
ros2 node list

# What topics exist?
ros2 topic list

# What type of message does /turtle1/cmd_vel use?
ros2 topic info /turtle1/cmd_vel

# What does the turtle's position look like?
ros2 topic echo /turtle1/pose --once

# What does this node subscribe to and publish?
ros2 node info /turtlesim
```

Record your findings in `experiments.md`.

### Step 3: Drive the turtle manually

Try publishing a velocity command directly from the command line — this is the same `ros2 topic pub` you used in Activity 5:

```bash
# Drive forward
ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 1.0}, angular: {z: 0.0}}"

# Turn in place
ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.0}, angular: {z: 1.5}}"
```

Notice the turtle leaves a **trail** showing where it's been.

> **Tip:** To clear the trail, run: `ros2 service call /clear std_srvs/srv/Empty`

### Step 4: Compare to TurtleBot3

Think about how this compares to the TurtleBot3 environment from Activity 5 and Project 4:
- In Gazebo, the velocity topic was `/cmd_vel` — here it's `/turtle1/cmd_vel`
- The message type is the same: `geometry_msgs/msg/Twist`
- The ROS2 tools work identically

Fill in the node-topic table in `experiments.md`.

---

## Part 2: Running and Modifying a Publisher Node

In Part 1, you sent commands one at a time from the CLI. Now you'll use a **Python node** that publishes velocity commands on a timer — the same publisher + timer pattern from the [slides](https://learnroboticagents.com/slides/ros2nodes.html) (slide 6).

### Step 1: Examine the provided script

The file `drive_pattern.py` is mounted in the container at `~/drive_pattern.py`. Open it in the terminal:

```bash
cat ~/drive_pattern.py
```

Read through the code and identify:
- What class does it inherit from? (This is the same `Node` base class from the slides)
- What does `create_publisher()` do?
- What does `create_timer()` do?
- How does the state machine alternate between driving forward and turning?

### Step 2: Run the script

In a terminal (keep turtlesim running in the other terminal):

```bash
source /opt/ros/jazzy/setup.bash
python3 ~/drive_pattern.py
```

Watch the turtle draw a square! The trail shows you exactly what the robot did.

Observe the terminal output — the node logs each side it completes.

### Step 3: Echo the velocity commands

While `drive_pattern.py` is running, open a **third terminal** and echo the velocity topic:

```bash
source /opt/ros/jazzy/setup.bash
ros2 topic echo /turtle1/cmd_vel
```

You'll see the `Twist` messages being published in real time. Notice the pattern: `linear.x` is non-zero when driving forward, `angular.z` is non-zero when turning.

Record what you observe in `experiments.md`.

### Step 4: Modify the pattern

Stop the current script (`Ctrl+C`). Clear the trail and reset the turtle:

```bash
ros2 service call /reset std_srvs/srv/Empty
```

Now edit `drive_pattern.py` to make the turtle draw a **different shape**.

> **Edit on your Mac, not in the container.** The file is volume-mounted, so any changes you save in VS Code on your Mac are instantly available inside the container — no editor needed in the container (`nano` is not installed).

Look for the `# TODO` section. Choose one:

- **Triangle**: Change `total_sides` to `3` and adjust `turn_ticks` so the turtle turns 120° instead of 90°
- **Circle**: Set constant `linear.x` and `angular.z` simultaneously (remove the state machine)
- **Star**: Use longer forward segments and sharper turns (144° exterior angle)

> **Hint for triangle:** At `angular_speed = 1.0` rad/s, a 120° turn (2π/3 ≈ 2.09 rad) takes about 2.09 seconds. At 0.1 s/tick, that's ~21 ticks.

Run your modified script and screenshot the result.

### Step 5: The crash test

Reset the turtle, then try driving it straight into the wall:

```bash
ros2 topic pub /turtle1/cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 5.0}, angular: {z: 0.0}}" -r 10
```

What happens? The turtle hits the boundary and **stops** — but your publisher keeps sending velocity commands. There's no obstacle detection, no replanning, no recovery. Press `Ctrl+C` to stop.

**This is the key limitation of direct velocity control.** In Project 4, Nav2 solves this using costmaps and path planning — your node just says *where* to go, and Nav2 figures out *how* to get there safely.

Record what happened in `experiments.md`.

---

## Part 3: Connecting to Project 4

In this activity you published `Twist` messages directly to control the turtle. In **Project 4 Part 3**, you'll use a different ROS2 pattern — **actions** — to send `NavigateToPose` goals to Nav2. You tell the robot *where to go*, and Nav2 handles obstacle avoidance, path planning, and recovery.

The slides (slides 8–18) cover actions and the `NavigateToPose` pattern in detail. Review them before starting P4 Part 3.

### Quick Quaternion Check

In P4 Part 3, navigation goals include an **orientation** as a quaternion. For a 2D robot, this simplifies to:

```python
import math
yaw = 1.57  # radians (90°)
z = math.sin(yaw / 2.0)   # → 0.7071
w = math.cos(yaw / 2.0)   # → 0.7071
```

Use this formula to answer the quaternion question in `experiments.md`.

### What's Next?

| Step | What | Where |
|------|------|-------|
| **You just did** | Direct velocity control (publisher + timer) | Activity 8 |
| **Next** | Goal-based navigation (action client + callbacks) | P4 Part 3 |
| **After that** | Sim-to-real transfer with physical TurtleBot 4 | P4 Part 4 |

Answer the reflection questions in `experiments.md`.
