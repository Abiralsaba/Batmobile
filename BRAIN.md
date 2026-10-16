# BRAIN — Project Context (read before coding)

## Where code runs
- **Development**: Ubuntu **22.04 VM running on Mac**, **ROS 2 Humble**; not native macOS.
- **Deployment**: Jetson **Orin** target (exact module TBD), compatible Ubuntu 22.04 / JetPack / ROS 2 Humble. Verify board, JetPack, ZED X capture hardware and Stereolabs SDK support before installing.
- Mac VM architecture may be ARM64 or x86_64. Never commit prebuilt inference binaries for a different CPU/GPU. Jetson TensorRT engines are compiled on a compatible target.

## Hardware (existing unless explicitly deferred)
GNSS, IMU, Kalman/EKF, waypoint navigation, MIT motor bus/control, Raspberry Pi; their actual topic names/source files will be supplied later. ZED X stereo camera available; proper GMSL2 capture interface required. No LiDAR in this phase. Arm pickup and GIVE are deferred, **not removed**.

## Task scope / competition
URC 2027 Astronaut Assistance, first 50 points: EVA suit video/mic (5), GNSS approach within 3 m (5), quiet visual beckoning and autonomous FOLLOW within 3 m (15), STAY (5), FETCH hammer autonomously with arm (10), COME within 3 m (5), GIVE hammer (5). Entire Autonomy Mission is 40 minutes including route-finding.
- NOW: GNSS approach; person tracking with ZED X stereo range; gesture; development laptop voice; FOLLOW / STAY / COME; hammer detection and **authorization-gated staging approach**.
- LATER: EVA monitoring, true autonomous hammer pickup, GIVE; implement judged astronaut-origin commands.
- C2-issued commands and arm-free hammer approach do **not** count as completed judged FETCH. Sign/ArUco-only FOLLOW is not the full 15-point quiet gesture method. Avoid relying on ArUco for astronaut following.

## Architecture decisions
1. ROS 2 modularity with **one flat Python file per feature** in `rover/`. No nested module directories, no duplicate frameworks.
2. ZED SDK native body detection / tracking + 3D person estimate FIRST. Benchmark YOLO11n-Pose + ByteTrack only if native tracking underperforms. Use one active tracker.
3. ZED stereo depth for distance + obstacle monitoring. No LiDAR; not safe to drive outdoors without validated depth, path clearance, watchdog and E-stop.
4. Quiet beckoning: time series of body keypoints → rule baseline → tiny classifier only if needed. Do not equate open palm/fist with a quiet beckoning motion without task-specific validation.
5. Whisper.cpp locally for **development C2 microphone**; deterministic allowlist text parser. No LLM needed for fixed commands. Introduce astronaut audio later if chosen.
6. Existing GNSS + IMU + EKF for map navigation; use fresh astronaut location (not stale GNSS) for COME; visually refine last meters.
7. All AI outputs are observations/events. Mission FSM selects task; approved navigation and independent safety layer select motion. Only reviewed motor adapter can actuate. No module should publish hardware speed until authorized.
8. STOP is always available. STAY latches motion inhibit. Never assume a valid person target on missing/old camera frames. Approval YES must be state-scoped and expire when target validity changes in real integration.
9. Preserve and adapt prior rover code later; do not replace proven motor drivers or localization without reason.

## Interfaces pending real hardware
The topic names in `config.yaml` are illustrative. Query real ROS topics, frames and ZED wrapper version before integrating. Keep all measurements timestamped and in named frames (person relative to ROS `base_link`: X forward, Y left; depth confidence/uncertainty included).

## Important boundary
Current scaffold is **non-actuating**. `node.py` exposes `/dev/cmd` and `/rover/state` only; actual perception, Whisper, obstacle navigation and motor integration are intentionally unfinished. Make simulations/mock tests pass before real robot connection.

## Progress
- [x] Flat scaffold + docs + tests
- [ ] Verified Ubuntu 22.04 VM colcon build (run in actual VM)
- [ ] Verified Jetson hardware/JetPack/ZED X compatibility
- [ ] Camera tracking on recorded/ZED data
- [ ] Visual following with safe depth checks
- [ ] Full gesture/voice mission
- [ ] Hammer localization + approval approach
- [ ] EVA + manipulator for 50 points

When implementing a stage, update this checklist, `ROADMAP.md`, module docstring and dependencies. Never claim a hardware test that was not run.
