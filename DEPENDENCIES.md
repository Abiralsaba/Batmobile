# Dependency rules — Ubuntu VM now, Jetson later

## Ubuntu 22.04 VM on Mac
- Install Ubuntu **22.04**, ROS **2 Humble**, `python3-colcon-common-extensions`, `python3-rosdep`, `python3-pip` and tools via Ubuntu apt/ROS repos. Use `rosdep install --from-paths src --ignore-src -r -y` for package dependencies.
- `requirements.txt` holds only small *pip-installable Python* dependencies. The standard-library unit tests require no GPU.
- For native ROS 2 Humble Python nodes, use the Python installation compatible with the apt-installed ROS 2 environment; generally Ubuntu 22.04 Python 3.10. Do not `pip install rclpy` into an unrelated Mac Python runtime.
- VM can run mock/recorded data; ZED X GMSL2 camera and Jetson TensorRT inference will **not** be assumed accessible through UTM VM.

## Jetson Orin (future)
- Confirm exact board module/carrier, `uname -m`, `cat /etc/nv_tegra_release`, `python3 --version`, JetPack version, ZED GMSL2 interface and the Stereolabs compatibility matrix before installing anything.
- Jetson system libraries and drivers are vendor/apt-managed: **JetPack/L4T, CUDA, TensorRT, ZED SDK, ZED ROS 2 wrapper**, ROS 2 Humble, capture-card drivers. They cannot be reliably expressed in pip requirements alone.
- `requirements-jetson.txt` has Python-only extras and can be updated with **tested and pinned** versions. Do not blindly pip-install CPU-only torch, incompatible numpy or unverified `pyzed`/TensorRT wheels.
- Whisper.cpp is a separately built local binary on laptop/VM (if needed). It is **not a pip requirement**; no cloud API or LLM is needed to map recognized text into a small fixed command set.

## Record real versions on target
In a VM or Jetson terminal:

```bash
bash save_deps.sh
```

This writes `deps_snapshot.txt` with installed Ubuntu packages, Python freeze and environment metadata for later reproducibility. Do not commit private environment values or credentials.
