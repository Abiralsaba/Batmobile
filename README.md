# Mars Rover — Ubuntu VM / Jetson

**Develop on your Mac's Ubuntu 22.04 VM with ROS 2 Humble.** Later copy this same ROS 2 package to Jetson Orin with its compatible Ubuntu 22.04 / JetPack / ZED SDK. Do **not** develop natively in macOS for this project.

One Python file per feature under `rover/`; no nested Python subpackages. Module descriptions are in each file's opening docstring and in [MODULES.md](MODULES.md).

## Scope

- **Now:** existing GNSS + IMU + EKF + motors (integration placeholders); ZED X astronaut detection and stereo position (adapter placeholder); quiet beckoning; offline voice from C2; FOLLOW, STAY, COME; hammer detection and **YES/NO-authorized approach only**.
- **Later:** attach real prior rover drivers; EVA-suit monitoring; arm pickup and GIVE.
- **No LiDAR**, no cloud dependency at competition time. The current code is a **non-actuating scaffold**. No real ZED / Whisper / motors are connected.

## Quick start — Ubuntu 22.04 VM (ROS 2 Humble)

```bash
# Install ROS 2 Humble separately first, then in an Ubuntu terminal:
source /opt/ros/humble/setup.bash
mkdir -p ~/rover_ws/src
# Extract ZIP so this project is at ~/rover_ws/src/mars_rover
# (or rename that folder to mars_rover; package name stays mars_rover).
cd ~/rover_ws
python3 -m pip install --user -r src/mars_rover/requirements.txt
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
ros2 launch mars_rover mars_rover.launch.py
```

> Install `python3-colcon-common-extensions`, `python3-rosdep`, and `ros-humble-ros-base` / `ros-humble-desktop` as needed. Use system Python for ROS 2 to avoid mixing mismatched rclpy installations. Ubuntu ROS packages come from apt, not pip. See [DEPENDENCIES.md](DEPENDENCIES.md).

In a **second sourced terminal**:

```bash
ros2 topic echo /rover/state
ros2 topic pub --once /dev/cmd std_msgs/msg/String '{data: "start"}'
```

The launch file currently starts one executable, `mission_control_node`. Future
perception or hardware files will gain `_node.py` names only when they become
real ROS nodes; the existing feature modules remain pure, testable logic.

For a pure Python simulation (works in the VM with Python even without ROS):

```bash
cd ~/rover_ws/src/mars_rover
PYTHONPATH=. python3 -m rover.demo
PYTHONPATH=. python3 -m unittest discover -s tests -v
```

## Essential files

- [AGENT_PROMPT.md](AGENT_PROMPT.md): copy to your AI coding agent.
- [BRAIN.md](BRAIN.md): fixed project context / decisions.
- [ROADMAP.md](ROADMAP.md): ordered development stages.
- [MODULES.md](MODULES.md): one-line descriptions of each `.py` file.
- [requirements.txt](requirements.txt), [requirements-jetson.txt](requirements-jetson.txt), [DEPENDENCIES.md](DEPENDENCIES.md): Python vs ROS / CUDA / ZED SDK dependencies.
- [config.yaml](config.yaml): centralized, provisional topic names and conservative defaults.

## Safety and competition caveats

Never connect demo commands directly to motors. A physical all-power E-stop, low-level controller watchdog, calibrated `base_link` pose, local stereo-obstacle safety checks and reviewed motor adapter are required before physical driving. Laptop voice is a **development operator interface**, not a substitute for an astronaut's quiet beckoning gesture (full 15-point FOLLOW option) or other judged astronaut-issued commands. 2027 FETCH and GIVE still require real arm manipulation to earn their points.
