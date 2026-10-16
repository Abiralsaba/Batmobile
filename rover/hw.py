"""Hardware: placeholders for existing GNSS, IMU, EKF, Pi and MIT motor bus. DISABLED.

No actuation until owners provide driver code and safety requirements are verified.
"""


def drive(_linear_mps: float, _angular_rps: float):
    raise RuntimeError('MOTOR OUTPUT DISABLED: hardware/safety review required')


def get_rover_pose():
    raise NotImplementedError('Connect existing GNSS/IMU/EKF localization later')
