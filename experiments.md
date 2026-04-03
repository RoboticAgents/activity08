# Activity 8: Writing Your First ROS2 Node — Experiments

## Name:

---

## Part 1: Exploring the ROS2 Graph

**Q1: Run `ros2 node list` with turtlesim running. What nodes are listed?**

(your answer)

---

**Q2: Run `ros2 topic list` and fill in the table below. Use `ros2 topic info <topic>` to find each topic's message type.**

| Topic | Message Type | Publisher(s) | Subscriber(s) |
|-------|-------------|-------------|---------------|
|       |             |             |               |
|       |             |             |               |
|       |             |             |               |
|       |             |             |               |

---

**Q3: Run `ros2 topic echo /turtle1/pose --once`. What fields does the pose message contain? What is the turtle's starting position and heading?**

(your answer)

---

**Q4: Run `ros2 node info /turtlesim`. List the topics it subscribes to and publishes. What is the difference between these two lists in terms of how you interact with the robot?**

Subscribes to (inputs you can send):
-

Publishes (outputs you can read):
-

(Ignore the Services and Action sections for now.)

---

## Part 2: Running and Modifying a Publisher Node

**Q5: Look at `drive_pattern.py`. What three ROS2 concepts does the node use? Fill in the table with the specific method call from the code.**

| ROS2 Concept | Method call in drive_pattern.py |
|-------------|-------------------------------|
|             |                               |
|             |                               |
|             |                               |

---

**Q6: When you run `drive_pattern.py`, does the turtle draw a perfect square? If not, why? What does this tell you about open-loop control (commanding movement without sensor feedback)?**

(your answer)

---

**Q7: Paste the modified section of `drive_pattern.py` that makes a different shape. What shape did you choose and what values did you change?**

Shape:

```python
# Paste your modified code here
```

Screenshot or description of the result:

---

**Q8: (Crash test) When you drove the turtle into the wall at high speed, what happened? Did the node detect the collision? Did it try to recover or replan? Why not?**

(your answer)

---

## Part 3: Connecting to Project 4

**Q9: Fill in this comparison table between what you did in this activity and what you'll do in P4 Part 3.**

|                                  | Activity 8 (Direct Control) | P4 Part 3 (NavigateToPose) |
|----------------------------------|----------------------------|---------------------------|
| **You tell the robot...**        |                            |                           |
| **Obstacles are handled by...**  |                            |                           |
| **ROS2 communication pattern**   |                            |                           |
| **What happens if path is blocked?** |                        |                           |

---

**Q10: Compute the quaternion values for a goal facing "up" on the map (yaw = 90 degrees = pi/2 radians). Show your work using the formula from the README.**

```
z = sin(_____ / 2) = _____

w = cos(_____ / 2) = _____
```

---

**Q11: Across activities 5–8, you've used `ros2 node list` and `ros2 topic list` (Activity 5), traced lidar data through Cartographer for SLAM (Activity 6), analyzed Nav2 costmap parameters (Activity 7), and now written a publisher node (Activity 8). How do all of these pieces connect for P4 Part 3, where your Python node sends NavigateToPose goals to Nav2?**

(your answer)
